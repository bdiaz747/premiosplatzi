from django.contrib import admin
from .models import Question, Choice

class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3
    

class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_test"]
    inlines = [ChoiceInLine]
    list_display = ("question_test", "pub_date","was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["question_test"]


admin.site.register(Question,QuestionAdmin)


