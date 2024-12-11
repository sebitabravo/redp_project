import csv
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db import IntegrityError
from .models import Category, Experience, Favorite, User
from .serializers import CategorySerializer, ExperienceSerializer, FavoriteSerializer
from .forms import ExperienceForm, CommentForm, SignUpForm, LoginForm

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
    # Configurar la respuesta HTTP para un archivo CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="experiences.csv"'

    # Crear un escritor CSV
    writer = csv.writer(response)
    writer.writerow(['Title', 'Category', 'Description',
                    'Rating', 'Additional Info', 'User'])

    # Consultar las experiencias y escribirlas en el archivo
    experiences = Experience.objects.all()
    for exp in experiences:
        writer.writerow([
            exp.title,
            exp.get_category_display(),  # Si prefieres el nombre legible de la categoría
            exp.description,
            exp.rating,
            exp.additional_info if exp.additional_info else 'N/A',
            exp.user.email if exp.user else 'No User'
        ])

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


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = get_object_or_404(User, email=email)
            if user.check_password(password):  # Verifica la contraseña
                if user.is_active:
                    login(request, user)  # Inicia la sesión
                    return redirect('experience_list')  # Redirige al CRUD
                else:
                    return render(request, 'login.html', {'form': form, 'error': 'User account is inactive'})
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirige al login después de cerrar sesión


@login_required
def experience_list(request):
    # Solo experiencias del usuario autenticado
    experiences = Experience.objects.filter(user=request.user)
    return render(request, 'experience_list.html', {'experiences': experiences})


@login_required
def experience_create(request):
    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)
            experience.user = request.user
            experience.save()
            return redirect('experience_list')
    else:
        form = ExperienceForm()
    return render(request, 'experience_form.html', {'form': form})


@login_required
def experience_edit(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == 'POST':
        form = ExperienceForm(request.POST, instance=experience)
        if form.is_valid():
            form.save()
            return redirect('experience_list')
    else:
        form = ExperienceForm(instance=experience)
    return render(request, 'experience_form.html', {'form': form})


@login_required
def experience_delete(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    experience.delete()
    return redirect('experience_list')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al login después del registro
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})
