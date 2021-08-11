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

        self.q2 = self.create_helper(Question, {
            'author': self.user2,
            'title': 'title2'
        })

        self.q3 = self.create_helper(Question, {
            'author': self.user3,
            'title': 'title3'
        })

    def create_helper(self, model, data):
        return model.objects.create(**data)

    def test_sort_by_points(self):
        answer1 = self.create_helper(Answer, {
            'question': self.q1,
            'author': self.user2
        })
        like1 = self.create_helper(Like, {
            'question': self.q1,
            'author': self.user3
        })
        dislike1 = self.create_helper(Like, {
            'question': self.q1,
            'author': self.user2,
            'value': -1
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
        self.assertEquals(questions[0], 30)

        self.assertEquals(questions[1], self.q1)
        self.assertEquals(questions[1], 22)

        self.assertEquals(questions[2], self.q2)
        self.assertEquals(questions[2], 20)
