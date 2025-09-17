from django.contrib import messages

from .models import Car, Racer, Route, Race, RaceEntry, Bet, process_race_results
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, LoginForm, BetForm, ProfileUpdateForm, BalanceTopUpForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Bet


# def home(request):
#     return render(request, "index.html")


# @login_required(login_url="login")
def home(request):
    return render(request, "index.html", {"request": request})


def racers(request):
    racers_lst = Racer.objects.all()
    return render(request, "Racers.html", {"request": request, "racers_lst": racers_lst})


def cars(request):
    cars_lst = Car.objects.all()
    return render(request, "Cars.html", {"request": request, "cars_lst": cars_lst})


def routes(request):
    routes_lst = Route.objects.all()
    return render(request, "Routes.html", {"request": request, "routes_lst": routes_lst})


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # автоматичний вхід
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def race_view_detail(request):
    race_id = request.GET.get("id")
    race_obj = Race.objects.get(id=race_id)
    entries = RaceEntry.objects.filter(race=race_obj).select_related('driver', 'car')
    return render(request, "Race.html", {"race": race_obj, "entries": entries})


def races_view(request):
    races = Race.objects.all().order_by('-date_time')

    # Формуємо словник: гонка → учасники
    races_data = []
    for race_item in races:
        entries = RaceEntry.objects.filter(race=race_item).select_related('driver', 'car')
        races_data.append({
            'race': race_item,
            'entries': entries
        })

    return render(request, 'races_list.html', {'races_data': races_data})


@login_required
def place_bet_view(request, race_id):
    race = get_object_or_404(Race, id=race_id)

    if request.method == "POST":
        form = BetForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            driver_id = form.cleaned_data['driver'].id
            print(amount, driver_id)

            if Bet.objects.filter(user=request.user, race=race).exists():
                messages.error(request, "⚠️ Ви вже зробили ставку на цю гонку.")
                return redirect('races')

            driver = get_object_or_404(Racer, id=driver_id)

            if request.user.balance < float(amount):
                messages.error(request, "Недостатньо коштів на балансі.")
                return redirect('place_bet', race_id=race_id)

            # списання коштів
            request.user.balance -= amount
            request.user.save()

            # створення ставки
            Bet.objects.create(
                user=request.user,
                race=race,
                driver=driver,
                amount=amount
            )

            messages.success(request, "✅ Ставку успішно зроблено!")
            return redirect('profile')

    else:
        form = BetForm()

    return render(request, "place_bet.html", {"race": race, "form": form})


@login_required(login_url="login")
def profile_view(request):
    user = request.user
    bets = Bet.objects.select_related('race', 'driver').filter(user=user).order_by('-placed_at')

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, 'profile.html', {
        'form': form,
        'bets': bets,
    })


def car_detail(request):
    car_id = request.GET.get("id")
    car_obj = Car.objects.get(id=car_id)
    return render(request, "car_detail.html", {"car_obj": car_obj})


def racer_detail(request):
    racer_id = request.GET.get("id")
    racer_obj = Racer.objects.get(id=racer_id)
    return render(request, "racer_detail.html", {"racer_obj": racer_obj})


def route_detail(request):
    route_id = request.GET.get("id")
    route_obj = Route.objects.get(id=route_id)
    return render(request, "route_detail.html", {"route_obj": route_obj})


@login_required
def top_up_balance_view(request):
    if request.method == 'POST':
        form = BalanceTopUpForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            request.user.balance += amount
            request.user.save()
            messages.success(request, f'Баланс поповнено на {amount} ₴!')
            return redirect('profile')
    else:
        form = BalanceTopUpForm()

    return render(request, 'top_up_balance.html', {'form': form})


# views.py
from django.contrib.admin.views.decorators import staff_member_required


@staff_member_required
def finish_race_view(request, race_id):
    race = get_object_or_404(Race, id=race_id)
    process_race_results(race)
    messages.success(request, f"Гонка '{race}' завершена. Ставки оброблені.")
    return redirect('races')
