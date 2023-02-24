from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('노동복지 빅데이터 포털', navbar.text)
        self.assertIn('Home', navbar.text)
        self.assertIn('지식정보', navbar.text)
        self.assertIn('데이터맵', navbar.text)
        self.assertIn('분석환경', navbar.text)
        self.assertIn('Log-In', navbar.text)

    def test_post_list(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)

    def test_post_detail(self):
        post_000 = Post.objects.create(
            title= '첫번째 포스트입니다.',
            content='Hello world',
        )
        self.assertEqual(post_000.get_absolute_url(), '/blog/1/')
        response = self.client.get(post_000.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')
        self.navbar_test(soup)

