from django.contrib import admin
from django.urls import path, include

# urlpatterns = [
#   path('admin/', admin.site.urls),
#  path('', include('tehran.urls')),  # اضافه کردن مسیرهای app تهران
# ]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("tehran.urls")),  # مسیر app 'api'
]
