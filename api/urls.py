from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    CategoryViewSet,
    ExperienceViewSet,
    FavoriteViewSet,
    export_experiences_csv,
    create_experience,
    add_comment,
)

# Router para los endpoints de API
router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'experiences', ExperienceViewSet)
router.register(r'favorites', FavoriteViewSet)

# Rutas adicionales (no manejadas por el router)
urlpatterns = router.urls + [
    path('export-experiences/', export_experiences_csv, name='export_experiences'),
    path('create-experience/', create_experience, name='create_experience'),
    path('add-comment/<int:experience_id>/', add_comment, name='add_comment'),
]
