from django.db import models

#导入django user 表
from django.contrib.auth.models import User
# Create your models here.


from ckeditor.fields import RichTextField
 
class QAmodel(models.Model):
    content = RichTextField(verbose_name='正文内容',config_name='default')
 #config_name指定ckeditor配置文件，不指定就使用default
    

# 小说ID (novel_id): 整型，主键
# 标题 (title): 字符串
# 作者ID (author_id): 整型，外键 (连接到用户表的用户ID)
# 发布日期 (publish_date): 日期时间型
# 状态 (status): 字符串 (例如，连载中，已完成等)
#小说表

class Novel(models.Model):
    novel_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100,default='取一个高端大气的小说名吧',verbose_name='作品名 ')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE)
    publish_date = models.DateTimeField(auto_now=True)
    introduction = models.CharField(max_length=200,default='我们的征途是诸天万界！',null=True,verbose_name='简介')
    status_choice =(
        ('r', '连载中'),
        ('f', '已完成'),
    )

    status = models.CharField(max_length=1, choices=status_choice,default='r')
    enable = models.BooleanField(default=True)
    renew_time = models.DateTimeField(auto_now=True,verbose_name='最后一次更新时间')
    publish_enable = models.BooleanField(default=False)
    base_novel = models.IntegerField(default=0)

    @property
    def base_novel_titile(self):
        if self.base_novel == 0:
            return '无'
        else:
            return Uploadnovel.objects.get(id=self.base_novel).file_name
        
    @property
    def status_display(self):
        if self.status == 'r':
            return '连载中'
        elif self.status == 'f':
            return '已完成'
        
    @property
    def woredit_class(self):
        return '原创'

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-publish_date']


# 章节ID (chapter_id): 整型，主键
# 小说ID (novel_id): 整型，外键 (连接到小说表的小说ID)
# 标题 (title): 字符串
# 内容 (content): 文本
# 发布日期 (publish_date): 日期时间型
#章节表
from markdownx.models import MarkdownxField
class Chapter(models.Model):
    chapter_id = models.AutoField(primary_key=True)
    novel_id = models.ForeignKey("Novel", on_delete=models.CASCADE)
    title = models.CharField(max_length=100,verbose_name='章节名',default='这章叫什么好呢？')
    content = MarkdownxField(verbose_name='正文',default='此处是正文。。。。从前有座山，山里有座庙。。。。（支持markdown语法哦）')
    publish_date = models.DateTimeField()
    enable = models.BooleanField(default=True)
    renew_time = models.DateTimeField(auto_now=True,verbose_name='最后一次更新时间')
    publish_enable = models.BooleanField(default=False,verbose_name='是否发布')

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['chapter_id']

from django.urls import reverse
class Aichatsession(models.Model):
    id = models.AutoField(primary_key=True)
    session_title = models.CharField(max_length=20,default='默认标题')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.session_title
    class Meta:
        ordering = ['-create_time']

    def get_absolute_url(self):
        return reverse("ai_chat_withvalue", kwargs={"aisession_id": self.pk})
    
class Aichatcontent(models.Model):
    id = models.AutoField(primary_key=True)
    session = models.ForeignKey("Aichatsession", on_delete=models.CASCADE)
    role = models.CharField(max_length=10)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.role + ':' + self.content
    class Meta:
        ordering = ['create_time']

from django.db import IntegrityError
class Aiapikey(models.Model):
    id = models.AutoField(primary_key=True)
    key_name = models.ForeignKey("AIapi", verbose_name='api名称', on_delete=models.CASCADE,to_field='api_name')
    key = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=False)

    def __str__(self):
        return self.key
    class Meta:
        ordering = ['-create_time']
        unique_together = ('key','key_name')

    def save(self, *args, **kwargs):
        # 检查是否已经有一个 enable 为 True 的记录存在
        if self.enable==True:
            
            existing_record = Aiapikey.objects.filter(user=self.user, enable=True).first()
            if existing_record is not None:
                raise IntegrityError("只能有一个 enable 为 True 的记录")
        super().save(*args, **kwargs)
    
class AIapi(models.Model):
    id = models.AutoField(primary_key=True)
    api_name = models.CharField(max_length=20,unique=True)
    api_url = models.CharField(max_length=200,null=True)
    create_time = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=True)

    def __str__(self):
        return self.api_name
    class Meta:
        ordering = ['create_time']


from django.conf import settings
class Uploadnovel(models.Model):
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=200,null=True)
    file_path = models.CharField(max_length=200,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now=True)
    enable = models.BooleanField(default=False)
    check_result = models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.file_name
    class Meta:
        ordering = ['create_time']

    @property
    def woredit_class(self):
        return '仅个人学习研究使用，禁止转载'
    
    @property
    def source_url(self):
        if self.file_path == None:
            return ''
        return '/static/'+self.file_path
    
    @property
    def source_state(self):
        if self.enable == False and self.check_result == None:
            return '审核中'
        elif self.enable == True:
            return '审核已通过'
        elif self.check_result != None:
            return '审核未通过,请重新上传'