from django.urls import path

from . import views

app_name = "rates-api"
urlpatterns = [
    path("difference/<str:code>/<int:number>/", views.DifferenceRateLastQuotations.as_view(),
         name="difference-rate"),
    path("<str:code>/<int:number>/", views.AverageRateLastQuotations.as_view(),
         name="last-quotations"),
    path("<str:code>/<str:date>/", views.AverageRateCurrencyDate.as_view(),
         name="currency-date"),
]
