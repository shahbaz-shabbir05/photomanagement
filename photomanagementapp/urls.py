from django.conf.urls import url

from photomanagement import settings
from photomanagementapp.forms import SignInForm
from photomanagementapp.views import SignUp, IndexView
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^login/$', login, {
        'template_name': 'registration/login.html',
        'authentication_form': SignInForm,
    }, name='login'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]