from django.shortcuts import render
from .forms import SearchForm
from PageRankApp.pagerank.src import main
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def search(request):

    def get_method(method):
        if method != '':
            print('method changed')

        if method == 'matrix':
            main.METHOD = 'matrix'
        elif method == 'power':
            main.METHOD = 'power'
        return main.METHOD

    if request.method == 'POST':
        searching_form = SearchForm(request.POST)
    else:
        searching_form = SearchForm()

    searched_exp = request.POST.get('searched_exp', '')
    crawling = request.POST.get('crawling', '')
    pagerank_method = get_method(request.POST.get('pagerank_method', ''))

    if crawling == '1':
        tmp = main.CRAWL
        main.CRAWL = True
        main.crawl_them_all()
        main.CRAWL = tmp
    pages = []
    return render(request, "search.html", {'pages': pages,
                                           'searching_form': searching_form,
                                           'searched_exp': searched_exp,
                                           'pagerank_method': pagerank_method})


def index(request):
    return render(request, 'search.html', {'': []})