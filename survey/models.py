from datetime import date

from django.db import models
from django.db.models import Sum, Case, When, Count
from django.db.models.functions import Coalesce
from django.contrib.auth import get_user_model
from django.db.models.expressions import Value

from django.urls import reverse


class QuestionManager(models.Manager):
    def sorted_by_points(self):
        return self.annotate(
            num_answers=Count('answers', distinct=True),
            total_likes=Coalesce(Sum('likes__value'), Value(0)),
            to_day=Case(
                When(created=date.today(), then=10),
                default=0
            ),
            points=Count('answers', distinct=True)*10
            + Coalesce(Sum('likes__value'), Value(0))
            + Case(
                When(created=date.today(), then=10),
                default=0
            )
        ).order_by('-points')


class Question(models.Model):
    created = models.DateField('Creada', auto_now_add=True)
    author = models.ForeignKey(get_user_model(), related_name="questions", verbose_name='Pregunta',
                               on_delete=models.CASCADE)
    title = models.CharField('Título', max_length=200)
    description = models.TextField('Descripción')

    objects = QuestionManager()
    # TODO: Quisieramos tener un ranking de la pregunta, con likes y dislikes dados por los usuarios.

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self):
        return reverse('survey:question-edit', args=[self.pk])


class Answer(models.Model):
    ANSWERS_VALUES = ((0,'Sin Responder'),
                      (1,'Muy Bajo'),
                      (2,'Bajo'),
                      (3,'Regular'),
                      (4,'Alto'),
                      (5,'Muy Alto'),)

    question = models.ForeignKey(Question, related_name="answers", verbose_name='Pregunta', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), related_name="answers", verbose_name='Autor', on_delete=models.CASCADE)
    value = models.PositiveIntegerField("Respuesta", default=0, choices=ANSWERS_VALUES)
    comment = models.TextField("Comentario", default="", blank=True)


class Like(models.Model):
    LIKE_VALUES = [
        (5, 5),
        (-3, -3)
    ]
    question = models.ForeignKey(Question, related_name='likes', on_delete=models.CASCADE)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    value = models.IntegerField("Respuesta", default=5, choices=LIKE_VALUES)

    def __str__(self) -> str:
        return "%s" % self.value

