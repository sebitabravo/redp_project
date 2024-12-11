from django import forms
from .models import Experience, Comment, User  # Importa el modelo personalizado


class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'category', 'description',
                  'rating', 'additional_info']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'additional_info': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter additional information as plain text'
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Add a comment...'}),
        }


class SignUpForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User  # Utiliza tu modelo de usuario personalizado
        fields = ['name', 'email']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Llama al constructor base de forms.Form
        for field_name in self.fields:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
