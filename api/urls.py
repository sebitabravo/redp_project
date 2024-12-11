from django.urls import path
from .views import (
    login_view,
    logout_view,
    signup_view,
    export_experiences_csv,
    experience_list,
    experience_create,
    experience_edit,
    experience_delete,
)
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, FavoriteViewSet, ExperienceViewSet

# Configuración del API
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'favorites', FavoriteViewSet)
router.register(r'experiences', ExperienceViewSet)

# Rutas del CRUD basado en HTML
urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    path('export-experiences/', export_experiences_csv, name='export_experiences'),
    path('experiences/', experience_list, name='experience_list'),
    path('experiences/create/', experience_create, name='experience_create'),
    path('experiences/edit/<int:pk>/', experience_edit, name='experience_edit'),
    path('experiences/delete/<int:pk>/',
         experience_delete, name='experience_delete'),
]

# Rutas del API
urlpatterns += router.urls
