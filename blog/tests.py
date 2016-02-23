from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from .models import Post


def create_post(title, text, author):
    return Post.objects.create(title=title, text=text, author=author)


class PostMethodTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='testb@test.com', password='top_secret')

    def test_publish_method(self):
        post = create_post("Publishing post.", 'publishing a post.', self.user)
        post.publish()
        self.assertTrue(post.published_date)


class PostIndexTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='testb@test.com', password='top_secret')

    def test_index_with_no_posts(self):
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts are available.')
        self.assertQuerysetEqual(response.context['posts'], [])

    def test_index_with_a_post(self):
        post = create_post('Publishing post', 'publishing a post', self.user)
        post.publish()
        response = self.client.get(reverse('blog:index'))
        self.assertQuerysetEqual(response.context['posts'], ['<Post: Publishing post>'])

    def test_index_with_a_draft(self):
        create_post('Draft post', 'Creating a draft post', self.user)
        response = self.client.get(reverse('blog:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts are available.')
        self.assertQuerysetEqual(response.context['posts'], [])


class PostDetailTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='test', email='testb@test.com', password='top_secret')

    def test_detail_with_draft(self):
        post = create_post('Draft post', 'Creating a draft post', self.user)
        response = self.client.get(reverse('blog:post_detail', args=(post.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, post.title, status_code=200)
        self.assertContains(response, '>Publish</a>')

    def test_detail_with_published_post(self):
        post = create_post('Published post', 'published post', self.user)
        post.publish()
        response = self.client.get(reverse('blog:post_detail', args=(post.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, '>Publish</a>')
        self.assertContains(response, post.title, status_code=200)

