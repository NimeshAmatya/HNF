from django.urls import path

from . import views

from django.conf.urls.static import static

from django.conf import settings

app_name = "FMS"

urlpatterns = [
    path('index/', views.index, name='index'),
    path('index/predict', views.predict, name='predict'),
    path('upload_form/', views.upload_form, name='upload_form'),
    path('form/',views.form_list, name='form'),
    path('form/<int:pk>',views.delete_form, name='delete_form')
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

