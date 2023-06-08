"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path

from . import views

app_name = 'recipes'
urlpatterns = [
    path('',
         views.RecipeListViewHome.as_view(),
         name='home'),  # home
    path('recipes/search/',
         views.RecipeListViewSearch.as_view(),
         name='search'),  # recipe
    path('recipes/tags/<slug:slug>/',
         views.RecipeListViewTag.as_view(),
         name='tag'),  # recipe|tag
    path('recipes/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(),
         name='category'),  # recipe
    path('recipes/<int:pk>/',
         views.RecipeDetail.as_view(),
         name='recipe'),  # recipe
    path('recipes/api/v1/',
         views.RecipeListViewHomeApi.as_view(),
         name='recipe_api_v1'),  # home API
    path('recipes/api/v1/<int:pk>/',
         views.RecipeDetailAPI.as_view(),
         name='recipe_api_v1_detail'),  # detail API
    path('recipes/theory/',
         views.theory,
         name='theory'),  # theory
]
