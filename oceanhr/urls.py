from django.contrib import admin
from django.urls import path
from recruitment import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('assess/', views.assess_candidate, name='assess_candidate'),
]
