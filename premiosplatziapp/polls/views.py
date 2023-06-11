from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from . models import Question, Choice


# Create your views here.
# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(request,"polls/index.html", {
#         "latest_question_list": latest_question_list
#     })

# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/detail.html",{
#         "question": question
#     } )

# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request,"polls/results.html",{
#             "question": question
#         })

class IndexView(generic.ListView):
    template_name = "polls/index.html"  # Plantilla utilizada para renderizar la vista
    context_object_name = "latest_question_list"  # Nombre del objeto en el contexto de la plantilla

    def get_queryset(self):
        return Question.objects.order_by("-pub_date")[:5]  # Consulta para obtener todas las preguntas

class DetailView(generic.DetailView):
    model = Question  # Modelo utilizado para la vista
    template_name = "polls/detail.html"  # Plantilla utilizada para renderizar la vista de detalle

class ResultsView(generic.DetailView):
    model = Question  # Modelo utilizado para la vista
    template_name = "polls/results.html"  # Plantilla utilizada para renderizar la vista de resultados


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request,"polls/detail.html",{
            "question": question,
            "error_message": "!No elegiste una respuesta¡"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args = (question.id,)))
        
