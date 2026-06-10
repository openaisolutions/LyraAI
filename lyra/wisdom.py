"""
Wisdom Database for LYRA AI.
"""

import json
import random
from typing import List, Dict, Optional


class WisdomDatabase:
    """
    A database of wisdom quotes, philosophies, and insights.

    Attributes:
        quotes: List of wisdom entries (dicts with 'text', 'author', 'tags').
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize the Wisdom Database.

        Args:
            data_path: Path to a JSON file containing wisdom data.
                      If None, uses default embedded data.
        """
        self.quotes: List[Dict[str, str]] = []

        if data_path:
            self.load_from_file(data_path)
        else:
            self._load_default_data()

    def _load_default_data(self) -> None:
        """Load default wisdom data into the database."""
        default_quotes = [
            {
                "text": "The only true wisdom is in knowing you know nothing.",
                "author": "Socrates",
                "tags": ["humility", "knowledge", "philosophy"]
            },
            {
                "text": "The journey of a thousand miles begins with one step.",
                "author": "Lao Tzu",
                "tags": ["journey", "persistence", "taoism"]
            },
            {
                "text": "To thine own self be true.",
                "author": "William Shakespeare",
                "tags": ["authenticity", "self", "truth"]
            },
            {
                "text": "The unexamined life is not worth living.",
                "author": "Socrates",
                "tags": ["self-reflection", "life", "philosophy"]
            },
            {
                "text": "That which does not kill us makes us stronger.",
                "author": "Friedrich Nietzsche",
                "tags": ["resilience", "strength", "adversity"]
            },
            {
                "text": (
                    "The greatest glory in living lies not in never falling, "
                    "but in rising every time we fall."
                ),
                "author": "Nelson Mandela",
                "tags": ["resilience", "perseverance", "inspiration"]
            },
            {
                "text": "The way to get started is to quit talking and begin doing.",
                "author": "Walt Disney",
                "tags": ["action", "motivation", "productivity"]
            },
            {
                "text": (
                    "Your time is limited, so don't waste it living "
                    "someone else's life."
                ),
                "author": "Steve Jobs",
                "tags": ["purpose", "time", "authenticity"]
            },
            {
                "text": (
                    "If you look at what you have in life, you'll always have more. "
                    "If you look at what you don't have in life, you'll never have "
                    "enough."
                ),
                "author": "Oprah Winfrey",
                "tags": ["gratitude", "abundance", "mindset"]
            },
            {
                "text": (
                    "The only limit to our realization of tomorrow is our "
                    "doubts of today."
                ),
                "author": "Franklin D. Roosevelt",
                "tags": ["future", "doubt", "potential"]
            },
            {
                "text": (
                    "Do not go where the path may lead, go instead where there "
                    "is no path and leave a trail."
                ),
                "author": "Ralph Waldo Emerson",
                "tags": ["innovation", "leadership", "courage"]
            },
            {
                "text": (
                    "The best and most beautiful things in the world cannot be "
                    "seen or even touched - they must be felt with the heart."
                ),
                "author": "Helen Keller",
                "tags": ["beauty", "heart", "perception"]
            },
        ]
        self.quotes = default_quotes

    def load_from_file(self, data_path: str) -> None:
        """
        Load wisdom data from a JSON file.

        Args:
            data_path: Path to the JSON file.
        """
        try:
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.quotes = data
                else:
                    raise ValueError("Wisdom data must be a list of quotes.")
        except FileNotFoundError:
            raise FileNotFoundError(f"Wisdom data file not found: {data_path}")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in wisdom data file: {data_path}")

    def save_to_file(self, data_path: str) -> None:
        """
        Save the wisdom database to a JSON file.

        Args:
            data_path: Path to save the JSON file.
        """
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(self.quotes, f, indent=2, ensure_ascii=False)

    def add_quote(self, text: str, author: str, tags: List[str]) -> None:
        """
        Add a new quote to the database.

        Args:
            text: The quote text.
            author: The author of the quote.
            tags: List of tags for categorization.
        """
        self.quotes.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    def search(self, query: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Search the wisdom database for quotes matching a query.

        Args:
            query: Search term (case-insensitive, matches text/author/tags).
            limit: Maximum number of results to return.

        Returns:
            List of matching quotes (dicts).
        """
        query_lower = query.lower()
        results = []

        for quote in self.quotes:
            # Check if query matches text, author, or any tag
            if (
                query_lower in quote["text"].lower() or
                query_lower in quote["author"].lower() or
                any(query_lower in tag.lower() for tag in quote.get("tags", []))
            ):
                results.append(quote)

        return results[:limit]

    def get_random(self, limit: int = 1) -> List[Dict[str, str]]:
        """
        Get random quotes from the database.

        Args:
            limit: Number of random quotes to return.

        Returns:
            List of random quotes (dicts).
        """
        return random.sample(self.quotes, min(limit, len(self.quotes)))

    def get_by_tag(self, tag: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Get quotes by a specific tag.

        Args:
            tag: Tag to filter by (case-insensitive).
            limit: Maximum number of results to return.

        Returns:
            List of quotes with the specified tag.
        """
        tag_lower = tag.lower()
        results = [
            quote for quote in self.quotes
            if tag_lower in [t.lower() for t in quote.get("tags", [])]
        ]
        return results[:limit]

    def get_by_author(self, author: str, limit: int = 5) -> List[Dict[str, str]]:
        """
        Get quotes by a specific author.

        Args:
            author: Author name (case-insensitive).
            limit: Maximum number of results to return.

        Returns:
            List of quotes by the specified author.
        """
        author_lower = author.lower()
        results = [
            quote for quote in self.quotes
            if author_lower in quote["author"].lower()
        ]
        return results[:limit]

    def __len__(self) -> int:
        """Return the number of quotes in the database."""
        return len(self.quotes)

    def __repr__(self) -> str:
        """Return a string representation of the database."""
        return f"WisdomDatabase({len(self)} quotes)"
