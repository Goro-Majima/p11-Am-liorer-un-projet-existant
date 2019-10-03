"""purbeurre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path, include, re_path
from . import views
from users import views as user_views

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', views.homepage, name='homepage'),
    re_path(r'^mentions/', views.mentions, name='mentions'),
    re_path(r'^grocery/', include('grocery.urls')),
    re_path(r'^results/', views.results, name='results'),
    re_path(r'^detail/(?P<substitute_id>\w+)/$', views.detail, name='detail'),
    re_path(r'^mentions/', views.mentions, name='mentions'),
    re_path(r'^favorite/(?P<user_name>\w+)/$', views.favorite, name='favorite'),
    re_path(r'^ajax_calls/search/', views.autocomplete_model, name='autocomplete'),
    re_path(r'^register/', user_views.register, name='register'),
    re_path(r'^profile/', user_views.profile, name='profile'),
    re_path(r'^login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    re_path(r'^logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
