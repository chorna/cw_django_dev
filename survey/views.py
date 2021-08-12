import json

from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView

from survey.models import Question, Answer, Like


class QuestionListView(ListView):
    model = Question

    def get_queryset(self):
        return self.model.objects.sorted_by_points()


class QuestionCreateView(CreateView):
    model = Question
    fields = ['title', 'description']
    redirect_url = ''

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class QuestionUpdateView(UpdateView):
    model = Question
    fields = ['title', 'description']
    template_name = 'survey/question_form.html'


def answer_question(request):
    body = json.loads(request.body)
    question_pk = body.get('question_pk')
    value = body.get('value')

    if not question_pk:
        return JsonResponse({'ok': False})
    Answer.objects.update_or_create(
        question_id=question_pk,
        author_id=request.user.pk,
        defaults={'value': value},
        )
    return JsonResponse({'ok': True})

def like_dislike_question(request):
    body = json.loads(request.body)
    question_pk = body.get('question_pk')
    value = body.get('value')

    if not question_pk:
        return JsonResponse({'ok': False})
    like = Like.objects.filter(question=question_pk, author=request.user).first()
    if like and like.value == int(value):
        value = 0

    Like.objects.update_or_create(
        question_id=question_pk,
        author_id=request.user.pk,
        defaults={'value': value},
    )
    return JsonResponse({'ok': True})

