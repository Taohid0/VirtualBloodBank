from django.conf.urls import include,url
from bloodBank import views
urlpatterns = [
    url(r"^$",views.blood_view_class.as_view())
]