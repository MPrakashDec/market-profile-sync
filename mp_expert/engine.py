from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Iterable

class EvidenceClass(str, Enum):
    OBSERVED="OBSERVED"; CALCULATED="CALCULATED"; INFERRED="INFERRED"; UNKNOWN="UNKNOWN"

class HypothesisStatus(str, Enum):
    OPEN="OPEN"; STRENGTHENING="STRENGTHENING"; WEAKENING="WEAKENING"; SUPPORTED="SUPPORTED"; INVALIDATED="INVALIDATED"

@dataclass(frozen=True)
class Bar:
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float=0.0
    oi: Optional[float]=None

@dataclass(frozen=True)
class SessionContext:
    prior_high: Optional[float]=None
    prior_low: Optional[float]=None
    prior_vah: Optional[float]=None
    prior_val: Optional[float]=None
    prior_poc: Optional[float]=None
    tick_size: float=5.0
    tpo_minutes: int=30

@dataclass(frozen=True)
class Evidence:
    timestamp: datetime
    code: str
    text: str
    evidence_class: EvidenceClass

@dataclass
class Hypothesis:
    code: str
    label: str
    status: HypothesisStatus=HypothesisStatus.OPEN
    support: list[Evidence]=field(default_factory=list)
    contradictions: list[Evidence]=field(default_factory=list)
    invalidation: Optional[str]=None

@dataclass(frozen=True)
class AuctionSnapshot:
    timestamp: datetime
    session_open: float
    last_price: float
    session_high: float
    session_low: float
    prior_location: str
    initial_range_high: float
    initial_range_low: float
    tpo_poc: Optional[float]
    vah: Optional[float]
    val: Optional[float]
    vwap: Optional[float]
    opening_type: str
    hypotheses: tuple[Hypothesis,...]
    evidence: tuple[Evidence,...]
    questions: tuple[str,...]
    narrative: str

