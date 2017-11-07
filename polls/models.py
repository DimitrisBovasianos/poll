import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


@python_2_unicode_compatible
class Question(models.Model): #sthlh sth vash dedomenwn
    # auta ta 2 einai pinakes sth vash dedomenwn enw to instance ths Field class dhlwnei to
    # tupo twn dedomenwn
    question_text = models.CharField(max_length=200)
    pud_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pud_date <=now


@python_2_unicode_compatible
class Choice(models.Model): #sthlh sth vash dedomenwn
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #ginetai h sxusxethsh metaxu twn 2 klasewn kai to on_delete.CASCADE otan diagrafoume mia erwthsh amesws diagrafete kai to choice
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
