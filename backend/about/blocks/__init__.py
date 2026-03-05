"""about/blocks/__init__.py."""

from .about_page import FounderHistoryBlock
from .wholesale_page import (
    TabItemBlock,
    TabMiniItemBlock,
    WholesaleIntroBlock,
    WholesaleTabsBlock,
)

__all__ = [
    "FounderHistoryBlock",
    "TabItemBlock",
    "TabMiniItemBlock",
    "WholesaleIntroBlock",
    "WholesaleTabsBlock",
]
