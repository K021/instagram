import filecmp
from random import randint

import io

import os
from PIL import Image
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APILiveServerTestCase, force_authenticate

from post.apis import PostList
from post.models import Post

User = get_user_model()


class PostListViewTest(APILiveServerTestCase):
    URL_API_POST_LIST_NAME = 'api-post'
    URL_API_POST_LIST = '/api/post/'
    VIEW_CLASS = PostList

    @staticmethod
    def create_user(username='dummy'):
        return User.objects.create_user(username=username)

    @staticmethod
    def create_post(author=None):
        # django.core.files.base.ContentFile은 스트링 파일용으로 사용하도록 만들어졌다. (NamedTemporaryFile)
        return Post.objects.create(photo=File(io.BytesIO()), author=author)

    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_post_list_url_name_reverse(self):
        url = reverse(self.URL_API_POST_LIST_NAME)
        self.assertEqual(url, self.URL_API_POST_LIST)

    def test_post_list_url_resolve(self):
        resolver_match = resolve(self.URL_API_POST_LIST)
        self.assertEqual(resolver_match.url_name, self.URL_API_POST_LIST_NAME)
        self.assertEqual(resolver_match.func.view_class, self.VIEW_CLASS)

    def test_get_post_list(self):
        user = self.create_user()
        num = randint(1, 20)
        for i in range(num):
            self.create_post(author=user)
        url = reverse(self.URL_API_POST_LIST_NAME)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), num)

        for i in range(num):
            cur_post_data = response.data[i]
            self.assertIn('pk', cur_post_data)
            self.assertIn('author', cur_post_data)
            self.assertIn('photo', cur_post_data)
            self.assertIn('title', cur_post_data)

    def test_get_post_list_exclude_author_which_is_None(self):
        user = self.create_user()
        num_posts_with_author = randint(5, 10)
        num_posts_without_author = randint(10, 15)
        for i in range(num_posts_with_author):
            self.create_post(user)
        for i in range(num_posts_without_author):
            self.create_post()

        response = self.client.get(self.URL_API_POST_LIST)
        self.assertEqual(len(response.data), num_posts_with_author)

    # def test_create_post(self):
    #     data = {
    #         'photo': self.generate_photo_file(),
    #     }
    #     self.client.force_authenticate(user=self.create_user())
    #     response = self.client.post(self.URL_API_POST_LIST, data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     self.assertEqual(len(response.data), 1)

    def test_create_post(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/image.png')
        with open(path, 'rb') as f:
            data = {
                'photo': f,
            }
            self.client.force_authenticate(user=self.create_user())
            response = self.client.post(self.URL_API_POST_LIST, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)

        post = Post.objects.get(pk=response.data['pk'])
        self.assertTrue(filecmp.cmp(path, post.photo.file.name, shallow=True))

        # s3에 올라간 파일을 비교해야 하는 경우


# url = reverse('api-post')
# factory = APIRequestFactory()
# request = factory.get('/api/post')
#
# view = PostList.as_view()
# response = view(request)
#
# print(response.data)


# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase
#
# from post.models import Post
#
#
# class PostListViewTest(APITestCase):
#     def test_post_create(self):
#         """
#         Ensure we can create a new account object.
#         """
#         url = reverse('post:list')
#         data = {
#             'title': 'Test',
#             'photo': ,
#         }
#         response = self.client.post(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(Post.objects.count(), 1)
#         self.assertEqual(Post.objects.get().title, 'Test')
