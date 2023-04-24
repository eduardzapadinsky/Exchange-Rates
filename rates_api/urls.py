from django.urls import path

from . import views

app_name = "api"
urlpatterns = [
    path("difference/<str:code>/<int:number>/", views.DifferenceRateLastQuotations.as_view(),
         name="DifferenceRate"),
    path("<str:code>/<int:number>/", views.AverageRateLastQuotations.as_view(),
         name="LastQuotations"),
    path("<str:code>/<str:date>/", views.AverageRateCurrencyDate.as_view(),
         name="CurrencyDate"),
]
