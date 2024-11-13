from django.contrib.auth.decorators import login_required
from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('list/', login_required(views.DeviceList.as_view()), name='device_list'),
    path('', views.home_page, name='home_page'),
    path('find_sensor/<str:mac_addr>', views.get_sensor_page, name='get_sensor_page'),

    path('relay/<int:relay_id>', views.RelayDetail.as_view()),
    path('add_relay/', views.add_relay),

    path('dh11/<int:dh11_id>', views.Dh11Detail.as_view(), name='dh11_detail'),
    path('add_dh11/', views.add_dh11),
]
