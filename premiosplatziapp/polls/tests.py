import datetime

from django.test import TestCase
from django.urls.base import reverse                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                
from django.utils import timezone

from .models import Question, Choice

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

class QuestionDetailViewTest(TestCase):
    def test_future_question(self):
        """
        The datail wiew of a question with a pub_date in the future
        return a 404 (error no fount)
        """
        """
        La vista de detalle de una pregunta con una fecha de publicación en el futuro
        debe devolver un error 404 (página no encontrada)
        """

        # Create a new question with the question_text set to "Future question" and the pub_date set to the future date
        # Crear una nueva pregunta con el texto de la pregunta establecido en "Future question" y la fecha de publicación establecida en la fecha futura
        future_question = create_question(question_test="Future question 1", days=30)
        # Get the URL for the question detail view using the reverse function and the question's ID
        # Obtener la URL para la vista de detalle de la pregunta utilizando la función reverse y el ID de la pregunta
        url = reverse("polls:detail", args=(future_question.id,))
        # Send a GET request to the URL using the test client
        # Enviar una solicitud GET a la URL utilizando el cliente de pruebas (test client)
        response = self.client.get(url)
        # Assert that the response status code is 404, indicating a page not found error
        # Verificar que el código de estado de la respuesta sea 404, lo que indica un error de página no encontrada
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        The datail wiew of a question with a pub_date in the past
        displays yhe quiestion a text
        """
        """
        La vista de detalle de una pregunta con una pub_date en el pasado
        muestra el texto de la pregunta
        """
        
        # Creates a past question with the specified test and a negative time delta of 30 days.
        # Crea una pregunta pasada con el texto especificado y un desfase de tiempo negativo de 30 días.
        past_question = create_question(question_test="Past question 1", days=-30)
        # Generates the URL for the detail view of the past question using its ID.
        # Genera la URL para la vista de detalle de la pregunta pasada utilizando su ID.
        url = reverse("polls:detail", args=(past_question.id,))
        # Sends a GET request to the generated URL using the test client.
        # Envía una solicitud GET a la URL generada utilizando el cliente de pruebas.
        response = self.client.get(url) 
        # Asserts that the response contains the text of the past question's test.
        # Asegura que la respuesta contenga el texto de la pregunta pasada.       
        self.assertContains(response, past_question.question_test) 
        
def create_question(question_test, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_test=question_test, pub_date=time)

class QuestionResultsViewTests(TestCase):
    def test_question_not_exists(self):
        """Si el ID de la pregunta no existe, se debe obtener un código 404"""
        response = self.client.get(reverse("polls:results", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 404)

    def test_future_question(self):
        """Si es una pregunta del futuro, se debe obtener un código 404"""
        future_question = create_question("Pregunta futura", 30)
        response = self.client.get(reverse("polls:results", kwargs={'pk': future_question.pk}))
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """Si es una pregunta del pasado, se debe poder mostrar"""
        past_question = create_question("Pregunta pasada", -10)
        response = self.client.get(reverse("polls:results", kwargs={'pk': past_question.pk}))
        self.assertContains(response, past_question.question_test)

    def test_display_question_choices_and_votes(self):
        """La página debe mostrar los votos para cada opción de una pregunta"""
        question = create_question("Pregunta", -1)
        choice1 = Choice(choice_test="Opción 1", questions_id=question.id)
        choice1.save()

        choice2 = Choice(choice_test="Opción 2", questions_id=question.id)
        choice2.save()

        response = self.client.get(reverse("polls:results", kwargs={'pk': question.id}))

        self.assertContains(response, question.question_test)
        self.assertContains(response, choice1.choice_test + ' -- ' + str(choice1.votes) + ' vote')
        self.assertContains(response, choice2.choice_test + ' -- ' + str(choice2.votes) + ' votes')