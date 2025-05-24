from django.test import TestCase

from .models import User


class UserModelTest(TestCase):
    def test_follow(self) -> None:
        u1 = User.objects.create(username="john", email="john@example.com")
        u2 = User.objects.create(username="susan", email="susan@example.com")
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)

        u1.follow(u2)
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 1)
        self.assertEqual(u2.followers_count(), 1)
        self.assertEqual(u1.following.first(), u2)
        self.assertEqual(u2.followers.first(), u1)

        u1.unfollow(u2)
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.following_count(), 0)
        self.assertEqual(u2.followers_count(), 0)
