import csv
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import login
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Category, Experience, Favorite
from .serializers import CategorySerializer, ExperienceSerializer, FavoriteSerializer
from .forms import ExperienceForm, CommentForm, SignUpForm

# Create your views here.


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ExperienceViewSet(ModelViewSet):
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class FavoriteViewSet(ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


def home(request):
    return render(request, 'home.html')


def create_experience(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            form.save()
            # Cambia 'experience_list' por la URL de tu lista de experiencias
            return redirect('experience_list')
    else:
        form = ExperienceForm()

    return render(request, 'experience_form.html', {'form': form})


def add_comment(request, experience_id):
    experience = Experience.objects.get(id=experience_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.experience = experience
            comment.user = request.user  # Asegúrate de tener autenticación configurada
            comment.save()
            # Cambia 'experience_detail' por tu vista específica
            return redirect('experience_detail', id=experience.id)
    else:
        form = CommentForm()

    return render(request, 'comment_form.html', {'form': form, 'experience': experience})


def export_experiences_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="experiences.csv"'

    writer = csv.writer(response)
    writer.writerow(['Title', 'Category', 'Description'])

    experiences = Experience.objects.all()
    for exp in experiences:
        writer.writerow([exp.title, exp.category, exp.description])

    return response


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirigir si el usuario ya está autenticado

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Autenticar al usuario después de crearlo
                login(request, user)
                return redirect('home')
            except IntegrityError as e:
                # Manejar el error (por ejemplo, si un campo único ya existe)
                form.add_error(
                    None, "An account with this email already exists.")
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
