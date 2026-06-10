"""Tests for Wisdom Database."""

import tempfile
import os
from lyra.wisdom import WisdomDatabase


class TestWisdomDatabase:
    """Test cases for WisdomDatabase class."""

    def test_default_data_loaded(self):
        """Test that default wisdom data is loaded."""
        db = WisdomDatabase()
        assert len(db) > 0

    def test_search_exact_match(self):
        """Test searching for an exact quote match."""
        db = WisdomDatabase()
        results = db.search("Socrates")
        assert len(results) > 0
        assert any("Socrates" in quote["author"] for quote in results)

    def test_search_partial_match(self):
        """Test searching for a partial match."""
        db = WisdomDatabase()
        results = db.search("life")
        assert len(results) > 0

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        db = WisdomDatabase()
        results_lower = db.search("socrates")
        results_upper = db.search("SOCRATES")
        assert len(results_lower) == len(results_upper)

    def test_search_limit(self):
        """Test that search respects the limit parameter."""
        db = WisdomDatabase()
        results = db.search("the", limit=3)
        assert len(results) <= 3

    def test_search_no_results(self):
        """Test search with no matching results."""
        db = WisdomDatabase()
        results = db.search("xyznonexistent123")
        assert len(results) == 0

    def test_get_random(self):
        """Test getting random quotes."""
        db = WisdomDatabase()
        results = db.get_random(limit=3)
        assert len(results) == 3
        assert all(isinstance(quote, dict) for quote in results)

    def test_get_by_tag(self):
        """Test getting quotes by tag."""
        db = WisdomDatabase()
        results = db.get_by_tag("philosophy")
        assert len(results) > 0
        for quote in results:
            assert "philosophy" in [t.lower() for t in quote["tags"]]

    def test_get_by_author(self):
        """Test getting quotes by author."""
        db = WisdomDatabase()
        results = db.get_by_author("Socrates")
        assert len(results) > 0
        assert all("Socrates" in quote["author"] for quote in results)

    def test_add_quote(self):
        """Test adding a new quote."""
        db = WisdomDatabase()
        initial_len = len(db)
        db.add_quote("Test quote", "Test Author", ["test"])
        assert len(db) == initial_len + 1

    def test_load_from_file(self):
        """Test loading wisdom data from a file."""
        test_data = [
            {"text": "Test quote 1", "author": "Author 1", "tags": ["test"]},
            {"text": "Test quote 2", "author": "Author 2", "tags": ["test"]},
        ]

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            import json
            json.dump(test_data, f)
            temp_path = f.name

        try:
            db = WisdomDatabase(data_path=temp_path)
            assert len(db) == 2
            assert db.quotes[0]["text"] == "Test quote 1"
        finally:
            os.unlink(temp_path)

    def test_save_to_file(self):
        """Test saving wisdom data to a file."""
        db = WisdomDatabase()
        db.add_quote("New quote", "New Author", ["new"])

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_path = f.name

        try:
            db.save_to_file(temp_path)

            # Verify the file was saved correctly
            db2 = WisdomDatabase(data_path=temp_path)
            assert len(db2) == len(db)
            assert db2.quotes[-1]["text"] == "New quote"
        finally:
            os.unlink(temp_path)

    def test_repr(self):
        """Test string representation."""
        db = WisdomDatabase()
        repr_str = repr(db)
        assert "WisdomDatabase" in repr_str
        assert str(len(db)) in repr_str
