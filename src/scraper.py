import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import json

class BillboardScraper:
    def __init__(self):
        self.base_url = "https://www.billboard.com/charts/hot-100/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }

    def fetch_chart(self, date=None):
        """Fetch Billboard Hot 100 chart for a specific date or current."""
        url = self.base_url
        if date:
            url += date
        
        response = requests.get(url, headers=self.headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch data: {response.status_code}")
        
        return response.text

    def parse_chart(self, html_content):
        """Parse HTML content and extract chart data."""
        soup = BeautifulSoup(html_content, 'html.parser')
        songs = []

        chart_items = soup.select("div.chart-results-list > div.o-chart-results-list-row-container")
        
        for item in chart_items:
            try:
                rank = item.select_one("span.c-label").text.strip()
                title = item.select_one("h3#title-of-a-story").text.strip()
                artist = item.select_one("span.c-label.a-no-trucate").text.strip()
                
                songs.append({
                    "rank": int(rank),
                    "title": title,
                    "artist": artist
                })
            except Exception as e:
                print(f"Error parsing item: {e}")
                continue

        return songs

    def export_to_csv(self, songs, filename=None):
        """Export songs data to CSV file."""
        if not filename:
            filename = f"billboard_hot_100_{datetime.now().strftime('%Y%m%d')}.csv"
        
        df = pd.DataFrame(songs)
        df.to_csv(filename, index=False)
        return filename

    def export_to_json(self, songs, filename=None):
        """Export songs data to JSON file."""
        if not filename:
            filename = f"billboard_hot_100_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(filename, 'w') as f:
            json.dump(songs, f, indent=2)
        return filename

    def analyze_trends(self, songs):
        """Analyze trends in the chart data."""
        analysis = {
            "total_songs": len(songs),
            "artists": {},
            "top_10": songs[:10]
        }

        # Count songs per artist
        for song in songs:
            artist = song["artist"]
            if artist in analysis["artists"]:
                analysis["artists"][artist] += 1
            else:
                analysis["artists"][artist] = 1

        # Sort artists by number of songs
        analysis["top_artists"] = dict(
            sorted(analysis["artists"].items(), 
                  key=lambda x: x[1], 
                  reverse=True)[:5]
        )

        return analysis 