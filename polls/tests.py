import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse
# from django.views import generic
# from django import HttpResponse

from .models import Question, Choice


class QuestionMethodTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() deve retornar falso para questões com 
        data de publicação futura
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertEqual(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() deve retornar falso para questões com
        data de publicação anterior a 1 dia
        """
        time = timezone.now() - datetime.timedelta(days=30)
        old_question = Question(pub_date=time)
        self.assertEqual(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() deve retornar verdadeiro para questões com
        data de publicação no dia anterior
        """
        time = timezone.now() - datetime.timedelta(days=1)
        recent_question = Question(pub_date=time)
        self.assertEqual(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


def create_choice(question, choice_text):
    return Choice.objects.create(question=question, choice_text=choice_text)


class QuestionViewTests(TestCase):
    def test_index_view_with_no_questions(self):
        """
        Se não tiver questões, uma mensagem amigavel deve ser apresentada
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_index_view_with_a_past_question(self):
        """
        a
        """
        past_question = create_question(question_text="Past question.", days=-30)
        create_choice(past_question, "Choice text")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_index_view_with_a_future_question(self):
        future_question = create_question(question_text="Future question.", days=30)
        create_choice(future_question, "Choice text")
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.', status_code=200)
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_index_view_with_a_past_and_future_question(self):
        future_question = create_question(question_text="Future question.", days=30)
        create_choice(future_question, "Choice text future")
        past_question = create_question(question_text="Past question.", days=-30)
        create_choice(past_question, "Choice text past")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_index_view_with_two_past_questions(self):
        past_question_1 = create_question(question_text="Past question 1.", days=-30)
        past_question_2 = create_question(question_text="Past question 2.", days=-29)
        create_choice(past_question_1, "Choice text 1")
        create_choice(past_question_2, "Choice text 2")
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 2.>', '<Question: Past question 1.>'])

    def test_index_view_with_a_question_without_choice(self):
        create_question(question_text="Question without a choice.", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, 'No polls are available', status_code=200)


class QuestionDetailTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_question(self):
        past_question = create_question(question_text="Past question.", days=-5)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)


class QuestionResultTests(TestCase):
    def test_result_view_with_a_future_question(self):
        future_question = create_question(question_text="Future question.", days=5)
        response = self.client.get(reverse("polls:results", args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)

    def test_result_view_with_a_past_question(self):
        past_question = create_question(question_text="Past question.", days=-5)
        response = self.client.get(reverse("polls:results", args=(past_question.id,)))
        self.assertContains(response, past_question.question_text, status_code=200)

# def index(request):
#     return HttpResponse("hello, World. You're at the polls index.")

