import math

from PageRankApp.pagerank.src.matrix_factory import MatrixFactory
from PageRankApp.pagerank.src.config import *


class PageRank:
    matfact = MatrixFactory
    alpha = 0.85
    length = 1
    iteration_count = 50
    debug = False

    def __init__(self, pages, alpha, iteration_count, debug):
        self.matfact = MatrixFactory(pages)
        self.length = len(pages)
        self.alpha = alpha
        self.iteration_count = iteration_count
        self.debug = debug

    # calculates the next PageRank vector iteration using the power method
    # def get_next_iteration(self):
    # todo - split to logical parts
    def do_page_rank(self):
        H = self.matfact.get_matrix_H()
        a = self.matfact.get_dangling_node_vector()
        pi = self.matfact.get_default_page_rank_vector()
        e = self.matfact.get_unit_vector()

        '''
        print("H matrix")
        print(H.todense())
        print("a vector")
        print(a.todense())
        print("PI vector")
        print(pi.todense())
        print("e vector")
        print(e.todense())
        print("pi * a")
        print(pi.dot(a).todense())
        print("pi * H")
        print(pi.dot(H).todense())
        print("pi * H * alpha")
        print(pi.dot(H).multiply(self.alpha).todense())
        '''
        if self.debug:
            print("Iterations:")
        for i in range(self.iteration_count):
            if self.debug:
                print(pi.todense())
            pi = pi.dot(H).multiply(self.alpha) + e.multiply((pi.dot(a).toarray()[0][0] * self.alpha + 1 - self.alpha)/self.length)
        if self.debug:
            print()
        return pi

    def do_page_rank_matrix(self):
        pi = self.matfact.get_default_page_rank_vector()
        e = self.matfact.get_unit_vector()
        S = self.matfact.get_matrix_S()

        E = (e.transpose(copy=True)).dot(e).multiply((1-self.alpha)/self.length)  # matrix of ((1-alpha)/n)*(e * e^T)
        aS = S.multiply(self.alpha)
        aSE = aS+E
        if self.debug:
            print("Iterations:")
        for i in range(self.iteration_count):
            if self.debug:
                print(pi.todense())
            pi = pi.dot(aSE)
        if self.debug:
            print()
        return pi

    def save_ranks(pgs):
        res = list(pgs.values())
        # res.sort(key=lambda x: x.page_url, reverse=True)
        f = open(PARENT_DIR + "page_ranks/ranks", mode="w+", encoding="utf-8")
        for pg in res:
            f.write(pg.page_url + " #PAGERANK# " + str(pg.rank) + "\n")
        f.close()

    def printPagesPR(pgs):
        res = list(pgs.values())
        res.sort(key=lambda x: x.rank, reverse=True)
        for pg in res:
            print(pg)

    def assign_ranks(res):
        maxPR = - math.inf
        minPR = math.inf
        for i in range(len(res)):
            with open(PARENT_DIR + "page_ranks/ranks", mode="r", encoding="utf-8") as fp:
                line = fp.readline()
                while line:
                    if line.split(" #PAGERANK# ")[0] == res[i].page_url:
                        res[i].page_rank = float(line.split(" #PAGERANK# ")[1].strip())
                        if res[i].page_rank > maxPR:
                            maxPR = res[i].page_rank
                        if res[i].page_rank < minPR:
                            minPR = res[i].page_rank
                        break
                    line = fp.readline()

        new_max = 10
        new_min = 1
        slopePR = (new_max - new_min) / (maxPR - minPR)
        for j in range(len(res)):
            # normalize ranks to range [new_min, new_max]
            res[j].normalized_page_rank = (slopePR * (res[j].page_rank - minPR)) + new_min
            res[j].normalized_page_rank = round(res[j].normalized_page_rank, 2)

            # combine page rank and content rank
            res[j].combined_rank = PR_WEIGHT * res[j].normalized_page_rank + CR_WEIGHT * res[j].content_rank

