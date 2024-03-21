from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

from django.conf import settings
class txttoaduiodata(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = models.TextField(verbose_name="text")
    
    voicer_options = (
    (1, '度小宇'),
    (0, '度小美'),
    (3, '度逍遥（基础）'),
    (4, '度丫丫'),
    (5003, '度逍遥（精品）'),
    (5118, '度小鹿'),
    (106, '度博文'),
    (110, '度小童'),
    (111, '度小萌'),
    (103, '度米朵'),
    (5, '度小娇'),
    )

    voicer = models.IntegerField(verbose_name="配音员", choices=voicer_options, default=0)
    speed = models.IntegerField(verbose_name="语速",default=5)
    pitch = models.IntegerField(verbose_name="音调",default=5)
    volume = models.IntegerField(verbose_name="音量",default=5)

    format_audio = (
        (3, 'mp3'),
        (4, 'pcm-16k'),
        (5, 'pcm-8k'),
        (6, 'wav'),
    )
    audio_format = models.IntegerField(verbose_name="音频格式", choices=format_audio, default=3)

    #audio_url由id+user.name拼接，后缀为audio_format的值
    audio_url = models.TextField(verbose_name="音频URL",null=True)

    def __str__(self):
        return self.text
    @property
    def audio_url_display(self):
        if self.audio_url == None:
            return ''
        return '/static/'+self.audio_url          #静态资源直接访问地址
    
    @property
    def audio_format_display(self):
        return {key: value for key, value in self.format_audio}[int(self.audio_format)]
    
    @property
    def voicer_display(self):
        return {key: value for key, value in self.voicer_options}[self.voicer]
    
    class Meta:
        verbose_name = "文本转语音数据"
        verbose_name_plural = "文本转语音数据"
        ordering = ['-created_at']

    


