from django.contrib import admin
from django.urls import path
from recruitment import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dashboard, name='dashboard'),
    path('assess/', views.assess_candidate, name='assess_candidate'),
    path(
        'assessments/<int:assessment_id>/',
        views.assessment_detail,
        name='assessment_detail',
    ),
]
