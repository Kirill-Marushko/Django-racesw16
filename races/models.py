from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings


class Car(models.Model):
    title = models.CharField(max_length=50)
    img = models.ImageField(upload_to="Django_races/media")
    speed = models.FloatField()
    weight = models.FloatField()
    model = models.CharField(max_length=50)
    release_date = models.FloatField()
    horse_power = models.FloatField()
    participation_in_races = models.CharField(max_length=100)
    acceleration_from_0_to_100 = models.FloatField()

    def __str__(self):
        return self.title


class Racer(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to="Django_races/media")
    experience = models.FloatField()
    wins = models.FloatField()
    age = models.FloatField()
    family = models.CharField(max_length=50)
    places_of_participation = models.CharField(max_length=100)
    teams = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Route(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(upload_to="Django_races/media")
    difficult = models.CharField(max_length=50)
    length = models.FloatField()
    year_of_manufacture = models.FloatField()
    number_of_turns = models.FloatField()
    number_of_sectors = models.FloatField()
    what_races_are_held = models.CharField(max_length=100)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    profile_image = models.ImageField(upload_to='profile_images/', default='default.png')

    def __str__(self):
        return self.username


class Race(models.Model):
    title = models.CharField(max_length=50)
    route_id = models.ForeignKey(Route, on_delete=models.CASCADE)
    winner = models.ForeignKey(Racer, on_delete=models.SET_NULL, null=True, blank=True)
    date_time = models.DateTimeField()
    participants = models.ManyToManyField(
        Racer,
        through='RaceEntry',
        related_name='races'
    )

    def is_finished(self):
        return self.winner is not None

    def __str__(self):
        return f"Race at {self.route_id.name} on {self.date_time.strftime('%Y-%m-%d %H:%M')}"


class RaceEntry(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE)
    driver = models.ForeignKey(Racer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    position = models.PositiveIntegerField(null=True, blank=True, help_text="Фінішна позиція")

    class Meta:
        unique_together = ('race', 'driver')

    def __str__(self):
        return f"{self.driver} in {self.car} at {self.race}"


class Bet(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    race = models.ForeignKey('Race', on_delete=models.CASCADE)
    driver = models.ForeignKey('Racer', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    placed_at = models.DateTimeField(auto_now_add=True)
    is_win = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'race')  # Один користувач — одна ставка на гонку

    def __str__(self):
        return f"{self.user.username} — {self.driver} ({self.amount} грн)"


def process_race_results(race):
    if not race.is_finished():
        return

    winning_driver = race.winner
    bets = Bet.objects.filter(race=race, is_paid=False)

    for bet in bets:
        if bet.driver == winning_driver:
            bet.is_win = True
            # виграш x2
            bet.user.balance += bet.amount * 2
            bet.user.save()
        else:
            bet.is_win = False

        bet.is_paid = True
        bet.save()
