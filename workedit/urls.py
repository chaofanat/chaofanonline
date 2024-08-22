from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # path('user/register/', views.UserCreate, name='register'),
    path('workedit/', views.workedits.as_view(), name='workedit'),
    path('workedit/<int:pk>/', views.workedit_chapters.as_view(), name='workedit_chapters'),
    path('workedit/<int:pk>/<int:chapter_pk>/', views.workedit_chapter_detail.as_view(), name='workedit_chapter_detail'),
    path('novel_list/', views.novel_list.as_view(), name='novel_list'),
    path('novel/<int:pk>/', views.chapter_list.as_view(), name='chapter_list'),
    path('novel_list_manage/', views.novel_list_manage.as_view(), name='novel_list_manage'),
    path('novel_manage_publish/<int:pk>/', views.novel_manage_publish, name='novel_manage_publish'),
    path('novel_manage_nopublish/<int:pk>/', views.novel_manage_nopublish, name='novel_manage_nopublish'),
    path('novel_manage_delete/<int:pk>/', views.novel_manage_delete, name='novel_manage_delete'),
    path('chapter_list_manage/<int:pk>/', views.chapter_list_manage.as_view(), name='chapter_list_manage'),
    path('chapter_manage_publish/<int:pk>/', views.chapter_manage_publish, name='chapter_manage_publish'),
    path('chapter_manage_nopublish/<int:pk>/', views.chapter_manage_nopublish, name='chapter_manage_nopublish'),
    #chapter_detail
    path('novel/<int:novel_pk>/<int:pk>/', views.chapter_detail.as_view(), name='chapter_detail'),
    path('delete/<int:novel_id>/<int:pk>',views.chapter_delete.as_view(), name='chapter_delete'),
    #aichat
    path('chat/', views.AIChatView.as_view(), name='ai_chat'),
    path('chat/<int:aisession_id>', views.AIChatView.as_view(), name='ai_chat_withvalue'),
    path('chat_newsession/', views.new_session, name='new_session'),
    path('chat_deletesession/<int:aisession_id>/', views.delete_aisession, name='delete_session'),
    #由于使用默认的updateview, 需要提供pk参数, 故参数名称为pk
    path('chat_updatesession/<int:pk>/', views.aisessions_update.as_view(), name='update_session'),
    path('chat_api/', views.myapikey.as_view(), name='ai_apikey'),
    path('apikey/<int:pk>/enable',views.apikey_enable, name='apikey_enable'),
    path('apikey/<int:pk>/disable',views.apikey_disable, name='apikey_disable'),
    path('apikey/<int:pk>/delete',views.apikey_delete, name='apikey_delete'),
    #noveltxt上传
    path('novel_upload/', views.novel_upload, name='novel_upload'),
    path('novel_upload_chunked/', views.NovelChunkedUploadView.as_view(), name='novel_upload_chunked'),
    #uploadnovel_read
    path('uploadnovel_read/<int:pk>', views.uploadnovel_read, name='uploadnovel_read'),



]
from django.conf.urls import include
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += [
    path('markdownx/', include('markdownx.urls')),
]