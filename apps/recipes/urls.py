from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('api/recipes/', views.api_recipes, name='api_recipes'),
    path('api/recipes/<int:id>/', views.api_recipe_detail, name='api_recipe_detail'),
    path('client/', views.client_view, name='client'),
]
