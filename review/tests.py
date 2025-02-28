from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Review, Comment

class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.review = Review.objects.create(
            film_title="Test Film",
            slug="test-film",
            author=self.user,
            content="This is a test review.",
            director="Test Director",
            release_year=2024,
            status=1
        )

    def test_review_str(self):
        self.assertEqual(str(self.review), "Test Film | Reviewed by testuser")

    def test_review_status_default(self):
        draft_review = Review.objects.create(
            film_title="Draft Film",
            slug="draft-film",
            author=self.user,
            content="This is a draft review.",
            director="Test Director",
            release_year=2024
        )
        self.assertEqual(draft_review.status, 0)  # Default status should be draft (0)


class CommentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.review = Review.objects.create(
            film_title="Test Film",
            slug="test-film",
            author=self.user,
            content="This is a test review.",
            director="Test Director",
            release_year=2024,
            status=1
        )
        self.comment = Comment.objects.create(
            review=self.review,
            author=self.user,
            content="This is a test comment.",
            approved=True
        )

    def test_comment_str(self):
        self.assertEqual(str(self.comment), "testuser wrote: This is a test comment.")


class ReviewViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.review = Review.objects.create(
            film_title="Test Film",
            slug="test-film",
            author=self.user,
            content="This is a test review.",
            director="Test Director",
            release_year=2024,
            status=1
        )

    def test_review_list_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/index.html')
        self.assertContains(response, "Test Film")

    def test_review_detail_view(self):
        response = self.client.get(reverse('review_detail', args=[self.review.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/review_detail.html')
        self.assertContains(response, "This is a test review.")


class CommentViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.user2 = User.objects.create_user(username='anotheruser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.review = Review.objects.create(
            film_title="Test Film",
            slug="test-film",
            author=self.user,
            content="This is a test review.",
            director="Test Director",
            release_year=2024,
            status=1
        )
        self.comment = Comment.objects.create(
            review=self.review,
            author=self.user,
            content="This is a test comment.",
            approved=True
        )

    def test_edit_comment_view(self):
        response = self.client.get(reverse('edit_comment', args=[self.review.slug, self.comment.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review/edit_comment.html')
        
        response = self.client.post(reverse('edit_comment', args=[self.review.slug, self.comment.id]), {
            'content': 'Updated comment'
        })
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.content, 'Updated comment')

    def test_delete_comment_view(self):
        response = self.client.post(reverse('delete_comment', args=[self.review.slug, self.comment.id]))
        self.assertEqual(response.status_code, 302)  # Redirect after deletion
        self.assertFalse(Comment.objects.filter(id=self.comment.id).exists())

    def test_delete_comment_by_wrong_user(self):
        self.client.logout()
        self.client.login(username='anotheruser', password='testpass')
        response = self.client.post(reverse('delete_comment', args=[self.review.slug, self.comment.id]))
        self.assertEqual(response.status_code, 302)  # Redirect due to permission check
        self.assertTrue(Comment.objects.filter(id=self.comment.id).exists())  # Comment should not be deleted


class URLResolutionTest(TestCase):
    def test_home_url_resolves(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_review_detail_url_resolves(self):
        url = reverse('review_detail', args=['some-slug'])
        self.assertEqual(url, '/some-slug/')