import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_test = models.CharField(max_length = 200)
    pub_date = models.DateTimeField("date published")
    
    def __str__(self):
        return self.question_test
    
    def was_published_recently(self):
    # Verifica si la fecha de publicación es reciente con un día atras a la fecha actual
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        

class Choice(models.Model):
    # Clase que representa una opción dentro de un modelo de encuesta en Django   
    questions = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Campo ForeignKey que establece una relación de clave externa con el modelo Question.
    # Cada opción pertenece a una pregunta específica.
    choice_test = models.CharField(max_length=200)
    # Campo CharField que almacena el texto de la opción.
    # El parámetro max_length=200 indica que la longitud máxima del texto es de 200 caracteres.
    votes = models.IntegerField(default=0)
    # Campo IntegerField que almacena la cantidad de votos que ha recibido la opción.
    # El parámetro default=0 establece el valor predeterminado de votos en 0.
    def __str__(self):
        # Método especial que devuelve una representación legible de la opción.
        return self.choice_test



