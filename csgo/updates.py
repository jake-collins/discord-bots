import feedparser
import os

from html.parser import HTMLParser
from logs.logger import logger

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "latest-title.txt")

class CustomHTMLParser(HTMLParser):
    parsedHtml = ''

    def handle_data(self, data):
        self.parsedHtml = self.parsedHtml + data

    def handle_starttag(self, tag, attrs):
        if (tag == 'p'):
            self.parsedHtml += '\n'

    def get_parsed_html(self):
        return self.parsedHtml

    def clear_parsed_html(self):
        self.parsedHtml = ''


def get_latest_update():
    result = feedparser.parse(
        'https://blog.counter-strike.net/index.php/category/updates/feed/',
        request_headers={'Cache-control': 'max-age=0'})
    title = result.entries[0].title
    parser = CustomHTMLParser()
    parser.clear_parsed_html()
    parser.feed(result.entries[0].content[0].value)
    return title, parser.get_parsed_html()


def read_latest_title():
    latest_title_file = open(filename)
    latest_title = latest_title_file.read()
    latest_title_file.close()
    return latest_title


def write_latest_title(latest_title):
    logger.info("Message sent.")
    logger.info("Updating latest-title.txt with %s...", latest_title)
    latest_update_file = open(filename, 'w')
    latest_update_file.write(latest_title)
    latest_update_file.close()
    logger.info("latest-title.txt updated.")
