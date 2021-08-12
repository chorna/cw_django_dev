import json

from django.test import TestCase, Client
from django.contrib.auth import get_user_model

from .models import Question, Answer, Like
# Create your tests here.


class TestQuestions(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user1 = User.objects.create_user(username='user1', password='secret1')
        self.user2 = User.objects.create_user(username='user2', password='secret2')
        self.user3 = User.objects.create_user(username='user3', password='secret3')

        self.q1 = self.create_helper(Question, {
            'author': self.user1,
            'title': 'title1'
        })

        self.q2 = self.create_helper(Question, {
            'author': self.user2,
            'title': 'title2'
        })

        self.q3 = self.create_helper(Question, {
            'author': self.user3,
            'title': 'title3'
        })

        self.client = Client()

    def create_helper(self, model, data):
        return model.objects.create(**data)

    def test_sort_by_points(self):
        answer1 = self.create_helper(Answer, {
            'question': self.q1,
            'author': self.user2
        })
        like1 = self.create_helper(Like, {
            'question': self.q1,
            'author': self.user3,
            'value': 5,
        })
        dislike1 = self.create_helper(Like, {
            'question': self.q1,
            'author': self.user2,
            'value': -3
        })

        answer2 = self.create_helper(Answer, {
            'question': self.q2,
            'author': self.user1
        })

        answer3 = self.create_helper(Answer, {
            'question': self.q3,
            'author': self.user1
        })
        answer4 = self.create_helper(Answer, {
            'question': self.q3,
            'author': self.user2
        })

        questions = Question.objects.sorted_by_points()
        self.assertEquals(questions[0], self.q3)
        self.assertEquals(questions[0].points, 10*2 + 0 + 10)

        self.assertEquals(questions[1], self.q1)
        self.assertEquals(questions[1].points, 10*1 + 5*1 - 3*1 + 10)

        self.assertEquals(questions[2], self.q2)
        self.assertEquals(questions[2].points, 10*1 + 0 + 10)

    def test_upsert_answers(self):
        self.client.login(username='user1', password='secret1')
        path = '/question/answer'
        value = 5
        response = self.client.post(
            path,
            {'question_pk': self.q2.id, 'value': value},
            content_type="application/json"
            )
        self.assertEquals(response.status_code, 200)
        last_answer = Answer.objects.filter(author=self.user1).last()
        self.assertEquals(last_answer.value, value)

        value = 2
        response = self.client.post(
            path,
            {'question_pk': self.q2.id, 'value': value},
            content_type="application/json"
            )
        self.assertEquals(response.status_code, 200)
        last_answer = Answer.objects.filter(author=self.user1).last()
        self.assertEquals(last_answer.value, value)

    def test_upsert_likes(self):
        self.client.login(username='user1', password='secret1')
        path = '/question/like'
        value = 5
        response = self.client.post(
            path,
            {'question_pk': self.q3.id, 'value': value},
            content_type="application/json"
            )
        self.assertEquals(response.status_code, 200)
        last_like = Like.objects.filter(author=self.user1).last()
        self.assertEquals(last_like.value, value)

        value = 5
        response = self.client.post(
            path,
            {'question_pk': self.q3.id, 'value': value},
            content_type="application/json"
            )
        self.assertEquals(response.status_code, 200)
        last_like = Like.objects.filter(author=self.user1).last()
        self.assertEquals(last_like.value, 0)

        value = -3
        response = self.client.post(
            path,
            {'question_pk': self.q3.id, 'value': value},
            content_type="application/json"
            )
        self.assertEquals(response.status_code, 200)
        last_like = Like.objects.filter(author=self.user1).last()
        self.assertEquals(last_like.value, value)