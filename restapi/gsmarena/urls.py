from django.urls import path
from .views import brands_list, brand_devices, device_detail

urlpatterns = [
    path('brands/', brands_list, name='brands-list'),
    path('brands/<str:brand_id>/devices/', brand_devices, name='brand-devices'),
    path('devices/<str:device_id>/', device_detail, name='device-detail'),
]


