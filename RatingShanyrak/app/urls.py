from django.urls import path
from .views import (
    login_view, logout_view, home_view,
    violation_section,api_students,api_violations,reward_section,my_acts_view,act_pdf_view,shanyrak_stats
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('section/violation/', violation_section, name='violation-section'),
    path('api/students/', api_students, name='api-students'),
    path('api/violations/', api_violations, name='api-violations'),
    path('section/reward/', reward_section, name='reward-section'),
    path('my-acts/', my_acts_view, name='my-acts'),
    path('act/<int:id>/pdf/', act_pdf_view, name='act-pdf'),
    path('shanyrak-stats/', shanyrak_stats, name='shanyrak-stats'),


]
