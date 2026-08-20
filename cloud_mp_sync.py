import os
import requests
import json
import datetime
import pandas as pd
import numpy as np

def run_cloud_sync():
    print(f"=== [3:08 PM IST CLOUD SYNC] Starting at {datetime.datetime.now()} ===")
    
    # 1. Fetch Upstox Zero-Token Intraday Candles
    fut_key = "NSE_FO|58072"  # NIFTY Current Month Futures
    index_key = "NSE_INDEX|Nifty 50"
    
    url_fut = f"https://api.upstox.com/v2/historical-candle/intraday/{fut_key}/1minute"
    url_spot = f"https://api.upstox.com/v2/historical-candle/intraday/{index_key}/1minute"
    
    r_fut = requests.get(url_fut, headers={"Accept": "application/json"}, timeout=15)
    r_spot = requests.get(url_spot, headers={"Accept": "application/json"}, timeout=15)
    
    if r_fut.status_code != 200 or not r_fut.json().get("data", {}).get("candles"):
        print("[WARN] Futures intraday candle fetch failed, using spot data.")
        df_candles = pd.DataFrame(r_spot.json()["data"]["candles"], columns=["timestamp", "open", "high", "low", "close", "vol", "oi"])
    else:
        df_candles = pd.DataFrame(r_fut.json()["data"]["candles"], columns=["timestamp", "open", "high", "low", "close", "vol", "oi"])

    df_candles["datetime"] = pd.to_datetime(df_candles["timestamp"]).dt.tz_convert("Asia/Kolkata")
    df_candles = df_candles.sort_values("datetime").reset_index(drop=True)
    
    # Daily Candles for ATR(14) & 5DR
    today_str = datetime.datetime.now().strftime("%Y-%m-%d")
    url_daily = f"https://api.upstox.com/v2/historical-candle/{index_key}/day/{today_str}/2026-06-01"
    r_daily = requests.get(url_daily, headers={"Accept": "application/json"}, timeout=15)
    df_daily = pd.DataFrame(r_daily.json().get("data", {}).get("candles", []), columns=["timestamp", "open", "high", "low", "close", "vol", "oi"])
    df_daily["datetime"] = pd.to_datetime(df_daily["timestamp"]).dt.tz_convert("Asia/Kolkata")
    df_daily = df_daily.sort_values("datetime").reset_index(drop=True)
    
    # ATR(14)
    tr1 = df_daily["high"] - df_daily["low"]
    tr2 = np.abs(df_daily["high"] - df_daily["close"].shift())
    tr3 = np.abs(df_daily["low"] - df_daily["close"].shift())
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr_14 = round(float(tr.rolling(14).mean().iloc[-1]), 0)
    five_dr = round(float((df_daily["high"] - df_daily["low"]).tail(5).mean()), 0)
    
    high = round(float(df_candles["high"].max()), 1)
    low = round(float(df_candles["low"].min()), 1)
    ltp = round(float(df_candles["close"].iloc[-1]), 1)
    mid = round((high + low) / 2.0, 1)
    range_pts = round(high - low, 0)
    
    # IB (First 60 bars: 09:15 to 10:15)
    ib_df = df_candles.iloc[:60]
    ibh = round(float(ib_df["high"].max()), 0)
    ibl = round(float(ib_df["low"].min()), 0)
    
    # VWAP
    cum_vol = float(df_candles["vol"].sum())
    if cum_vol > 0:
        typ = (df_candles["high"] + df_candles["low"] + df_candles["close"]) / 3.0
        vwap = round(float((typ * df_candles["vol"]).sum() / cum_vol), 0)
    else:
        vwap = mid
        
    vol_lakhs = round(cum_vol / 100000.0, 0)
    
    # TPO Value Area & POC
    price_bins = []
    for idx, row in df_candles.iterrows():
        steps = np.arange(round(row["low"]/5)*5, round(row["high"]/5)*5 + 5, 5)
        price_bins.extend(steps)

    counts = pd.Series(price_bins).value_counts().sort_index()
    poc = round(float(counts.idxmax()), 0)

    total_tpos = len(price_bins)
    target_va = total_tpos * 0.70
    sorted_c = counts.sort_values(ascending=False)
    cum_tpos = sorted_c.cumsum()
    va_levels = sorted_c[cum_tpos <= target_va].index
    vah = round(float(va_levels.max() if len(va_levels) > 0 else high), 0)
    val = round(float(va_levels.min() if len(va_levels) > 0 else low), 0)
    
    today_formatted = datetime.datetime.now().strftime("%-m/%-d/%Y") if os.name != 'nt' else datetime.datetime.now().strftime("%m/%d/%Y").replace("/0", "/")
    
    # 2. AI Narrative Generation (Groq / Gemini)
    groq_key = os.getenv("GROQ_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    day_recap = f"Session Range: [{low} - {high}] with Range {range_pts} pts. High-Value balance established at POC {poc}."
    auction_achieved = f"Tested Session Extremes: High {high} / Low {low}."
    info_carry_fwd = f"VAH: {vah}, POC: {poc}, VAL: {val}. Watch IBH {ibh} and IBL {ibl} as immediate boundary brackets."
    
    prompt = f"Given Nifty session data: High={high}, Low={low}, Close={ltp}, VAH={vah}, POC={poc}, VAL={val}, IBH={ibh}, IBL={ibl}, Range={range_pts}. Provide 3 crisp sentences: 1. Day Recap (Open/Day Type), 2. Auction Achieved (Key targets/structures), 3. Info to Carry Forward (Next day pivots). Separate each with a pipe | character."
    
    if groq_key:
        try:
            url_g = "https://api.groq.com/openai/v1/chat/completions"
            p_g = {"model": "qwen/qwen3.6-27b", "messages": [{"role": "user", "content": prompt}], "temperature": 0.1}
            r_g = requests.post(url_g, headers={"Authorization": f"Bearer {groq_key}", "Content-Type": "application/json"}, json=p_g, timeout=10)
            if r_g.status_code == 200:
                txt = r_g.json()["choices"][0]["message"]["content"]
                if "</think>" in txt: txt = txt.split("</think>")[-1].strip()
                parts = [p.strip() for p in txt.split("|")]
                if len(parts) >= 3:
                    day_recap, auction_achieved, info_carry_fwd = parts[0], parts[1], parts[2]
        except Exception as e:
            print(f"[AI Fallback]: {e}")

    # 3. Append to CSV
    csv_file = "market_profile_history.csv"
    new_row = f'{today_formatted},{high},{low},{ltp},{mid},{vah},{poc},{val},{vwap},{ibh},{ibl},{range_pts},{atr_14},{five_dr},{vol_lakhs},"{day_recap}","{auction_achieved}","{info_carry_fwd}"\n'
    
    # Check if today already exists
    if os.path.exists(csv_file):
        with open(csv_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        if not any(today_formatted in l for l in lines):
            with open(csv_file, "a", encoding="utf-8") as f:
                f.write(new_row)
            print("[SUCCESS] Appended new row to market_profile_history.csv")
    
    # 4. Generate README.md Markdown Table
    try:
        df_all = pd.read_csv(csv_file)
        md_table = df_all.to_markdown(index=False)
        readme_content = f"# 🏛️ Deskworks Cloud Market Profile Ledger\n\n*Automated 3:08 PM IST Cloud Sync powered by Upstox Public Zero-Token Engine + Gemini/Groq AI.*\n\nLast Updated: `{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S IST')}`\n\n{md_table}\n"
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("[SUCCESS] Generated README.md")
    except Exception as e:
        print(f"[README Error]: {e}")

    # 5. Telegram Broadcast
    tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
    tg_chat = os.getenv("TELEGRAM_CHAT_ID")
    if tg_token and tg_chat:
        msg = f"🏛️ *MARKET PROFILE 3:08 PM CLOUD SYNC*\n\n" \
              f"📅 *Date:* `{today_formatted}`\n" \
              f"📈 *High:* `{high}` | *Low:* `{low}` | *LTP:* `{ltp}`\n" \
              f"🎯 *VAH:* `{vah}` | *POC:* `{poc}` | *VAL:* `{val}`\n" \
              f"📏 *IBH:* `{ibh}` | *IBL:* `{ibl}` | *Range:* `{range_pts} pts`\n" \
              f"⚡ *ATR(14):* `{atr_14}` | *5DR:* `{five_dr}`\n\n" \
              f"📝 *Day Recap:* {day_recap}\n\n" \
              f"🎯 *Auction Achieved:* {auction_achieved}\n\n" \
              f"🔮 *Carry Forward:* {info_carry_fwd}\n\n" \
              f"✅ *Synced to Cloud Repository autonomously.*"
        try:
            tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
            requests.post(tg_url, json={"chat_id": tg_chat, "text": msg, "parse_mode": "Markdown"}, timeout=10)
            print("[SUCCESS] Sent Telegram broadcast!")
        except Exception as e:
            print(f"[TG Error]: {e}")

if __name__ == "__main__":
    run_cloud_sync()
