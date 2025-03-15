from django.urls import path
from . import views
app_name = "nfactorial"
urlpatterns = [
    path("",views.index,name="index"),
    path("<int:first>/add/<int:second>/",views.add,name="add"),
    path("transform/<str:text>/",views.transform,name="transform"),
]