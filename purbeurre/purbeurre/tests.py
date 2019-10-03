#pylint: disable=C0103, W0612
""" Python testing file checking each page returns the correct response"""
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from grocery.models import Category, Product, Favorite
from users.forms import UserRegisterForm
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

class DataFilledTestCase(TestCase):
    """ fill Category with list """
    def test_product_filled(self):
        """ Method use to fill both categories and products """
        CATEGORYNAME = [
            "Pizzas",
            "Conserves",
            "Fromages",
            "Boissons",
            "Snacks sucrés",
            "Viandes",
            "Charcuteries",
            "Epicerie",
            "Desserts",
            "Surgelés",
            "Sauces",
            "Biscuits",
            "Chocolats",
            "Gâteaux",
            "Confitures",
            "Apéritif",
            "Condiments",
            "Yaourts",
            "Pains",
            "Huiles",
        ]
        for name in CATEGORYNAME:
            categ = Category.objects.create(name=name)
        categ = Category.objects.get(name='Confitures')
        product = Product.objects.create(name='nutella', nutrigrade='a', image='url.htt',\
        url='url.htt', nutrient='url.htt', category=categ)
        products = Product.objects.all()
        self.assertTrue(products.exists)

# Homepage
class IndexPageTestCase(TestCase):
    """ Class Test that the function returns the home page with response 200 """
    def test_index_page(self):
        """ Test that the function returns the home page with response 200 """
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

# Mention page
class MentionPageTestCase(TestCase):
    """ Class Test that the function returns the mention page with response 200 """
    def test_mention_page(self):
        """ Test that the function returns the mention page with response 200 """
        response = self.client.get(reverse('mentions'))
        self.assertEqual(response.status_code, 200)

class LoginTestCase(TestCase):
    """ Class make sure the user is redirected to the homepage after login """
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')

    def test_Login(self):
        """ check status code """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('homepage'))
        self.assertEqual(response.status_code, 200)

class RegisterPageTestCase(TestCase):
    """ Class test that the function returns to the home page after registration"""
    def setUp(self):
        self.client = Client()

    def test_register_page(self):
        """ check the form """
        form_data = {'username':'john',
                     "email":'lennon@thebeatles.com',
                     "password1":'Abracadabra0',
                     'password2':'Abracadabra0'}
        form = UserRegisterForm(data=form_data)
        self.assertTrue(form.is_valid())
        response = self.client.post(reverse('register'), form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_not_register_page(self):
        """ check the response status code """
        self.user = User.objects.create_user('vic', 'vicpassword')
        self.client.login(password='johnpassword')
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)


class ResultsPageTestcase(TestCase):
    """ Class Test that the function returns the results page with response 200 """
    def setUp(self):
        categ = Category.objects.create(name='pate')
        product = Product.objects.create(name='nutella', nutrigrade='d', image='url.htt',\
        url='url.htt', nutrient='url.htt', category=categ)
        product2 = Product.objects.create(name='kiri', nutrigrade='b', image='url.htt',\
        url='url.htt', nutrient='url.htt', category=categ)
        product3 = Product.objects.create(name='boursin', nutrigrade='c', image='url.htt',\
        url='url.htt', nutrient='url.htt', category=categ)
        product4 = Product.objects.create(name='miel', nutrigrade='a', image='url.htt',\
        url='url.htt', nutrient='url.htt', category=categ)
        self.product = Product.objects.get(name='nutella')
        self.categ = categ

    def test_query_is_valid(self):
        """ must returns 200 """
        prod = Product.objects.filter(name__startswith=self.product.name).first()
        response = self.client.get(reverse('results'), {'text': 'prod'})
        self.assertEqual(response.status_code, 200)

    def test_substitute_is_better_than_product(self):
        """ test that substitures are found if better grade in same category"""
        product = Product.objects.filter(name__startswith=self.product.name).first()
        sub = Product.objects.filter\
                    (Q(category=product.category, nutrigrade='a')\
                     | Q(category=product.category, nutrigrade='b')\
                          | Q(category=product.category, nutrigrade='c'))
        response = self.client.get(reverse('results'), {'txtsearch': product.name})
        self.assertEqual(sub.count(), 3)
        self.assertEqual(response.status_code, 200)

class ProfilePageTestCase(TestCase):
    """ Class Test that the function returns the profile page with response 200"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_profile_page(self):
        """ check the response status code """
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

class DetailPageTestCase(TestCase):
    """ Create an object and its instance """
    def setUp(self):
        categ = Category.objects.create(name='pate')
        product = Product.objects.create(name='nutella', nutrigrade='a', image='url.htt',\
        url='url.htt', nutrient='url.htt', category=categ)
        self.product = Product.objects.get(name='nutella')

    # test that detail page returns 200 if the item exists
    def test_detail_page_returns_200(self):
        """ Test that the function returns the detail page with response 200 """
        product = self.product.id
        response = self.client.get(reverse('detail', args=(product,)))
        self.assertEqual(response.status_code, 200)

    # test that detail page returns 404 if the item exists
    def test_detail_page_returns_404(self):
        """ Test that the function returns the error page with response 404 """
        product = self.product.id + 1000
        response = self.client.get(reverse('detail', args=(product,)))
        self.assertEqual(response.status_code, 404)

class FavoritePageTestCase(TestCase):
    """ Ensure an item is added to a user's favorite list"""
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('Mickael', 'mickael@gmail.com', 'johnpassword')
        categ = Category.objects.create(name='pate')
        product = Product.objects.create(name='nutella', nutrigrade='a', image='url.htt',\
        url='url.htt', nutrient='url.htt', category=categ, id=5)
        self.user = User.objects.get(username="Mickael")
        self.product = Product.objects.get(name='nutella')

    def test_no_favorite_exist(self):
        """ test that template is returned although no favorite """
        self.client.login(username='Mickael', password='johnpassword')


    def test_favorite_is_added(self):
        """ Check if favorite is added """
        self.client.login(username='Mickael', password='johnpassword')
        response = self.client.get(reverse('favorite', args=(self.user.id, )))
        self.assertEqual(response.status_code, 200)

    def test_favorite_already_exists(self):
        """ check if a product is already in the table favorite """
        self.client.login(username='Mickael', password='johnpassword')
        fav = Favorite.objects.create(product=self.product, user=self.user)
        favs = Favorite.objects.filter(product=self.product, user=self.user)
        self.assertTrue(favs.exists())

class ModelTestCase(TestCase):
    """ Test string returns """

    def test_str_Category(self):
        """ test str method for the model Category """
        categ = Category.objects.create(name='Pate')
        self.assertIs(categ.__str__(), "Pate")

    def test_str_product(self):
        """ test str method for the model Product """
        categ = Category.objects.create(name='pate')
        product = Product.objects.create(name="Coca", nutrigrade='a', image='url.htt',\
        url='url.htt', nutrient='url.htt', category=categ)
        self.assertIs(product.__str__(), "Coca")


