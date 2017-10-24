from django.contrib.auth import authenticate
from django.test import TestCase, TransactionTestCase

from member.models import User


class UserModelTest(TransactionTestCase):
    DUMMY_USERNAME = 'username'
    DUMMY_PASSWORD = 'password'

    def test_fields_default_value(self):
        """
        user 를 기본값으로 설정했을 때 default 값이 잘 들어 있나
        :return:
        """
        user = User.objects.create_user(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD,
        )
        self.assertEqual(user.first_name, '')
        self.assertEqual(user.last_name, '')
        self.assertEqual(user.username, self.DUMMY_USERNAME)
        self.assertEqual(user.img_profile, 'default/profile.jpg')
        self.assertEqual(user.stars.count(), 0)
        self.assertEqual(user, authenticate(
            username=self.DUMMY_USERNAME,
            password=self.DUMMY_PASSWORD,
        ))

    def test_follow(self):
        u1, u2, u3, u4 = [User.objects.create_user(
            username=f'{name}'
        ) for name in ['은경', '보영', '혜리', '료코']]

        u1.follow_toggle(u2)
        u1.follow_toggle(u3)
        u1.follow_toggle(u4)

        u2.follow_toggle(u3)
        u2.follow_toggle(u4)

        u3.follow_toggle(u4)

        # user.stars 카운트 테스트
        self.assertEqual(u1.stars.count(), 3)
        self.assertEqual(u2.stars.count(), 2)
        self.assertEqual(u3.stars.count(), 1)
        self.assertEqual(u4.stars.count(), 0)

        # user.stars 에 인스턴스 존재 테스트
        self.assertIn(u2, u1.stars.all())
        self.assertIn(u3, u1.stars.all())
        self.assertIn(u4, u1.stars.all())

        self.assertIn(u3, u1.stars.all())
        self.assertIn(u4, u1.stars.all())

        self.assertIn(u4, u1.stars.all())

