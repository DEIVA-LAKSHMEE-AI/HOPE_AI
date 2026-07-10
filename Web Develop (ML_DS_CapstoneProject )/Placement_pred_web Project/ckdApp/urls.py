from django.urls import path
from . import views

app_name = 'ckdApp'

urlpatterns = [
    path('', views.dataUploadView.as_view(), name='ckd'),
]
