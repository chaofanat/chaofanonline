from django.db.models.base import Model as Model

from django.shortcuts import render,get_object_or_404
from .models import Uploadnovel 
# Create your views here.


def index(request):
    

    # Number of visits to this view, as counted in the session variable.
    views_count = request.session.get('views_count', 0) 
    request.session['views_count'] = views_count + 1

    # Render the HTML template index.html with the data in the context variable
    return render(
        request,
        'index.html',#django 默认在app的template下找html
        context={'views_count':views_count},
    )




from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import View

        

from django.contrib.auth.models import User

from .forms import RegisterForm

from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

def UserCreate(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = User.objects.create_user(user_name, email, password)
            user.groups.add(1)
            user.save()
            #重定向至accounts/login页面
            return HttpResponseRedirect('/accounts/login/')
            
    else:
        form = RegisterForm()
    return render(request, 'workedit/user_form.html', {'form': form})


 

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Novel,Chapter
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class workedits(LoginRequiredMixin,generic.ListView):
    model = Novel
    context_object_name = 'workedits'
    template_name = 'workedit/workedits.html'
    paginate_by = 10

    def get_queryset(self):
        return Novel.objects.filter(enable=True,publish_enable=True)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['uploadnovels'] = Uploadnovel.objects.filter(enable=True)
        return context

class workedit_chapters(LoginRequiredMixin,generic.ListView):
    model = Chapter
    context_object_name = 'workedit_chapters'
    template_name = 'workedit/workedits_chapters.html'
    paginate_by = 10

    def get_queryset(self):
        pk = self.kwargs.get('pk',None)
        if pk:
            Queryset = Chapter.objects.filter(novel_id=Novel.objects.get(pk=pk)).filter(enable=True,publish_enable=True)
            return Queryset
        else:
            return Chapter.objects.none()
    
#detailview不应该使用查询集，应该使用单个对象
#关于参数获取，listview使用self.kwargs.get('pk',None)获取参数
#detailview使用self.kwargs['pk']或者self.kwargs.get('pk',None)获取参数
class workedit_chapter_detail(LoginRequiredMixin,generic.DetailView):
    model = Chapter
    context_object_name = 'workedit_chapter_detail'
    template_name = 'workedit/workedits_chapter_detail.html'

    
    def get_object(self, queryset=None):
        obj = Chapter.objects.get(pk=self.kwargs['chapter_pk'])
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = Novel.objects.get(pk=self.kwargs.get('pk',None))
        return context
   
from django import forms
class novel_list(LoginRequiredMixin,generic.ListView,CreateView):
    model = Novel
    fields=['title',"introduction"]
    template_name = 'workedit/novel_list.html'
    context_object_name = 'novel_list'
    paginate_by = 10
    object = None
    success_url = "#"

    #设置author为当前用户,publish_date为当前时间
    def form_valid(self, form):
        form.instance.author_id = self.request.user
        form.instance.publish_date = datetime.datetime.now()
        return super().form_valid(form)
    #rows为4，cols为50
    def get_form(self):
        form = super().get_form()
        form.fields['introduction'].widget = forms.Textarea(attrs={'rows':4,'cols':50})
        return form
    
    def get_queryset(self):
        return Novel.objects.filter(author_id=self.request.user).filter(enable=True)


class novel_list_manage(LoginRequiredMixin,generic.ListView):
    model = Novel
    context_object_name = 'novels'
    template_name = 'workedit/novel_list_manage.html'
    paginate_by = 10

    def get_queryset(self):
        return Novel.objects.filter(author_id=self.request.user).filter(enable=True)

@login_required
def novel_manage_delete(request,pk):
    Novel.objects.filter(pk=pk,enable=True,author_id=request.user).update(enable=False)
    Chapter.objects.filter(novel_id=Novel.objects.get(pk=pk,enable=True,author_id=request.user),enable=True).update(enable=False)
    return HttpResponseRedirect(reverse('novel_list_manage'))

@login_required
def novel_manage_publish(request,pk):
    Novel.objects.filter(pk=pk,enable=True,author_id=request.user).update(publish_enable=True)
    Chapter.objects.filter(novel_id=Novel.objects.get(pk=pk,enable=True,author_id=request.user),enable=True).update(publish_enable=True)
    return HttpResponseRedirect(reverse('novel_list_manage'))

@login_required
def novel_manage_nopublish(request,pk):
    Novel.objects.filter(pk=pk,enable=True,author_id=request.user).update(publish_enable=False)
    Chapter.objects.filter(novel_id=Novel.objects.get(pk=pk,enable=True,author_id=request.user),enable=True).update(publish_enable=False)
    return HttpResponseRedirect(reverse('novel_list_manage'))

class chapter_list_manage(LoginRequiredMixin,generic.ListView):
    model = Chapter
    context_object_name = 'chapters'
    template_name = 'workedit/chapter_list_manage.html'
    paginate_by = 20

    def get_queryset(self):
        pk = self.kwargs.get('pk',None)
        if pk:
            Queryset = Chapter.objects.filter(novel_id=Novel.objects.get(pk=pk)).filter(enable=True)
            return Queryset
        else:
            return Chapter.objects.none()

    
@login_required
def chapter_manage_publish(request,pk):
    #存在安全隐患，更改他人的记录
    #应增加章节所属novel的author_id与当前用户一致的条件
    if Chapter.objects.filter(pk=pk,enable=True).first().novel_id.author_id!=request.user:
        messages.info(request, '你不能发布他人的作品')
        return render(request, 'workedit/message.html')
    Chapter.objects.filter(pk=pk,enable=True).update(publish_enable=True)
    return HttpResponseRedirect(reverse('chapter_list_manage',args=[Chapter.objects.get(pk=pk,enable=True).novel_id.pk]))

@login_required
def chapter_manage_nopublish(request,pk):
    if Chapter.objects.filter(pk=pk,enable=True).first().novel_id.author_id!=request.user:
        messages.info(request, '你不能发布他人的作品')
        return render(request, 'workedit/message.html')
    Chapter.objects.filter(pk=pk,enable=True).update(publish_enable=False)
    return HttpResponseRedirect(reverse('chapter_list_manage',args=[Chapter.objects.get(pk=pk,enable=True).novel_id.pk]))





#不能使用detaiView，因为传入的是novel的pk，不是chapter的pk
#关于参数获取，listview使用self.kwargs.get('pk',None)获取参数
#detailview使用self.kwargs['pk']或者self.kwargs.get('pk',None)获取参数
from .forms import chapterdetailform
class chapter_list(LoginRequiredMixin,generic.ListView,CreateView):
    model = Chapter
    context_object_name = 'chapters'
    template_name = 'workedit/chapter_list.html'
    
    success_url = "#"
    paginate_by = 10
    object = None
    form_class = chapterdetailform

    #允许queryset为空，因为当没有chapter时，应返回一个空的列表
    def get_queryset(self):
        pk = self.kwargs.get('pk',None)
        if pk:
            Queryset = Chapter.objects.filter(novel_id=Novel.objects.get(pk=pk)).filter(enable=True)
            return Queryset
        else:
            return Chapter.objects.none()
    def form_valid(self, form):
        form.instance.novel_id = Novel.objects.get(pk=self.kwargs.get('pk',None))
        form.instance.publish_date = datetime.datetime.now()
        return super().form_valid(form)
     # 将 novel 添加到模板上下文中
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = Novel.objects.get(pk=self.kwargs.get('pk',None))
        return context
    

class chapter_detail(LoginRequiredMixin,generic.DetailView,UpdateView):
    model = Chapter
    context_object_name = 'chapter_detail'
    template_name = 'workedit/chapter_detail.html'
    
    success_url = "#"
    object = None
    form_class = chapterdetailform

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novel'] = Novel.objects.get(pk=self.kwargs.get('novel_pk',None))
        context['chapters'] = Chapter.objects.filter(novel_id=Novel.objects.get(pk=self.kwargs.get('novel_pk',None))).filter(enable=True)
        return context

class chapter_delete(LoginRequiredMixin,View):
    def dispatch(self, *args, **kwargs):
        return super(chapter_delete, self).dispatch(*args, **kwargs)
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk',None)
        novel_id = self.kwargs.get('novel_id',None)
        if pk and novel_id:
            Chapter.objects.filter(pk=pk).update(enable=False)
            return HttpResponseRedirect(reverse('chapter_list',args=[novel_id]))
        else:
            #异常
            return render(request, 'workedit/chapter_delete_confirm.html')
        


from zhipuai import ZhipuAI
from django.http import JsonResponse
import json
from .models import Aichatsession,Aichatcontent,Aiapikey
from django.contrib import messages
class AIChatView(LoginRequiredMixin,View):

   
    def dispatch(self, *args, **kwargs):
        return super(AIChatView, self).dispatch(*args, **kwargs)

    def post(self, request):
        #取得当前用户id
        user_id = request.user.id
        data = json.loads(request.body)
        user_message = data.get('message', '')
        aisession_id = data.get('aisession_id','')
        #暂时直接创建session记录,后续应和前端互动
        session_id= ''
        if aisession_id != '':
            session_id = aisession_id
        else:
            session_id = Aichatsession.objects.create(user=request.user).id
            Aichatcontent.objects.create(session=Aichatsession.objects.filter(id=session_id).first(),role='system',content='你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。')
        if Aiapikey.objects.filter(user=request.user,enable=True,key_name=AIapi.objects.filter(api_name='zhipuai').first()).count()==0  :
            return JsonResponse({'error': '请先设置AI APIKEY,并启用'}, status=400)
        if user_message:
            # 在这里调用你的AI模型来获取回复
            ai_reply = get_ai_reply(user_message,user_id,session_id)
            return JsonResponse({'reply': ai_reply})
        else:
            return JsonResponse({'error': '没有收到有效的消息'}, status=400)
    
    def get(self, request, *args, **kwargs):
        #注意get方法参数的获取方式，如果是以url带问号传参数，则使用request.GET.get('参数名',None)
        #如果以url路径传参，则使用kwargs.get('参数名',None)
        aisession_id = kwargs.get('aisession_id',None)
        if aisession_id==None:
            aisession_id = request.GET.get('aisession_id',None)
        context = {}
        aisessions = Aichatsession.objects.filter(user=request.user)
        context['aisessions'] = aisessions
        
        if(aisession_id!=None):
            aisessions_content = Aichatcontent.objects.filter(session=Aichatsession.objects.filter(id=aisession_id).first())
            context['aisession_content'] = aisessions_content
            context['aisession_id'] = aisession_id
            
        return render(request, 'workedit/ai_chat.html',context)
       
        
        
        
    
  
    


from .models import AIapi
def get_ai_reply(message,user_id,session_id):
    # 在这里调用你的AI模型来获取回复
    user = User.objects.filter(id=user_id)[0]
    apikey = Aiapikey.objects.filter(user=user,enable=True,key_name=AIapi.objects.filter(api_name='zhipuai').first())[0].key
    client = ZhipuAI(api_key=apikey) 
    Aichatcontent.objects.create(session=Aichatsession.objects.filter(id=session_id)[0],role='user',content=message)
    
    allcontent = Aichatcontent.objects.filter(session=Aichatsession.objects.filter(id=session_id)[0])
    value = []
    for content in allcontent:
        value.append({'role':content.role,'content':content.content})
    response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    # 设置一个唯一请求ID，用于记录日志
    messages=value,
    )
    result = response.choices[0].message.content
    Aichatcontent.objects.create(session=Aichatsession.objects.filter(id=session_id)[0],role='assistant',content=result)
    return result;


