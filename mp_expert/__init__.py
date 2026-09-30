"""Deterministic Market Profile / Auction Reasoning Engine.

No ML, LLM, broker connection, execution logic, or participant-identity claims.
"""
from .engine import AuctionEngine
from .model import Bar, SessionContext, AuctionSnapshot, Evidence, Hypothesis

__all__ = ["AuctionEngine", "Bar", "SessionContext", "AuctionSnapshot", "Evidence", "Hypothesis"]
