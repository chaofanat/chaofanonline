from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.shortcuts import render,get_object_or_404
from typing import Any


def index(request):
    

    # Number of visits to this view, as counted in the session variable.
    views_count = request.session.get('views_count', 0) 
    request.session['views_count'] = views_count + 1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'toolsindex.html',#django 默认在app的template下找html
        context={'views_count':views_count},
    )

from .forms import TTSForm
from .models import txttoaduiodata
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .toolsapi import tools_TTS as gettts
from django.http import JsonResponse

@login_required
def TTS(request,*args,**kwargs):
    #如果请求是post，则获取文本
    if request.method == "POST":
        print(request.POST)
        if len(request.POST) >= 6:
            text = request.POST.get('text')
            voicer = request.POST.get('voicer')
            speed = request.POST.get('speed')
            pitch = request.POST.get('pitch')
            volume = request.POST.get('volume')
            audio_format = request.POST.get('audio_format')
            data = txttoaduiodata.objects.create(
                text=text,
                voicer=voicer,
                speed=speed,
                pitch=pitch,
                volume=volume,
                audio_format=audio_format,
                user = request.user
            )
            #开发时设为settings.STATICFILES_DIRS[0]，生产时改为settings.STATIC_ROOT
            baseurl = settings.STATICFILES_DIRS[0]
            if not settings.DEBUG:
                baseurl = settings.STATIC_ROOT
            data.audio_url='tools/TTSaudio/' + str(data.id) + '_' +str(data.text)[:3] +'.'+{key: value for key, value in data.format_audio}[int(data.audio_format)]
            data.save()
            audio_url = os.path.join(baseurl,data.audio_url)
            try:
                gettts.get_TTspeech(text,voicer,speed,pitch,volume,audio_format,audio_url)
            except Exception as e:
                data.delete()
                return JsonResponse({'error':e})
            else:
                #图片的网络访问地址,地址开头有/，则是绝对地址，由网站项目目录开始
                #如果没有/，则是相对地址，相对于当前页面
                
                return JsonResponse({'audio_url':data.audio_url_display})
        else:
            return JsonResponse({'error':'表单错误'})
    
  
    pk = kwargs.get('pk',None)
    if pk != None:
        data = get_object_or_404(txttoaduiodata,id=pk,user=request.user)
    else:
        data = None
    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'tools/TTS.html',#django 默认在app的template下找html
        {'audioconfig':data},
    )


#导入LoginRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
class TTS_list(LoginRequiredMixin,ListView):
    model = txttoaduiodata
    template_name = 'tools/TTS_list.html'
    context_object_name = 'TTS_list'
    paginate_by = 5
    
    def get_queryset(self):
        return self.request.user.txttoaduiodata_set.all() #反向查询

import os
from django.http import HttpResponseRedirect
@login_required
def TTS_delete(request,pk):
    data = get_object_or_404(txttoaduiodata,id=pk,user=request.user)
    #检查文件是否存在
    if data.audio_url!=None:
        if settings.DEBUG:
            url = os.path.join(settings.STATICFILES_DIRS[0],data.audio_url)
        else:
            url = os.path.join(settings.STATIC_ROOT,data.audio_url)
        if os.path.exists(url):
            os.remove(url)
    data.delete()
    return HttpResponseRedirect('/tools/TTS_list/')