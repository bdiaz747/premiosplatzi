import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        # Prueba para verificar el comportamiento de was_published_recently con una pregunta futura
        # Obtener la fecha y hora actual más 30 días
        time = timezone.now() + datetime.timedelta(days=30)
        # Crear una pregunta futura con el texto "¿Quien es el mejor Course Director de Platzi?" y la fecha futura
        future_question = Question(question_text="¿Quien es el mejor Course Director de Platzi?", pub_date=time)  
        # Verificar que la pregunta no haya sido publicada recientemente
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_question(self):
        # Prueba para verificar el comportamiento de was_published_recently con una pregunta en el pasado
        # Obtener la fecha y hora actual menos 1 día
        time = timezone.now() - datetime.timedelta(days=1)
        # Crear una pregunta en el pasado con el texto "¿Cuál es tu lenguaje de programación favorito?" y la fecha pasada
        past_question = Question(question_text="¿Cuál es tu lenguaje de programación favorito?", pub_date=time)
        # Verificar que la pregunta haya sido publicada recientemente
        self.assertIs(past_question.was_published_recently(), True)

    def test_was_published_recently_with_current_question(self):
        # Prueba para verificar el comportamiento de was_published_recently con una pregunta actual 
        # Obtener la fecha y hora actual
        time = timezone.now()        
        # Crear una pregunta actual con el texto "¿Estás disfrutando del clima hoy?" y la fecha actual
        current_question = Question(question_text="¿Estás disfrutando del clima hoy?", pub_date=time)        
        # Verificar que la pregunta haya sido publicada recientemente
        self.assertIs(current_question.was_published_recently(), True)

               
class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        # Realizar una solicitud GET a la vista de índix de preguntas
        response = self.client.get(reverse("polls:index"))
        # Verificar que el código de estado de la respuesta sea 200 (éxito)
        self.assertEqual(response.status_code, 200)
        # Verificar que la respuesta contenga el texto "No polls are available"
        self.assertContains(response, "No polls are avaible")
        # Verificar que el conjunto de preguntas más recientes en el contexto de la respuesta sea vacío
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

        