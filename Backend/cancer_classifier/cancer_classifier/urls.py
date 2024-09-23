from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.upload_image, name='upload_image'),  # Image upload route
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
