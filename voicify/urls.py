"""voicify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website.views import welcome, about,download_mp3,download_mp3_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome,name="welcome"),
    path('about',about,name="about"),
    path("download_mp3",download_mp3,name="download_mp3"),
    path('mp3/<str:file_name>',download_mp3,name="download_mp3"),
]

#urlpatterns+=static(settings.STATIC_URL,  document_root=settings.STATIC_ROOT)
