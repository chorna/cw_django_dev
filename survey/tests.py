from django.test import TestCase

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

    def create_helper(model, data):
        return model.objects.create(**data)

    def test_points(self):
        answer1 = self.create_helper(Answer, {
            'question': self.q1,
            'author': self.user2
        })
        like1 = self.create_helper(Like, {
            'question': self.q1,
            'author': self.q2
        })
        dislike1 = self.create_helper(Like, {
            'question': self.q1,
            'author': self.q2,
            'value': -1
        })
        self.assertEquals(self.q1.points, 22)
