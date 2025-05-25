from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from .models import Post

User = get_user_model()


class PostModelTest(TestCase):
    def test_follow_posts(self) -> None:
        u1 = User.objects.create(username="john", email="john@example.com")
        u2 = User.objects.create(username="susan", email="susan@example.com")
        u3 = User.objects.create(username="mike", email="mike@example.com")
        u4 = User.objects.create(username="david", email="david@example.com")

        now = timezone.now()
        p1 = Post.objects.create(
            body="Post from john", author=u1, timestamp=now + timedelta(seconds=1)
        )
        p2 = Post.objects.create(
            body="Post from susan", author=u2, timestamp=now + timedelta(seconds=4)
        )
        p3 = Post.objects.create(
            body="Post from mike", author=u3, timestamp=now + timedelta(seconds=3)
        )
        p4 = Post.objects.create(
            body="Post from david", author=u4, timestamp=now + timedelta(seconds=2)
        )

        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)

        f1 = list(Post.followed_posts(u1).all())
        f2 = list(Post.followed_posts(u2).all())
        f3 = list(Post.followed_posts(u3).all())
        f4 = list(Post.followed_posts(u4).all())

        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])
