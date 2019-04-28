class Page:
    id = -1
    page_url = ''
    text_content = ''
    rank = 0
    # set of IDs of pages linking to self
    inlinks = set()
    # set of IDs of pages self links to
    outlinks = set()

    def __init__(self, id, page_url, text_content, outlinks):
        self.id = id
        self.page_url = page_url
        self.text_content = text_content
        self.outlinks = outlinks

    def __str__(self):
        return "PR = "+str(self.rank)+"\t| "+self.page_url

    def __lt__(self, other):
        return self.id < other.id

    def __le__(self, other):
        return self.id <= other.id

    def __eq__(self, other):
        return self.id == other.id

    def __ge__(self, other):
        return self.id >= other.id

    def __gt__(self, other):
        return self.id > other.id

    def __ne__(self, other):
        return self.id != other.id
