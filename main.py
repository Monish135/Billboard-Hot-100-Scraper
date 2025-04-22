#!/usr/bin/env python3
"""Main entry point for the Billboard Hot 100 Scraper application."""

from src.scraper import BillboardScraper
import argparse
from datetime import datetime

def main():
    parser = argparse.ArgumentParser(description='Billboard Hot 100 Chart Scraper')
    parser.add_argument('--date', type=str, help='Date in YYYY-MM-DD format (default: current)')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv',
                       help='Export format (default: csv)')
    args = parser.parse_args()

    try:
        scraper = BillboardScraper()
        
        # Format date if provided
        date_str = None
        if args.date:
            try:
                date_obj = datetime.strptime(args.date, '%Y-%m-%d')
                date_str = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                print("Invalid date format. Please use YYYY-MM-DD")
                return

        # Fetch and parse chart
        print("Fetching Billboard Hot 100 chart...")
        html_content = scraper.fetch_chart(date_str)
        
        print("Parsing chart data...")
        songs = scraper.parse_chart(html_content)
        
        # Export data
        if args.format == 'csv':
            filename = scraper.export_to_csv(songs)
        else:
            filename = scraper.export_to_json(songs)
        print(f"Data exported to {filename}")
        
        # Show analysis
        print("\nAnalyzing trends...")
        analysis = scraper.analyze_trends(songs)
        
        print(f"\nTotal songs: {analysis['total_songs']}")
        print("\nTop 5 Artists:")
        for artist, count in analysis['top_artists'].items():
            print(f"- {artist}: {count} songs")
        
        print("\nTop 10 Songs:")
        for song in analysis['top_10']:
            print(f"#{song['rank']}: {song['title']} by {song['artist']}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
