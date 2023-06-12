import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_test="¿Quien es el mejor Course Director de Platzi?", pub_date = time)
        self.assertIs(future_question.was_published_recently(), False)
               
           
    
    
