from django.contrib import admin
from .models import Question, Answer

# Register your models here.


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    list_per_page = 10
    search_fields = ("question",)
    ordering = ("-created_at",)
    list_select_related = ("user",)


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("id", "question", "answer", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    list_per_page = 10
    ordering = ("-created_at",)
    list_select_related = ("question",)
