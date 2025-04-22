import pytest
from src.scraper import BillboardScraper
import os
from datetime import datetime

@pytest.fixture
def scraper():
    return BillboardScraper()

def test_scraper_initialization(scraper):
    assert scraper.base_url == "https://www.billboard.com/charts/hot-100/"
    assert isinstance(scraper.headers, dict)

def test_fetch_chart(scraper):
    html_content = scraper.fetch_chart()
    assert isinstance(html_content, str)
    assert len(html_content) > 0
    assert "billboard" in html_content.lower()

def test_parse_chart(scraper):
    html_content = scraper.fetch_chart()
    songs = scraper.parse_chart(html_content)
    
    assert isinstance(songs, list)
    assert len(songs) > 0
    
    # Test first song structure
    first_song = songs[0]
    assert "rank" in first_song
    assert "title" in first_song
    assert "artist" in first_song
    assert isinstance(first_song["rank"], int)
    assert isinstance(first_song["title"], str)
    assert isinstance(first_song["artist"], str)

def test_export_to_csv(scraper, tmp_path):
    songs = [
        {"rank": 1, "title": "Test Song", "artist": "Test Artist"},
        {"rank": 2, "title": "Another Song", "artist": "Another Artist"}
    ]
    
    filename = scraper.export_to_csv(songs, tmp_path / "test.csv")
    assert os.path.exists(filename)
    
    # Clean up
    os.remove(filename)

def test_export_to_json(scraper, tmp_path):
    songs = [
        {"rank": 1, "title": "Test Song", "artist": "Test Artist"},
        {"rank": 2, "title": "Another Song", "artist": "Another Artist"}
    ]
    
    filename = scraper.export_to_json(songs, tmp_path / "test.json")
    assert os.path.exists(filename)
    
    # Clean up
    os.remove(filename)

def test_analyze_trends(scraper):
    songs = [
        {"rank": 1, "title": "Song 1", "artist": "Artist A"},
        {"rank": 2, "title": "Song 2", "artist": "Artist A"},
        {"rank": 3, "title": "Song 3", "artist": "Artist B"}
    ]
    
    analysis = scraper.analyze_trends(songs)
    
    assert "total_songs" in analysis
    assert "artists" in analysis
    assert "top_10" in analysis
    assert "top_artists" in analysis
    
    assert analysis["total_songs"] == 3
    assert analysis["artists"]["Artist A"] == 2
    assert analysis["artists"]["Artist B"] == 1
    assert len(analysis["top_10"]) == 3 