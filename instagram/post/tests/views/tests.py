from django.test import TestCase
from django.urls import reverse, resolve

from ... import views


class PostLiseToggleViewTEst(TestCase):
    TEST_POST_PK = 1
    VIEW_URL = f'/post/{TEST_POST_PK}/like/'
    VIEW_URL_NAME = 'post:post_like'

    def test_url_equal_reverse_url_name(self):
        """
        VIEW_URL_NAME reversed url이 VIEW_URL과 같은지 테스트
        :return:
        """
        self.assertEqual(
            self.VIEW_URL,
            reverse(self.VIEW_URL_NAME, kwargs={'pk': self.TEST_POST_PK})
        )

    def test_url_resolves_to_post_like_toggle_view(self):
        """
        VIEW_URL_NAME reversed url의 view가 실제 뷰와 같은지 검사
        :return:
        """
        found = resolve(self.VIEW_URL)
        self.assertEqual(found.func, views.post_like)
