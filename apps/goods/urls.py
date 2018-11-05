from django.conf.urls import url
from apps.goods import views
app_name = 'goods'
urlpatterns = [
    # url(r'^user/', include('user')),

    url(r'^index$', views.index, name='index'),

]
