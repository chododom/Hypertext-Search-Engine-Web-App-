from django.shortcuts import render
from .forms import SearchForm
from PageRankApp.pagerank.src import main
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect


def redirect_view():
    response = redirect('/pagerank/')
    return response

@csrf_exempt
def search(request):

    def get_method(method):
        if method == 'matrix':
            main.METHOD = 'matrix'
        elif method == 'power':
            main.METHOD = 'power'
        return main.METHOD

    def get_search_expr(expr):
        if expr != '':
            main.SEARCH_WORD = expr
        return main.SEARCH_WORD

    def get_alpha(a):
        if a != '':
            main.ALPHA = a
        return main.ALPHA

    if request.method == 'POST':
        searching_form = SearchForm(request.POST)
    else:
        searching_form = SearchForm()

    searched_exp = get_search_expr(request.POST.get('searched_exp', ''))
    crawling = request.POST.get('crawling', '')
    searching = request.POST.get('searching', '')
    pagerank_method = get_method(request.POST.get('pagerank_method', ''))
    alpha = get_alpha(request.POST.get('alpha', ''))
    pages = []

    if crawling == '1':
        tmpC = main.CRAWL
        tmpP = main.CALC_PR
        tmpI = main.INIT_SEARCH_INDEX

        main.CRAWL = True
        main.CALC_PR = True
        main.INIT_SEARCH_INDEX = True

        main.crawl_them_all()

        main.CRAWL = tmpC
        main.CALC_PR = tmpP
        main.INIT_SEARCH_INDEX = tmpI

    if searching == '1':
        tmpS = main.SEARCH
        main.SEARCH = True

        pages = main.search_them_all()

        main.SEARCH = tmpS

    print(pages)
    return render(request, "search.html", {'pages': pages,
                                           'alpha': alpha,
                                           'searching_form': searching_form,
                                           'searched_exp': searched_exp,
                                           'pagerank_method': pagerank_method})


def index(request):
    return render(request, 'search.html', {'': []})
