from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^validate$', views.validate),
    # url(r'^register$', views.register),
    url(r'^regvalidate$', views.regvalidate),
    # url(r'^success$', views.success),
    url(r'^quotes$', views.quotesWall),
    url(r'^quotesValidate$', views.quotesValidate),
    url(r'^quoteAddFav/(?P<id>\d+)$', views.quoteAddFav),
    url(r'^quoteRemoveFav/(?P<id>\d+)$', views.quoteRemFav),
    url(r'^users/(?P<id>\d+)$', views.userShow),
    url(r'^logout$', views.logout),
]