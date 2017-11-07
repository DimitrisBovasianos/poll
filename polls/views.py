# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404,render
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """return the last five published questions"""
        return  Question.objects.filter(  #epistrefei ena queryset dld mia lista apo Question twn opoiwn
          pud_date__lt=timezone.now()
           ).exclude(choice__isnull=True).order_by('-pud_date')[:5]    #to pud_date einai mikrotero h iso apo to timezone.now


class DetailView(generic.DetailView):
    model = Question
    template_name ='polls/detail.html'

    def get_queryset(self):
        """
        excludes any questions that are not published yes
        """
        return Question.objects.filter(pud_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id) #exetazei ama uparxei h erwthsh alliws emfanizei error 404
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice']) #epilegeis me th me8odo post to id tou choice
    except (KeyError, Choice.DoesNotExist): # an h choice den uparxei sth database pernaei to error_message
        #redisplay the question voting form (emfanizei pali th detail.html)
        return render(request, 'polls/detail.html',{
               'question':question,
            'error_message': "you dont select a choice",

           })
    else:
        selected_choice.votes += 1 # alliws votes attitube apo to polls/models pou kaname tis listes sth bazh dedomenwn
        #anevazei to votes kata ena sto choice
        selected_choice.save()
        # panta na epistrefeis mia HttpResponse meta apo epituxia ths
        #POST.auto apotrepei apo ta dedomena na apo8hkeutoun 2 fores
        # an o xrhsths pathsei to back
        #kanei redirect sto sth def results ousiastika dinontas argument to question.id
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
