import urllib.request
import collections
from bs4 import BeautifulSoup

from PageRankApp.pagerank.src.link_finder import LinkFinder
from PageRankApp.pagerank.src.page import *
from PageRankApp.pagerank.src.config import *
from PageRankApp.pagerank.src.domain import *


class Spider:
    visitedPages = 0
    project_name = ''
    base_url = ''
    domain_name = ''
    queue = collections.deque()
    crawled = set()
    pages = {}

    def __init__(self, base_url, domain_name, queue, crawled, pages):
        Spider.visitedPages = 0
        Spider.base_url = base_url
        Spider.domain_name = domain_name
        Spider.queue = queue
        Spider.crawled = crawled
        Spider.pages = pages

    @staticmethod
    def crawl_page(page_url):
        # skip pages with names of teachers
        if page_url.find('#') != -1:
            return

        print('Crawling page url: ' + page_url)
        Spider.visitedPages += 1
        print('Visited pages: ' + str(Spider.visitedPages))
        if page_url not in Spider.crawled:
            Spider.enqueue_links(Spider.gather_links(page_url), page_url)
            Spider.crawled.add(page_url)
        return Spider.pages

    @staticmethod
    def gather_links(page_url):
        html_string = ''
        try:
            response = urllib.request.urlopen(page_url)
            if 'text/html' in response.getheader('Content-Type'):
                html_bytes = response.read()
                html_string = html_bytes.decode("utf-8")
            finder = LinkFinder(Spider.base_url, page_url)
            finder.feed(html_string)

            # extract visible text
            soup = BeautifulSoup(html_string, "html.parser")
            for s in soup(['style', 'script', '[document]', 'head', 'title']):
                # removes tag
                s.extract()

            visible_text = soup.getText()
            outlinks = finder.page_links()

            f = open(PARENT_DIR + "page_contents/" + str(len(Spider.pages)), mode="w+", encoding="utf-8")
            f.write(page_url + "\n" + visible_text)
            f.close()

            page = Page(len(Spider.pages), page_url, visible_text, outlinks)
            Spider.pages[page_url] = page
            return outlinks
        except:
            # print('Error: could not crawl page')
            return set()

    @staticmethod
    def enqueue_links(links, page_url):
        for url in links:
            Spider.pages[page_url].outlinks.add(url)
            if (url in Spider.queue) or (url in Spider.crawled):
                continue
            if Spider.domain_name != get_domain_name(url):
                continue
            Spider.queue.appendleft(url)
