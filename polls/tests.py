# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
import datetime
from django.utils import timezone

from .models import Question
from django.urls import reverse

class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
     time = timezone.now() + datetime.timedelta(days=30)
     future_question = Question(pud_date=time)
     self.assertIs(future_question.was_published_recently(), False)

def create_question(question_text, days):
     """
     create a question with the given question_text and
     and published the given number of days offset to now(
     doesnot work for question published in the past,works
     for the questions will published in the future
     )
     """
     time = timezone.now() + datetime.timedelta(days=days)
     return Question.objects.create(question_text=question_text,pud_date=time)

class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        if no questions exist, an appropriate message is displayed
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,"no polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        """
        create a question in the and test if it published in
        the index page
        """
        create_question(question_text="past question",days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
        ['<Question: past question>']
        )

    def test_future_question(self):
        create_question(question_text="future question",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "no polls are available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        create_question(question_text="past question",days=-30)
        create_question(question_text="future question",days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
        ['<Question: past question>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        the detail view of a question with a pud_date in the future
        must return a 404 not found
        """
        future_question= create_question(question_text="future question",days=5)
        url = reverse('polls:detail',args=(future_question.id,)) #edw vazoume to url ths erwthshs pou xrhsimopoihsame px /polls/4
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question= create_question(question_text="past question",days=-3)
        url = reverse('polls:detail',args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, "past question") 
