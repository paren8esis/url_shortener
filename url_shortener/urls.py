from django.conf.urls import url
from url_shortener import views


urlpatterns = [
        url(r'^$', views.index, name='index'),
        url(r'^result/$', views.result, name='result'),
        url(r'^about/$', views.about, name='about'),
]