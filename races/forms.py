from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Bet, Racer


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введіть email'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введіть ім’я користувача'
    }))

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введіть пароль'
    }))

    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Підтвердіть пароль'
    }))

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Ім’я користувача",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть ім’я користувача'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль'
        })
    )


class BetForm(forms.ModelForm):
    class Meta:
        model = Bet
        fields = ['driver', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01', 'min': '1'}),
            'driver': forms.Select(attrs={'class': 'form-select'})
        }

    def __init__(self, *args, **kwargs):
        race = kwargs.pop('race', None)
        super().__init__(*args, **kwargs)
        if race:
            from .models import RaceEntry
            self.fields['driver'].queryset = Racer.objects.filter(
                id__in=RaceEntry.objects.filter(race=race).values_list('driver_id', flat=True))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'profile_image']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваш нікнейм',
                'style': 'background-color: #f8f9fa; border-radius: 8px;',
            }),
            'profile_image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }

# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'profile_image']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control'}),
#         }


class BalanceTopUpForm(forms.Form):
    amount = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        min_value=1,
        label="Сума поповнення (₴)",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введіть суму'})
    )


class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
