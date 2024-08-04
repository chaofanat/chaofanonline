"""
URL configuration for ChaoFanOnline project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,re_path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Use include() to add paths from the catalog application
from django.conf.urls import include
from django.urls import path
#add workedit app
urlpatterns += [
    path('workedit/', include('workedit.urls')),
]

#add tools app
urlpatterns += [
    path('tools/', include('tools.urls')),
]

#add markdownx
urlpatterns += [
    path('markdownx/', include('markdownx.urls')),
]

#add myblog app
urlpatterns += [
    path('myblog/', include('myblog.urls')),
]

#add metaphysics app
urlpatterns += [
    path('metaphysics/', include('metaphysics.urls')),
]

#add flashcard app
urlpatterns += [
    path('flashcard/', include('flashcard.urls')),
]

#Add URL maps to redirect the base URL to our application
#将myblog应用作为域名访问的主页
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/myblog/')),
]


# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
else:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#添加media文件访问

from django.views.static import serve
if settings.DEBUG:
   
    urlpatterns +=re_path('media/(?P<path>.*)', serve,{'document_root': settings.STATICFILES_DIRS[1]}),
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.STATICFILES_DIRS[1])
else:
    urlpatterns +=re_path('media/(?P<path>.*)', serve,{'document_root': settings.MEDIA_ROOT}),
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.conf.urls import include
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]


#ninjia api
from .api import api
urlpatterns += [
    path('api/', api.urls),
]