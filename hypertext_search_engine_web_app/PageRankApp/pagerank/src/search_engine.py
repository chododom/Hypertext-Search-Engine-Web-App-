import os
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
from whoosh.index import create_in
from whoosh.fields import Schema, TEXT, ID

from PageRankApp.pagerank.src.config import *


class Result:
    page_url = ""
    page_rank = 0
    normalized_page_rank = 0
    content_rank = 0
    normalized_content_rank = 0
    combined_rank = 0

    def __init__(self, url, rank):
        self.page_url = url
        self.content_rank = rank

    def __str__(self):
        return str(self.combined_rank) + " - " + self.page_url


def createSearchableData(root):
    schema = Schema(title=TEXT(stored=True), id=ID(stored=True), textcontent=TEXT(stored=True))
    if not os.path.exists(PARENT_DIR + "indexdir"):
        os.mkdir(PARENT_DIR + "indexdir")

    # Creating an index writer to add document as per schema
    ix = create_in(PARENT_DIR + "indexdir", schema)
    writer = ix.writer()

    filepaths = [os.path.join(root, i) for i in os.listdir(root)]
    for path in filepaths:
        try:
            fp = open(path, 'r', encoding="utf-8")
            text = fp.read()
            writer.add_document(title=path.split("\\")[1], id=path, textcontent=text)
            fp.close()
        except:
            print("Error: " + path)
    writer.commit()


def search(query_str, topN):
    ret = []
    ix = open_dir(PARENT_DIR + "indexdir")
    with ix.searcher() as searcher:
        query = QueryParser("textcontent", ix.schema).parse(query_str)
        results = searcher.search(query, limit=None)
        if results.is_empty():
            print("No results for query '" + query_str + "'.")
        else:
            for i in range(topN if len(results) > topN else len(results)):
                # print(results[i]['title'], str(results[i].score), results[i]['id'])
                with open(PARENT_DIR + "page_contents/" + str(results[i]['title']), mode="r", encoding="utf-8") as fp:
                    url = fp.readline()
                ret.append(Result(url.strip(), results[i].score))
    return ret
