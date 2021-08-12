from django.contrib import admin

from .models import Question, Answer, Like

# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = 'title', 'author', 'created'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = 'question', 'author', 'value'


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = 'question', 'author', 'value'

