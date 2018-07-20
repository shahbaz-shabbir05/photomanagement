from django.conf.urls import url

from photomanagement import settings
from photomanagementapp.forms import SignInForm
from photomanagementapp.views import SignUp, IndexView, PhotosView, DeleteGalleryView, DeletePhotoView
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='home'),
    url(r'^photos/(?P<gallery_id>\d+)$', PhotosView.as_view(), name='photos'),
    url(r'^signup/$', SignUp.as_view(), name='signup'),
    url(r'^login/$', login, {
        'template_name': 'jinja2/registration/login.html',
        'authentication_form': SignInForm,
    }, name='login'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^delete/gallery/(?P<gallery_id>\d+)/$', DeleteGalleryView.as_view(), name='delete_gallery'),
    url(r'^delete/photo/(?P<photo_id>\d+)/(?P<gallery_id>\d+)$', DeletePhotoView.as_view(), name='delete_photo'),
]
