import requests  # For making HTTP requests
from bs4 import BeautifulSoup  # For parsing HTML content
from datetime import datetime  # For working with dates and times
import os  # For file and directory operations
from logger import LOG  # For logging

class HackerNewsClient:
    def __init__(self):
        self.url = 'https://news.ycombinator.com/'  # Hacker News base URL

    def fetch_top_stories(self):
        LOG.debug("Fetching top stories from Hacker News.")
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()  # Ensure the request was successful
            return self.parse_stories(response.text)
        except requests.RequestException as e:
            LOG.error(f"Failed to fetch top stories: {e}")
            return []

    def parse_stories(self, html_content):
        LOG.debug("Parsing HTML content from Hacker News.")
        soup = BeautifulSoup(html_content, 'html.parser')
        story_rows = soup.find_all('tr', class_='athing')

        top_stories = []
        for story in story_rows:
            title_tag = story.find('span', class_='titleline').find('a')
            if title_tag:
                top_stories.append({
                    'title': title_tag.text,
                    'link': title_tag['href']
                })

        LOG.info(f"Parsed {len(top_stories)} top stories from Hacker News.")
        return top_stories

    def export_top_stories(self, date=None, hour=None):
        LOG.debug("Exporting top stories to markdown file.")
        top_stories = self.fetch_top_stories()

        if not top_stories:
            LOG.warning("No top stories found to export.")
            return None

        # Use current date and time if not provided
        date = date or datetime.now().strftime('%Y-%m-%d')
        hour = hour or datetime.now().strftime('%H')

        # Create directory path
        dir_path = os.path.join('hacker_news', date)
        os.makedirs(dir_path, exist_ok=True)

        # Create markdown file
        file_path = os.path.join(dir_path, f'{hour}.md')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(f"# Hacker News Top Stories ({date} {hour}:00)\n\n")
            for idx, story in enumerate(top_stories, start=1):
                file.write(f"{idx}. [{story['title']}]({story['link']})\n")

        LOG.info(f"Exported top stories to {file_path}")
        return file_path

if __name__ == "__main__":
    client = HackerNewsClient()
    client.export_top_stories()