class myapikey(LoginRequiredMixin,CreateView,generic.ListView):
    
    model = Aiapikey
    template_name = 'workedit/ai_apikey.html'
    fields=['key_name','key']
    success_url = '#'
    context_object_name = 'apikeys'
    paginate_by = 10
    object = None
    object_list = None
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    def get_queryset(self):
        return Aiapikey.objects.filter(user=self.request.user)
    

#登录验证
from django.contrib.auth.decorators import login_required

@login_required
def new_session(request):
    aisession_id = Aichatsession.objects.create(user=request.user).id
    Aichatcontent.objects.create(session=Aichatsession.objects.filter(id=aisession_id).first(),role='system',content='你是一个乐于解答各种问题的助手，你的任务是为用户提供专业、准确、有见地的建议。')
    return HttpResponseRedirect(reverse('ai_chat')+'?aisession_id='+str(aisession_id))


def delete_aisession(request,aisession_id):
    if aisession_id:
        if Aichatsession.objects.filter(pk=aisession_id).first().user==request.user:
            Aichatsession.objects.filter(pk=aisession_id).delete()
    return HttpResponseRedirect(reverse('ai_chat'))

@login_required
def apikey_delete(request,pk):
    if Aiapikey.objects.filter(pk=pk).first().user==request.user :
        Aiapikey.objects.filter(pk=pk).delete()
    else:
        messages.info(request, '你不能删除其他人的记录')
        return render(request, 'workedit/message.html')
    return HttpResponseRedirect(reverse('ai_apikey'))



