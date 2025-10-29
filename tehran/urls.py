from django.urls import path
from . import views

# Define app namespace
app_name = "tehran"

# URL patterns for web and API endpoints
# urlpatterns = [
#   path('', views.tehranAPIView.as_view(), name='tehran_api_view'),  # API for tasks
# ]
from django.urls import path
from .views import tehranAPIView, PredictTehranAPIView

urlpatterns = [
    path("tehran/", tehranAPIView.as_view(), name="tehran-list"),  # CRUD دیتابیس
    path(
        "predict/", PredictTehranAPIView.as_view(), name="predict-price"
    ),  # پیش‌بینی قیمت
]
