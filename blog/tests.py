from django.contrib.auth.models import User
from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Post


# Create your tests here.
class TestView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_trump = User.objects.create_user(username='trump', password='somepassword')
        self.user_obama = User.objects.create_user(username='obama', password='somepassword')

    def navbar_test(self, soup):
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        logo_btn = navbar.find('a', text='Do It Django')
        self.assertEqual(logo_btn.attrs['href'], '/')

        home_btn = navbar.find('a', text='Home')
        self.assertEqual(home_btn.attrs['href'], '/')

        blog_btn = navbar.find('a', text='Blog')
        self.assertEqual(blog_btn.attrs['href'], '/blog/')

        about_me_btn = navbar.find('a', text='About Me')
        self.assertEqual(about_me_btn.attrs['href'], '/about_me/')

    def test_post_list(self):
        # 포스트 목록 페이지가 정상적으로 로드된다
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

        # 페이지 타이틀은 Blog
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(soup.title.text, 'Blog')

        # 네비게이션 바가 있다
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 게시물이 하나도 없다면
        self.assertEqual(Post.objects.count(), 0)
        # main-area에 '아직 게시물이 없습니다'가 나타난다
        main_area = soup.find('div', id='main-area')
        self.assertIn('아직 게시물이 없습니다', main_area.text)

        # 포스를 만든다
        post_001 = Post.objects.create(
            title='첫 번째 포스트 입니다.',
            content='Hello World. 1st',
            author=self.user_trump,
        )

        post_002 = Post.objects.create(
            title='두 번째 포스트 입니다.',
            content='Hello World. 2nd',
            author=self.user_obama,
        )
        
        # 두개가 만들어 졌는지 확인
        self.assertEqual(Post.objects.count(), 2)

        # 새로 고침하면 정상으로 읽혀진다
        response = self.client.get('/blog/')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertEqual(response.status_code, 200)

        # main-area에 포스트 제목 2개가 나타난다
        main_area = soup.find('div', id='main-area')
        self.assertIn(post_001.title, main_area.text)
        self.assertIn(post_002.title, main_area.text)

        # 아직 게시물이 없습니다 라는 문구는 더 이상 나타나지 않는다
        self.assertNotIn('아직 게시물이 없습니다', main_area.text)

        self.assertIn(self.user_trump.username.upper(), main_area.text)
        self.assertIn(self.user_obama.username.upper(), main_area.text)

        # navbar가 제대로 보인다
        self.navbar_test(soup)

    def test_post_detail(self):

        # 포스트가 하나 있다
        post_001 = Post.objects.create(
            title='첫번째 포스트입니다.',
            content='Hello world',
            author=self.user_trump,
        )

        # 그 포스트의 url은 'blog/1/' 이다
        self.assertEqual(post_001.get_absolute_url(), '/blog/1/')

        # 포스트의 상세 페이지 를 불러온다
        response = self.client.get(post_001.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 포스트 목록 페이지와 똑같은 네비게이션 바가 있다
        navbar = soup.nav
        self.assertIn('Blog', navbar.text)
        self.assertIn('About Me', navbar.text)

        # 포스트의 제목이 웹 브라우저에 탭 타이틀에 들어 있다
        self.assertIn(post_001.title, soup.title.text)

        # 포스트의 제목이 포스트 영역에 있다
        main_area = soup.find('div', id='main-area')
        post_area = main_area.find('div', id='post-area')
        self.assertIn(post_001.title, post_area.text)

        # 포스트의 내용이 포스트 영역에 있다
        self.assertIn(post_001.content, post_area.text)

        # 작성자가 post-area에 있다
        self.assertIn(self.user_trump.username.upper(), post_area.text)

        # navbar가 제대로 보인다
        self.navbar_test(soup)

