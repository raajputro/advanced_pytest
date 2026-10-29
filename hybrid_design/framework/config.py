"""Configuration is injected via pytest, not read inside page objects."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str
    browser: str
    headless: bool
    slow_mo: int
    timeout_ms: int
