from django.urls import path

from . import views

urlpatterns = [
    path("api/exchanges/difference/<str:code>/<int:number>/", views.DifferenceRateLastQuotations.as_view(),
         name="DifferenceRate"),
    path("api/exchanges/<str:code>/<int:number>/", views.AverageRateLastQuotations.as_view(),
         name="LastQuotations"),
    path("api/exchanges/<str:code>/<str:date>/", views.AverageRateCurrencyDate.as_view(),
         name="CurrencyDate"),
]
