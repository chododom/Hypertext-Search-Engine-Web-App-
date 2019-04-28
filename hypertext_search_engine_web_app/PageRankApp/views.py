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

    def get_homepage(page):
        if page != '':
            main.HOMEPAGE = page
        return main.HOMEPAGE

    def get_alpha(a):
        if a != '':
            print(a)
            main.ALPHA = float(a)
        return main.ALPHA

    def get_thread_cnt(a):
        if a != '':
            print(a)
            main.THREAD_CNT = int(a)
        return main.THREAD_CNT

    def get_page_cnt(a):
        if a != '':
            print(a)
            main.PAGE_CNT = int(a)
        return main.PAGE_CNT

    def get_iter_cnt(a):
        if a != '':
            print(a)
            main.ITERATION_CNT = int(a)
        return main.ITERATION_CNT

    if request.method == 'POST':
        searching_form = SearchForm(request.POST)
    else:
        searching_form = SearchForm()

    searched_exp = get_search_expr(request.POST.get('searched_exp', ''))
    crawling = request.POST.get('crawling', '')
    searching = request.POST.get('searching', '')
    pagerank_method = get_method(request.POST.get('pagerank_method', ''))
    alpha = get_alpha(request.POST.get('alpha', ''))
    thread_cnt = get_thread_cnt(request.POST.get('thread_cnt', ''))
    page_cnt = get_page_cnt(request.POST.get('page_cnt', ''))
    iter_cnt = get_iter_cnt(request.POST.get('iter_cnt', ''))
    homepage = get_homepage(request.POST.get('homepage', ''))

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

    return render(request, "search.html", {'pages': pages,
                                           'homepage': homepage,
                                           'alpha': alpha,
                                           'searching_form': searching_form,
                                           'searched_exp': searched_exp,
                                           'pagerank_method': pagerank_method,
                                           'thread_cnt': thread_cnt,
                                           'page_cnt': page_cnt,
                                           'iter_cnt': iter_cnt})


def index(request):
    return render(request, 'search.html', {'': []})
