from django.shortcuts import render,get_object_or_404

# Create your views here.

from .models import FlashcardSet

def index(request):
    return render(request, 'flashcard/index.html')


def card(request,cardset_id):
    #获取get请求中的参数cardset_id

    cardset = get_object_or_404(FlashcardSet, pk=cardset_id)
    cardset_title = cardset.title
    
    return render(request, 'flashcard/card.html', {'cardset_id': cardset_id,"cardset_title":cardset_title})