from django.db import models
from django.contrib.auth.models import User

class FlashcardSet(models.Model):
    """
    A model representing a set of flashcards.
    """
    # Fields
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        ordering = ['title']
        unique_together = ('title', 'user')

    def __str__(self):
        return self.title

class Flashcard(models.Model):
    """
    A model representing a single flashcard.
    """
    # Fields
    id = models.AutoField(primary_key=True)
    front_content = models.CharField(max_length=255)
    back_content = models.TextField()
    cardset = models.ForeignKey(FlashcardSet, related_name='flashcards', on_delete=models.CASCADE)
    # 添加知识点掌握程度，每回答正确一次，knowledge_level加1
    knowledge_level = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        unique_together = ('front_content',  'cardset')
        ordering = ['cardset', 'knowledge_level']

    def __str__(self):
        return f"{self.front_content} -> {self.back_content}"

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flashcard_set = models.ForeignKey(FlashcardSet, on_delete=models.CASCADE)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    next_review = models.DateTimeField(null=True, blank=True)
    correct_answers = models.IntegerField(default=0)
    incorrect_answers = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    class Meta:
        unique_together = ('user', 'flashcard_set')

    def __str__(self):
        return f"Progress for {self.user.username} in {self.flashcard_set.title}"