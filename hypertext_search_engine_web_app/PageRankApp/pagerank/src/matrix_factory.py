from scipy import sparse


class MatrixFactory:
    pages = dict()
    length = 0

    def __init__(self, pages):
        self.pages = pages
        self.length = len(pages)
        self.cut_off_domain()

    # return basic sparse matrix H
    def get_matrix_H(self):
        row_indexes = []
        col_indexes = []
        data = []

        urls = {page_url for page_url in self.pages}  # list of all URLs

        for purl in self.pages:
            pg = self.pages[purl]  # iterated page

            # if no out-links at page
            if not pg.outlinks:
                continue
            # else otherwise
            else:
                for link in pg.outlinks:  # for all pages
                    if link in urls:  # if pg has out-link to link append alpha*(1 / (count of pg' out-links))
                        row_indexes.append(pg.id)
                        col_indexes.append(self.pages[link].id)
                        data.append(1 / len(pg.outlinks))

        mat = sparse.bsr_matrix((data, (row_indexes, col_indexes)), shape=(self.length, self.length), dtype='double')
        return mat

    # return row vector of 1/n (n - number of pages)
    def get_default_page_rank_vector(self):
        row_indexes = []
        col_indexes = []
        data = []
        for i in range(self.length):
            row_indexes.append(0)
            col_indexes.append(i)
            data.append(1 / self.length)

        return sparse.bsr_matrix((data, (row_indexes, col_indexes)), shape=(1, self.length), dtype='double')

    # returns row vector of 1

    def get_unit_vector(self):
        row_indexes = []
        col_indexes = []
        data = []
        for i in range(self.length):
            row_indexes.append(0)
            col_indexes.append(i)
            data.append(1)

        return sparse.bsr_matrix((data, (row_indexes, col_indexes)), shape=(1, self.length), dtype='int32')

    # returns column vector of binary values (1 - page has no out-links, 0 - otherwise)
    def get_dangling_node_vector(self):
        row_indexes = []
        col_indexes = []
        data = []

        for page in self.pages:
            if not self.pages[page].outlinks:
                row_indexes.append(0)
                col_indexes.append(self.pages[page].id)
                data.append(1)

        return sparse.bsr_matrix((data, (row_indexes, col_indexes)), shape=(1, self.length), dtype='int32').transpose()

    # return basic sparse matrix S
    def get_matrix_S(self):
        row_indexes = []
        col_indexes = []
        data = []

        h_matrix = self.get_matrix_H().todense().tolist()
        dangling_node = self.get_dangling_node_vector()

        for i in range(self.length):
            if dangling_node.toarray()[i][0] == 1:
                for j in range(self.length):
                    row_indexes.append(i)
                    col_indexes.append(j)
                    data.append(1 / self.length)
            else:
                for j in range(self.length):
                    row_indexes.append(i)
                    col_indexes.append(j)
                    data.append(h_matrix[i][j])

        return sparse.bsr_matrix((data, (row_indexes, col_indexes)), shape=(self.length, self.length), dtype='double')

    def cut_off_domain(self):
        urls = {page_url for page_url in self.pages}

        for purl in self.pages:
            page = self.pages[purl]
            new_outlinks = set()
            if not page.outlinks:
                continue
            else:
                # check if all outlinks are within selected domain, those that are not get cut off
                for link in page.outlinks:
                    if link in urls:
                        new_outlinks.add(link)
            page.outlinks = new_outlinks
