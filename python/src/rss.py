import feedparser
import logging
import datetime
import time

FEED_LIST = '/data/feeds'

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


def parse_time(struct_time):
    t = time.mktime(struct_time)
    return datetime.datetime.fromtimestamp(t)

def get_feed_urls():
    try:
        with open(FEED_LIST, 'r') as f:
            return f.readlines()
    except:
        logger.exception("Can't read feed file")
        return []

def process_url(url):
    url = url.strip()
    logger.debug("Starting parsing of '{}'".format(url))
    d = feedparser.parse(url)
    feed = d.feed
    title = feed.title
    logger.debug("Feed title '{}'".format(title))
    entries = d.entries
    logger.debug("Found {} entries".format(len(entries)))
    x = [process_entry(e) for e in entries]

def process_entry(entry):
    title = entry.title
    summary = entry.summary
    dt = parse_time(entry.published_parsed)
    url = entry.link
    logger.debug("{} was published on {} (available at {})".format(title, dt, url))
    logger.debug(summary[:100])



def main():
    logger.info("Hello world")
    feed_urls = get_feed_urls()
    feed_objs = [process_url(url) for url in feed_urls]
    logger.info("Done")
