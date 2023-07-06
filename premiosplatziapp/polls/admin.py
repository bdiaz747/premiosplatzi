from django.contrib import admin
from .models import Question, Choice

class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3
    

class QuestionAdmin(admin.ModelAdmin):
    fields = ["pub_date", "question_test"]
    inlines = [ChoiceInLine] 
    


admin.site.register(Question,QuestionAdmin)


