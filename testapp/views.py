from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse

from testapp.models import Question, Choice


def index(request):
    # q = [{x.id:x.question_text} for x in Question.objects.all()]
    # template = loader.get_template('testapp/index.html')
    latest_question_list = Question.objects.order_by('-pub_date').values()[:5]
    output = [x['question_text'] for x in latest_question_list]
    # print(request)
    context = {
        'latest_question_list': latest_question_list,
    }
    # print(request,latest_question_list, output[0])
    # return HttpResponse(template.render(context, request))
    return render(request, 'testapp/index.html', context)


# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     output = ', '.join([q.question_text for q in latest_question_list])
#     return HttpResponse(output)


def new(request):
    return HttpResponse("New World")


def detail(request, question_id):
    # try:
    #     question = Question.objects.get(id=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist.")

    question = get_object_or_404(Question, id=question_id)

    # return HttpResponse(f"You are looking at question with question id {question_id}")
    return render(request, 'testapp/detail.html', {'question': question})


def result(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    return render(request, 'testapp/result.html', {"question":question})


def vote(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    try :
        selected_choice = question.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'testapp/detail.html',{ 'question': question, 'error_message': "You didn't select a choice"})
    else : 
        selected_choice.votes += 1
        selected_choice.save()
    # print(selected_choice)
    # return HttpResponse(f"You are voting on the question with question id {question_id}")
    return HttpResponseRedirect(reverse('testapp:result', args=[question.id]))