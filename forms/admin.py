from django.contrib import admin
from .models import Form, Question, Response, Answer


@admin.register(Form)
class FormAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question_type', 'form')
    list_filter = ('question_type', 'form')
    search_fields = ('text',)

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('form', 'created_at')
    list_filter = ('form', 'created_at')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('response', 'question', 'answer_text')
    list_filter = ('question',)
