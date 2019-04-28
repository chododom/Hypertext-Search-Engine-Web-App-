import shutil
import threading
import collections
import time

from PageRankApp.pagerank.src.domain import *
from PageRankApp.pagerank.src.search_engine import *
from PageRankApp.pagerank.src.config import *
from PageRankApp.pagerank.src.spider import Spider
from PageRankApp.pagerank.src.page_rank import *

DOMAIN_NAME = get_domain_name(HOMEPAGE)
pages = {}
threads = set()
queue = collections.deque()
queue.appendleft(HOMEPAGE)
crawled = set()
Spider(HOMEPAGE, DOMAIN_NAME, queue, crawled, pages)


def create_spiders():
    for x in range(THREAD_CNT):
        thread = threading.Thread(target=crawl)
        threads.add(thread)
        thread.daemon = True
        thread.start()


def crawl():
    while len(crawled) < PAGE_CNT:
        if len(queue) != 0:
            url = queue.pop()
            Spider.crawl_page(url)
            time.sleep(0.05)

def crawl_them_all():
    if CRAWL:
        try:
            shutil.rmtree(PARENT_DIR + "page_contents")
        except:
            print("Page_contents folder couldn't be removed as it doesn't exist")
        os.mkdir(PARENT_DIR + "page_contents")
        create_spiders()
        for thread in threads:
            thread.join()


'''
pages = {
        "1": Page(id=0, page_url="1", text_content='', outlinks=["2", "3"]),
        "2": Page(id=1, page_url="2", text_content='', outlinks=[]),
        "3": Page(id=2, page_url="3", text_content='', outlinks=["1", "2", "5"]),
        "4": Page(id=3, page_url="4", text_content='', outlinks=["5", "6"]),
        "5": Page(id=4, page_url="5", text_content='', outlinks=["4", "6"]),
        "6": Page(id=5, page_url="6", text_content='', outlinks=["4"])
    }
'''

if CALC_PR:
    PR = PageRank(pages, ALPHA, ITERATION_CNT, False)
    if METHOD == "matrix":
        print("Result - matrix method")
        pi_matrix = PR.do_page_rank_matrix()
        print("PR sum: " + str(pi_matrix.sum()))
        for pg in pages:
            pages[pg].rank = pi_matrix.toarray()[0][int(pages[pg].id)]
    elif METHOD == "power":
        print("\nResult - power method")
        pi_power = PR.do_page_rank()
        print("PR sum: " + str(pi_power.sum()))
        for pg in pages:
            pages[pg].rank = pi_power.toarray()[0][int(pages[pg].id)]

    # sort by Page Rank
    PageRank.printPagesPR(pages)
    PageRank.save_ranks(pages)


if INIT_SEARCH_INDEX:
    createSearchableData(PARENT_DIR + "page_contents")
    print("Created searchable data schema")

if SEARCH:
    final_res = search(SEARCH_WORD, RESULT_CNT)

for i in range(len(final_res)):
    PageRank.assign_ranks(final_res)
    print(final_res[i].page_url + "  ---  " + str(final_res[i].page_rank) + "  ---  " + str(final_res[i].content_rank))