class AuctionEngine:
    """Deterministic MP/AMT observer. Replay and live use the same snapshot_at()."""
    def __init__(self, bars: Iterable[Bar], context: SessionContext|None=None):
        self.bars=sorted(list(bars), key=lambda b:b.timestamp)
        if not self.bars: raise ValueError("At least one bar is required")
        self.context=context or SessionContext()
        self.session_open=self.bars[0].open

    def snapshots(self): return [self.snapshot_at(i) for i in range(len(self.bars))]

    def snapshot_at(self, i:int):
        bars=self.bars[:i+1]; now=bars[-1]; c=self.context
        loc="NO_PRIOR_REFERENCE"
        if c.prior_vah is not None and c.prior_val is not None:
            if c.prior_val <= self.session_open <= c.prior_vah: loc="INSIDE_PRIOR_VALUE"
            elif c.prior_low is not None and c.prior_low <= self.session_open <= c.prior_high: loc="INSIDE_PRIOR_RANGE_OUTSIDE_VALUE"
            elif c.prior_high is not None and self.session_open > c.prior_high: loc="ABOVE_PRIOR_RANGE"
            elif c.prior_low is not None and self.session_open < c.prior_low: loc="BELOW_PRIOR_RANGE"
        elif c.prior_low is not None and c.prior_high is not None:
            loc="INSIDE_PRIOR_RANGE" if c.prior_low <= self.session_open <= c.prior_high else ("ABOVE_PRIOR_RANGE" if self.session_open>c.prior_high else "BELOW_PRIOR_RANGE")

        irbars=[b for b in bars if b.timestamp < self.bars[0].timestamp+timedelta(minutes=c.tpo_minutes)]
        if not irbars: irbars=bars
        irh=max(b.high for b in irbars); irl=min(b.low for b in irbars)
        poc,vah,val=self._profile(bars)
        vwap=self._vwap(bars)
        ev=[]
        ev.append(Evidence(now.timestamp,"OPEN_LOCATION",loc,EvidenceClass.CALCULATED))
        if max(b.high for b in bars)>self.session_open: ev.append(Evidence(now.timestamp,"UP_PROBE","Trade above open",EvidenceClass.OBSERVED))
        if min(b.low for b in bars)<self.session_open: ev.append(Evidence(now.timestamp,"DOWN_PROBE","Trade below open",EvidenceClass.OBSERVED))
        if now.close>irh: ev.append(Evidence(now.timestamp,"UP_ACCEPTANCE_CANDIDATE","Current close is above developing initial range",EvidenceClass.INFERRED))
        if now.close<irl: ev.append(Evidence(now.timestamp,"DOWN_ACCEPTANCE_CANDIDATE","Current close is below developing initial range",EvidenceClass.INFERRED))
        hs=self._hypotheses(bars,irh,irl,ev)
        active=[h.label for h in hs if h.status in (HypothesisStatus.SUPPORTED,HypothesisStatus.STRENGTHENING)]
        label=active[0] if len(active)==1 else ("COMPETING_HYPOTHESES" if active else "UNRESOLVED")
        qs=["Has the initial probe earned acceptance?"] if len(bars)<3 else ["What new evidence would invalidate the current opening hypothesis?"]
        if loc=="INSIDE_PRIOR_VALUE": qs.insert(0,"Does price earn acceptance outside prior value, or remain responsive/rotational?")
        narrative=f"Open {loc.lower().replace('_',' ')}. Developing range {irh:g}-{irl:g}; POC {poc:g}, VA {val:g}-{vah:g}." if poc is not None else "Profile still forming."
        narrative += f" Opening read: {label}. Unresolved: {qs[0]}"
        return AuctionSnapshot(now.timestamp,self.session_open,now.close,max(b.high for b in bars),min(b.low for b in bars),loc,irh,irl,poc,vah,val,vwap,label,tuple(hs),tuple(ev),tuple(qs),narrative)

    def _profile(self,bars):
        t=defaultdict(int); s=self.context.tick_size
        for b in bars:
            for n in range(round(b.low/s),round(b.high/s)+1): t[n*s]+=1
        if not t: return None,None,None
        poc=max(t,key=lambda p:(t[p],-abs(p-self.session_open))); target=sum(t.values())*.70
        inc={poc}; total=t[poc]
        while total<target:
            p=max((p for p in t if p not in inc),key=lambda p:(t[p],-abs(p-poc)),default=None)
            if p is None: break
            inc.add(p); total+=t[p]
        return poc,min(inc),max(inc)

    @staticmethod
    def _vwap(bars):
        v=sum(max(0,b.volume) for b in bars)
        return None if v<=0 else sum(((b.high+b.low+b.close)/3)*b.volume for b in bars)/v

    def _hypotheses(self,bars,irh,irl,ev):
        now=bars[-1]; up=max(b.high for b in bars)>self.session_open; down=min(b.low for b in bars)<self.session_open
        upacc=now.close>irh; downacc=now.close<irl
        reclaim_up=up and any(b.close<=self.session_open for b in bars[-3:])
        reclaim_down=down and any(b.close>=self.session_open for b in bars[-3:])
        hs=[
            Hypothesis("OTD_UP","Open-Test-Drive Up",invalidation=f"acceptance below {self.session_open:g}"),
            Hypothesis("OTD_DOWN","Open-Test-Drive Down",invalidation=f"acceptance above {self.session_open:g}"),
            Hypothesis("ORR_UP","Open-Rejection-Reverse Up",invalidation=f"acceptance below {self.session_open:g}"),
            Hypothesis("ORR_DOWN","Open-Rejection-Reverse Down",invalidation=f"acceptance above {self.session_open:g}"),
            Hypothesis("OAIR","Open Auction / rotational",invalidation="directional acceptance outside opening structure")]
        if up and not downacc: hs[0].status=HypothesisStatus.STRENGTHENING
        if down and not upacc: hs[1].status=HypothesisStatus.STRENGTHENING
        if down and reclaim_down: hs[2].status=HypothesisStatus.STRENGTHENING
        if up and reclaim_up: hs[3].status=HypothesisStatus.STRENGTHENING
        if not upacc and not downacc: hs[4].status=HypothesisStatus.SUPPORTED
        if upacc: hs[1].status=HypothesisStatus.INVALIDATED
        if downacc: hs[0].status=HypothesisStatus.INVALIDATED
        return hs
