import logging
import re
import sys
import time
from urllib.request import Request, urlopen, URLError, HTTPError

from bs4 import BeautifulSoup
import coloredlogs
import yaml


# pylint: disable=C0103,missing-docstring,R0201
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',  # Setting up logging for the project
                    filename='logs/crawl_' + time.strftime("%H_%M_%S") + '.log',
                    filemode='w',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
coloredlogs.install(level='INFO', logger=logger)
class Crawler:
    def __init__(self, config):
        self.config = config
    def fetch_config(self):  # Function for fetching config file
        try:
            with open("configuration/config.yml", 'r') as ymlfile:
                self.config = yaml.load(ymlfile)
        except FileNotFoundError:
            raise
    def crawl(self, seedurl):  # Function which crawls the given url
        try:
            header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}
            request = Request(seedurl, headers=header)
            html_page = urlopen(request)
            content = BeautifulSoup(html_page, 'html.parser')  # Fetching content of the url
            links = []
            with open("./repository.txt", "a") as repository:  # Opening file for writing all the urls found
                for link in content.findAll('a', attrs={'href': re.compile("^https?://")}):  # Finding <a/> tag and href in HTML Body fetching urls which start with either http or https
                    url = link.get('href')
                    links.append(url)
                    repository.write(url + "\n")
                logger.info("Found %s urls from %s", len(links), seedurl)
        except (HTTPError, URLError) as ex:  # If HttpError or UrlError occurs donot pause crawling log the error in log file
            logger.error("Received error code %s from url - %s", ex, seedurl)
        except (ConnectionAbortedError, ConnectionRefusedError, \
                ConnectionResetError, ConnectionError):
            pass
    def start(self):    
        try:
            self.fetch_config()
            seedurl = self.config["crawler"]["seedUrl"]  # Fetching sed url from config
            logger.info("Starting Crawling seed url - %s", seedurl)
            self.crawl(seedurl)  # Crawling seed url
            logger.info("Finished Crawling seed url - %s", seedurl)
            number_of_urls = self.config["crawler"]["numberOfLinks"]  # Fetching number of urls to be crawled from config
            count = 0
            with open("./repository.txt", "r") as repo:
                for url in repo:  # Reading url from repository
                    if count != number_of_urls:
                        logger.info("Starting crawling from repository for url - %s", url)
                        self.crawl(url)  # Crawling fetched url
                        count += 1
                        logger.info('Finished crawling url - %s', url)
                    else:
                        break
                logger.info("Finished crawling from repository")
                sys.exit()
        except FileNotFoundError as ex:
            logger.error(ex)
            sys.exit()
        except KeyboardInterrupt:  # The program will terminate if user presses Ctrl+C
            logger.info("Terminating Crawling - User pressed Ctrl+C")
            sys.exit()
        except Exception as ex:
            logger.error("Encountered error %s with message %s", type(ex), ex)
            sys.exit()

if __name__ == "__main__":
    Crawler(None).start()