@login_required
def apikey_enable(request,pk):
    existing_record = Aiapikey.objects.filter(user=request.user, enable=True).first()
    if existing_record is not None:
        #网页提示弹窗只能有一个 enable 为 True 的记录
        messages.info(request, '只能有一个 enable 为 True 的记录')
        return render(request, 'workedit/message.html')
    Aiapikey.objects.filter(pk=pk).update(enable=True)
    return HttpResponseRedirect(reverse('ai_apikey'))

@login_required
def apikey_disable(request,pk):
    try:
        Aiapikey.objects.filter(pk=pk).update(enable=False)
    except:
        pass
    return HttpResponseRedirect(reverse('ai_apikey'))
    

class aisessions_update(LoginRequiredMixin,UpdateView):
    model = Aichatsession
    context_object_name = 'aisessions'
    template_name = 'workedit/ai_sessions_update.html'
    fields = ['session_title']


  
import os
from django.conf import settings
#txt文件上传
@login_required
def novel_upload(request):
    if request.method == 'POST':
        uploadnovels=  Uploadnovel.objects.filter(user=request.user)
        return render(request, 'workedit/novel_upload.html',{'novels':uploadnovels})
    else:
        uploadnovels=  Uploadnovel.objects.filter(user=request.user)
        return render(request, 'workedit/novel_upload.html',{'novels':uploadnovels})
    

