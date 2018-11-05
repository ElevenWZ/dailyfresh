from django.conf.urls import url
from apps.user import views
from user.views import RegisterView, ActiveView, LoginView
app_name = 'user'
urlpatterns = [
    # url(r'^user/', include('user')),
    url(r'^register$', RegisterView.as_view(), name='register'),
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),
    url(r'^login$', LoginView.as_view(), name='login'),


]
