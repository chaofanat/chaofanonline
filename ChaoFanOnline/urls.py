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


#增加csrftoken获取接口
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def get_csrf_token(request):
    """
    获取CSRF令牌的函数。

    该函数用于在用户成功提供凭据后生成CSRF令牌。这样做可以确保后续请求具有有效的CSRF保护，
    从而增加应用的安全性。

    参数:
    - request: HTTP请求对象，用于判断请求方法并获取请求数据。

    返回:
    - 如果凭据验证成功，返回包含CSRF令牌的JSON响应。
    - 如果凭据验证失败，返回包含错误信息的JSON响应。
    - 如果请求方法不是POST，返回错误信息。
    """
    # 限制只有POST方法的请求
    if request.method == 'POST':
        # 从请求中获取用户名和密码
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户名和密码是否正确
        if username and password:
            # 尝试使用提供的用户名和密码验证用户
            user = authenticate(username=username, password=password)
            if user:
                # 用户验证成功后，生成csrftoken
                csrftoken = get_token(request)
                # 返回包含csrftoken的JSON响应
                return JsonResponse({'csrftoken': csrftoken})
            else:
                # 验证失败，返回错误信息
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        else:
            # 缺少用户名或密码，返回错误信息
            return JsonResponse({'error': 'Missing usernameor password'}, status=400)
    else:
        # 不是POST方法，返回错误信息
        return JsonResponse({'error': 'Invalid request method'}, status=405)
        
urlpatterns += [
    path('get_csrf_token/', get_csrf_token,name='get_csrf_token'),
]



    