import abc
from typing import Dict, List, Any

class BaseScraper(abc.ABC):
    """Abstract base class for all scrapers."""
    
    @abc.abstractmethod
    def scrape(self, source: str) -> List[Dict[str, Any]]:
        """Scrape data from the given source."""
        pass
    
    @abc.abstractmethod
    def clean(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Clean the scraped data."""
        pass
