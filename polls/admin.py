# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question,Choice

class Choicein(admin.TabularInline):
    model = Choice
    extra = 4

class QuestionAdmin(admin.ModelAdmin): #einai gia na allaxoume ta paidia fields,fieldset
    fieldsets = [
         ('Question',         {'fields': ['question_text']}),
         ('Date information', {'fields': ['pud_date']}),
    ]
    inlines = [Choicein]
    list_display = ('question_text', 'pud_date','was_published_recently')

admin.site.register(Question,QuestionAdmin)
