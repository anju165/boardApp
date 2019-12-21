from django.test import TestCase
from django.urls import reverse, resolve
from .views import index, newTopic
from django.contrib.auth.models import User
from .models import Board, Post, Topic

# Create your tests here.
class HomeTest(TestCase):
    def testHomeViewStatus(self):
        url = reverse('index')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
    
    def testHomeUrl(self):
        view = resolve('/boardApp/')
        self.assertEquals(view.func, index)

class BoardTopicTest(TestCase):
    def setup(self):
        Board.objects.create(name='Python',descrption='All about Python')
    
    def testBoardTopicSuccess(self):
        url = reverse('topic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)
    
    def testBoardTopicFailure(self):
        url = reverse('topic', kwargs={'pk':100})
        response = self.client.get(url)
        self.assertEquals(response.status_code,404)

class NewTopicTest(TestCase):
    def setup(self):
        Board.objects.create(name='Python',descrption='All about Python')
        User.objects.create(name='ravi', email='ravi@gmail.com',password='1234')
    
    def test_csrf(self):
        url = reverse('newTopic', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertContains(response,'csrfmiddlewaretoken')
    
    def testNewTopicValidPost(self):
        url = reverse('newTopic', kwargs={'pk':1})
        data = {
            "subject" : "Test Data",
            "message" : "Some demo text"
        }
        response = self.client.post(url,data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
    
    def testNewTopicInvalidPost(self):
        url = reverse('newTopic', kwargs={'pk':1})
        response = self.client.post(url,{})
        self.assertEquals(response.status_code, 200)
    
    def testNewTopicEmptyPost(self):
        url = reverse('newTopic', kwargs={'pk':1})
        data = {
            "subject" : "",
            "message" : ""
        }
        response = self.client.post(url,data)
        self.assertEquals(response.status_code, 200)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())