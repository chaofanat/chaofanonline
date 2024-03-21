from django.urls import path
from tools import views

urlpatterns = [
    path('', views.index, name='tools_index'),
    path('TTS/', views.TTS, name='tools_tts'),
    path('TTS/<int:pk>/', views.TTS, name='tools_ttswithpk'),
    path('TTS_list/', views.TTS_list.as_view(), name='tools_tts_list'),
    path('TTS_list_delete/<int:pk>/', views.TTS_delete, name='tools_tts_delete'),
]