from django.http import JsonResponse
from django.views.generic import View
import os
import hashlib

#MD5计算
def calculate_md5(file_chunk):
        md5 = hashlib.md5()
        file_chunk.seek(0)  # 重置文件块的读取位置
        while chunk := file_chunk.read(8192):
            md5.update(chunk)
        
        return md5.hexdigest()

#文件分块上传
class NovelChunkedUploadView(LoginRequiredMixin,View):
    def post(self, request):
        # 获取文件名
        file_name = request.POST.get('filename', None)

        #开发时设为settings.STATICFILES_DIRS[0]，生产时改为settings.STATIC_ROOT
        baseurl = settings.STATICFILES_DIRS[0]
        if not settings.DEBUG:
            baseurl = settings.STATIC_ROOT
        # 指定存储文件块的目录
        chunk_dir = os.path.join(baseurl, 'workedit','uploadednovels',str(request.user.id),file_name)
        if not os.path.exists(chunk_dir):
            os.makedirs(chunk_dir)

        # 获取文件块数据
        file_chunk = request.FILES['file']


        # 计算文件块的MD5哈希值
        calculated_hash = calculate_md5(file_chunk)

        # 获取文件的MD5哈希值
        file_hash = request.POST['hash']
        if calculated_hash != file_hash:
            return JsonResponse({'success': False})
        
        # 获取当前文件块的索引
        current_chunk = int(request.POST['chunk'])
        
        # 获取文件块的总数
        total_chunks = int(request.POST['chunks'])
        
        # 将文件块保存到指定目录
        file_path = os.path.join(chunk_dir, f'chunk_{current_chunk}')
        with open(file_path, 'wb') as f:
            file_chunk.seek(0)
            f.write(file_chunk.read())
        
        # 如果所有文件块都已接收，则合并文件,并且将文件路径存储至数据库
        if current_chunk == total_chunks - 1:
            merged_file_path = os.path.join(chunk_dir, file_name+'.json')
            with open(merged_file_path, 'wb') as merged_file:
                for i in range(total_chunks):
                    chunk_path = os.path.join(chunk_dir, f'chunk_{i}')
                    with open(chunk_path, 'rb') as chunk_file:
                        merged_file.write(chunk_file.read())
                        chunk_file.close()
                        os.remove(chunk_path)  # 删除临时文件块
            #将文件相对路径存储至数据库
            if Uploadnovel.objects.filter(file_path=merged_file_path).first()==None:     
                Uploadnovel.objects.create(file_name=file_name,file_path=merged_file_path.split(baseurl+'\\')[1],user=request.user)
            
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': True})
        

@login_required
def uploadnovel_read(request,pk):
    obj = get_object_or_404(Uploadnovel,pk=pk)
    uploadnovel_url =  obj.source_url
    uploadnovel_url =  uploadnovel_url.replace('\\','/')
    return render(request, 'workedit/uploadnovel_read.html',{'uploadnovel_url':uploadnovel_url})
