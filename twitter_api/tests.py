# -*- coding: utf-8 -*-
from django.test import TestCase
from utils import api
from models import User, Status
from factories import UserFactory
import tweepy

STATUS_ID = 327926550815207424
USER_ID = 813286
USER_SCREEN_NAME = 'BarackObama'
USER1_ID = 18807761
USER1_SCREEN_NAME = 'voronezh'
#USER2_ID = 16477634
#USER2_SCREEN_NAME = 'durov'

class TwitterApiTest(TestCase):

    def test_request(self):

        response = api('get_status', STATUS_ID)
        self.assertEqual(response.text, '@mrshoranweyhey Thanks for the love! How about a follow for a follow? :) ^LF')
        self.assertEqual(response.source_url, 'http://www.exacttarget.com/social')

        response = api('get_user', USER_SCREEN_NAME)
        self.assertEqual(response.id, USER_ID)
        self.assertEqual(response.name, 'Barack Obama')

    def test_tweepy_properties(self):

        instance = User.remote.fetch(USER_ID)

        self.assertEqual(instance.screen_name, USER_SCREEN_NAME)
        self.assertTrue(isinstance(instance.tweepy, tweepy.models.User))
        self.assertEqual(instance.tweepy.id_str, str(USER_ID))

    def test_fetch_user(self):

        instance = User.remote.fetch(USER_ID)

        self.assertEqual(instance.screen_name, USER_SCREEN_NAME)
        self.assertEqual(instance.id, USER_ID)
        self.assertEqual(instance.name, 'Barack Obama')
        self.assertEqual(instance.location, 'Washington, DC')
        self.assertEqual(instance.verified, True)
        self.assertEqual(instance.lang, 'en')
        self.assertTrue(instance.followers_count > 30886141)
        self.assertTrue(instance.friends_count > 660030)
        self.assertTrue(instance.listed_count > 192107)

        instance1 = User.remote.fetch(USER_SCREEN_NAME)
        self.assertEqual(instance.name, instance1.name)
        self.assertEqual(User.objects.count(), 1)

    def test_fetch_user_statuses(self):

        instance = UserFactory.create(id=USER_ID)

        self.assertEqual(Status.objects.count(), 0)
        instances = instance.fetch_statuses(count=30)
        self.assertEqual(len(instances), 30)
        self.assertEqual(len(instances), Status.objects.count())

        instances = instance.fetch_statuses(all=True, exclude_replies=True)
        self.assertTrue(len(instances) > 3100)
        self.assertTrue(len(instances) < 8000)
        self.assertEqual(len(instances), Status.objects.count())

    def test_fetch_user_followers(self):

        instance = UserFactory.create(id=USER1_ID)

        self.assertEqual(User.objects.count(), 1)
        instances = instance.fetch_followers(all=True)
        self.assertTrue(len(instances) > 870)
        self.assertTrue(len(instances) < 1000)
        self.assertEqual(len(instances), User.objects.count()-1)