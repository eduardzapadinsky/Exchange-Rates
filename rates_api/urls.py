from django.urls import path

from . import views

urlpatterns = [
    path("api/exchanges/<str:code>/<str:date>/", views.AverageRateCurrencyDate.as_view(), name="CurrencyDate"),
]
