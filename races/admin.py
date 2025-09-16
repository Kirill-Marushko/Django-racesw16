

from django.contrib import admin
from .models import (
    Car, Racer, Route, CustomUser,
    Race, RaceEntry, Bet, process_race_results
)

# 🚗 Car
@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('title', 'model', 'release_date', 'speed', 'horse_power')
    search_fields = ('title', 'model')
    list_filter = ('model', 'release_date')


# 🏁 Racer
@admin.register(Racer)
class RacerAdmin(admin.ModelAdmin):
    list_display = ('name', 'experience', 'wins', 'age', 'country')
    search_fields = ('name', 'country', 'teams')
    list_filter = ('country', 'teams')


# 🛣️ Route
@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'difficult', 'length', 'country')
    search_fields = ('name', 'country')
    list_filter = ('difficult', 'country')


# 👤 CustomUser
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'balance', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_active')


# 🏎️ Race Entry
@admin.register(RaceEntry)
class RaceEntryAdmin(admin.ModelAdmin):
    list_display = ('race', 'driver', 'car', 'position')
    search_fields = ('race__title', 'driver__name', 'car__title')
    list_filter = ('race',)


# 🎯 Race + обробка виграшів
@admin.register(Race)
class RaceAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_time', 'route_id', 'winner')
    search_fields = ('title', 'route_id__name')
    list_filter = ('route_id', 'date_time')
    actions = ['process_results']

    def process_results(self, request, queryset):
        for race in queryset:
            process_race_results(race)
        self.message_user(request, "✅ Результати оброблено.")
    process_results.short_description = "🎯 Обробити ставки та виграші"


# 💰 Bet
@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'race', 'driver', 'amount', 'is_win', 'is_paid', 'placed_at')
    list_filter = ('is_win', 'is_paid', 'race')
    search_fields = ('user__username', 'driver__name', 'race__title')
    readonly_fields = ('placed_at',)


