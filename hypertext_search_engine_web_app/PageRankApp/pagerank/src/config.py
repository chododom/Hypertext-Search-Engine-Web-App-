HOMEPAGE = 'https://fit.cvut.cz/'
CRAWL = False
THREAD_CNT = 30     # number of spiders to crawl the web
PAGE_CNT = 100     # approximate number of pages to search
CALC_PR = True and CRAWL    # CRAWL must be True in order for CALC_PR to work
ALPHA = 0.85
ITERATION_CNT = 50  # number of iterations to calculate page ranks
METHOD = "power"    # power / matrix
INIT_SEARCH_INDEX = False
SEARCH = False
SEARCH_WORD = "Den otevřených dveří FIT ČVUT"   # searched keyword or phrase
RESULT_CNT = 10     # number of shown top results
PR_WEIGHT = 1   # weight of page rank value in combined ranking
CR_WEIGHT = 1.5   # weight of content rank value in combined ranking

PARENT_DIR = "PageRankApp/pagerank/"