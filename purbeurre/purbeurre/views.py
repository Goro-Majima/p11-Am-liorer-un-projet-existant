#pylint: disable=C0103
""" Python file that manage Users input, database search and redirect to the templates """
import json
import urllib

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User

from grocery.models import Product, Favorite

def homepage(request):
    """ return the home page """
    return render(request, 'grocery/home.html')

def mentions(request):
    """ return the mention page """
    return render(request, 'grocery/mentions.html')

def results(request):
    """ get input from user, search the input in the database and display substitutes"""
    if request.method == 'GET':
        text = 'txtSearch'
        # product = Product.objects.filter(name__startswith=text).first()
        product = Product.objects.filter(name=text).first()
        if not product:
            messages.warning(request, f'veuillez effectuer une autre recherche !')
            return render(request, 'grocery/home.html')
        elif product.nutrigrade == 'a':
            substitute_list = []
        else:
            if product.nutrigrade == 'b':
                substitute_queries = Product.objects.filter\
                    (category=product.category, nutrigrade='a')
            elif product.nutrigrade == 'c':
                substitute_queries = Product.objects.filter\
                    (Q(category=product.category, nutrigrade='a')\
                     | Q(category=product.category, nutrigrade='b'))
            else:
                substitute_queries = Product.objects.filter\
                    (Q(category=product.category, nutrigrade='a')\
                     | Q(category=product.category, nutrigrade='b')\
                          | Q(category=product.category, nutrigrade='c'))
            paginator = Paginator(substitute_queries, 6)
            page = request.GET.get('page')
            try:
                substitute_list = paginator.page(page)
            except PageNotAnInteger:
                substitute_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                substitute_list = paginator.page(paginator.num_pages)
        context = {
            'product_name': product.name,
            'product_image': product.image,
            'product_nutrigrade': product.nutrigrade,
            'product_nutrient': product.nutrient,
            'product_url': product.url,
            'product_id': product.id,
            'sub_list': substitute_list,
            'paginate': True,
            'text':urllib.parse.quote_plus(text)
        }
    return render(request, 'grocery/results.html', context)

def detail(request, substitute_id):
    """ Return the detail page when item clicked on """
    # substitute = Product.objects.get(id=substitute_id)
    substitute = get_object_or_404(Product, pk=substitute_id)
    context = {
        'substitute_name': substitute.name,
        'substitute_image': substitute.image,
        'substitute_nutrigrade': substitute.nutrigrade,
        'substitute_nutrient': substitute.nutrient,
        'substitute_url': substitute.url,
        'substitute_id': substitute.id,
    }
    return render(request, 'grocery/detail.html', context)

@login_required
def favorite(request, user_name):
    """ Return the favorite page with all saved items of a logged user"""
    if request.method == 'POST':
        product = request.POST.get('substitute')
        myproduct = Product.objects.get(id=product)
        favorites = Favorite.objects.filter(product=myproduct, user=request.user)
        if favorites.exists():
            messages.success(request, f'Ce produit est déjà dans vos favoris !')
        else:
            favorites = Favorite.objects.create(product=myproduct, user=request.user)
            favorites.save()
            messages.success(request, f'Ce produit a été ajouté à vos favoris !')
    addfavorite = Favorite.objects.filter(user=request.user)
    if addfavorite != []:
        paginator = Paginator(addfavorite, 6)
        page = request.GET.get('page')
        try:
            addedfavorite = paginator.page(page)
        except PageNotAnInteger:
            addedfavorite = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            addedfavorite = paginator.page(paginator.num_pages)
        context = {
            'paginate': True,
            'added_favorite': addedfavorite
        }
    else:
        context = {
            'added_favorite': addfavorite
        }
    return render(request, 'grocery/favorite.html', context)

def autocomplete_model(request):
    """ Display items from the first two letters of user input in autocompletion """
    if request.is_ajax():
        item = request.GET.get('term', '').capitalize()
        search_qs = Product.objects.filter(name__startswith=item)
        result = []
        for req in search_qs:
            result.append(req.name)
        data = json.dumps(result)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
