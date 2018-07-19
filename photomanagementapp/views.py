from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from photomanagementapp.forms import SignUpForm, GalleryCreationForm, UploadPhotoForm
from photomanagementapp.models import Gallery, Photo


class SignUp(generic.CreateView):
    form_class = SignUpForm
    # success_url = reverse_lazy('login')
    template_name = 'signup.html'

    def post(self, request, **kwargs):
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('home')
        else:
            form = SignUpForm()
        return render(request, 'signup.html', {'form': form})


class IndexView(generic.TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        galleries = Gallery.objects.all()
        form = GalleryCreationForm()
        return render(request, self.template_name, {'galleries': galleries, 'form': form})

    def post(self, request):
        if request.method == 'POST':
            form = GalleryCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = GalleryCreationForm()
        return render(request, 'index.html', {'form': form})


class PhotosView(generic.TemplateView):
    template_name = 'photos.html'

    def get(self, request, *args, **kwargs):
        gallery_id = kwargs.get('gallery_id')
        photos = Photo.objects.filter(gallery_id=gallery_id)
        form = UploadPhotoForm(gallery_id=gallery_id)
        return render(request, self.template_name, {'photos': photos, 'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse('photos', args=[kwargs.get('gallery_id')]))
        form = UploadPhotoForm()
        return render(request, 'index.html', {'form': form})


class DeleteGalleryView(generic.TemplateView):

    def post(self, request, *args, **kwargs):
        gallery_id = kwargs.get('gallery_id')
        Gallery.objects.filter(id=gallery_id).first().delete()
        return redirect(reverse('home'))


class DeletePhotoView(generic.TemplateView):

    def post(self, request, *args, **kwargs):
        photo_id = kwargs.get('photo_id')
        Photo.objects.filter(id=photo_id).first().delete()
        return redirect(reverse('photos', args=[kwargs.get('gallery_id')]))
