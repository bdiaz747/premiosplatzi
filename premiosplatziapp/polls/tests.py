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
        future_question = Question(question_test="¿Quien es el mejor Course Director de Platzi?", pub_date=time)  
        # Verificar que la pregunta no haya sido publicada recientemente
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_past_question(self):
        # Prueba para verificar el comportamiento de was_published_recently con una pregunta en el pasado
        # Obtener la fecha y hora actual menos 1 día
        time = timezone.now() - datetime.timedelta(days=1)
        # Crear una pregunta en el pasado con el texto "¿Cuál es tu lenguaje de programación favorito?" y la fecha pasada
        past_question = Question(question_test="¿Cuál es tu lenguaje de programación favorito?", pub_date=time)
        # Verificar que la pregunta haya sido publicada recientemente
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_current_question(self):
        # Prueba para verificar el comportamiento de was_published_recently con una pregunta actual 
        # Obtener la fecha y hora actual
        time = timezone.now()        
        # Crear una pregunta actual con el texto "¿Es                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           tás disfrutando del clima hoy?" y la fecha actual
        current_question = Question(question_test="¿Estás disfrutando del clima hoy?", pub_date=time)        
        # Verificar que la pregunta haya sido publicada recientemente
        self.assertIs(current_question.was_published_recently(), True)
        
# Function to create a question with the given question text and number of days in the future to set as the publication date.
# Función para crear una pregunta con el texto de la pregunta y la cantidad de días en el futuro para establecer como fecha de publicación.
def create_question(question_test, days):
    # Calculate the time in the future based on the current time and the provided number of days.
    # Calcular el tiempo en el futuro basado en la hora actual y la cantidad de días proporcionada.
    time = timezone.now() + datetime.timedelta(days=days)
    # Create a new Question object with the given question text and the calculated publication date.
    # Crear un nuevo objeto Question con el texto de la pregunta proporcionado y la fecha de publicación calculada.
    return Question.objects.create(question_test=question_test, pub_date=time)

               
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
        
    def test_no_future_questions(self):
        # Create a future question (30 days in the future)
        # Crear una pregunta futura (30 días en el futuro)
        create_question("Future question", days=30)    
        # Get the response from the index view
        # Obtener la respuesta de la vista "index"
        response = self.client.get(reverse("polls:index"))    
        # Verify that the response status code is 200 (success)
        # Verificar que el código de estado de la respuesta sea 200 (éxito)
        self.assertEqual(response.status_code, 200)    
        # Verify that the response contains the text "No polls are available"
        # Verificar que la respuesta contiene el texto "No polls are available"
        self.assertContains(response, "No polls are avaible")
        # Verify that the latest_question_list in the response's context is an empty queryset
        # Verificar que latest_question_list en el contexto de la respuesta es un conjunto de consultas vacío
        self.assertQuerysetEqual(response.context["latest_question_list"], [])


    def test_pass_questions(self):
        # Create a past question (-10 days in the past)
        # Crear una pregunta pasada (-10 días en el pasado)
        question = create_question("Past question", days=-10)
        # Get the response from the index view
        # Obtener la respuesta de la vista "index"
        response = self.client.get(reverse("polls:index"))
        # Verify that the response status code is 200 (success)
        # Verificar que el código de estado de la respuesta sea 200 (éxito)
        self.assertEqual(response.status_code, 200)
        # Verify that the latest_question_list in the response's context contains the expected question
        # Verificar que latest_question_list en el contexto de la respuesta contiene la pregunta esperada
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
        
    def test_future_question_and_past_question(self):
        """
        Even if boot pass and future question exist, onli past questions are displayed 
        """
        past_question = create_question(question_test="Past question", days=-30)
        future_question = create_question(question_test="Past question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question])   
         
    def test_two_past_questions(self):
        """_
        The questioms index page my display multiple questions.
        """
        past_question1 = create_question(question_test="Past question 1", days=-30)
        past_question2 = create_question(question_test="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], [past_question1, past_question2]
        )
    
    def test_two_future_questions(self):
        """_
        The questioms index page my display multiple questions.
        """
        future_question1 = create_question(question_test="Future question 1", days=30)
        future_question2 = create_question(question_test="Future question 2", days=40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], []
        )   

        