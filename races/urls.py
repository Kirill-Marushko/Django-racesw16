from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name="home"),
    path('cars/', views.cars, name="cars"),
    path('racers/', views.racers, name="racers"),
    path('routes/', views.routes, name="routes"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('race/', views.race_view_detail, name='race'),
    path('races/', views.races_view, name='races'),
    path('race/<int:race_id>/bet/', views.place_bet_view, name='place_bet'),
    path('profile/', views.profile_view, name='profile'),
    path('car_detail/', views.car_detail, name='car_detail'),
    path('racer_detail/', views.racer_detail, name='racer_detail'),
    path('route_detail/', views.route_detail, name='route_detail'),
    path('top_up/', views.top_up_balance_view, name='top_up_balance'),
    path('race/<int:race_id>/finish/', views.finish_race_view, name='finish_race'),

]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
