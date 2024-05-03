from rest_framework.test import APITestCase, APIRequestFactory
from django.urls import reverse
from rest_framework import status
from .views import PostListCreatGenericAPIViews
from django.contrib.auth import get_user_model

User = get_user_model()

class HelloWordApiTest(APITestCase):
    def test_hello_world(self):
        print("Testing the hello world api")
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message':'Home page!'})
        
class PostListCreateTestCase(APITestCase):
    
    def authenticate(self):
        signup_data= {
            "email": "testuser2@gmail.com",
            "username": "testuser2",
            "password": "Testuser2",
            "date_of_birth": "2000-01-01",
        }
        self.client.post(reverse('signup'),
                         signup_data)
        
        login_data= {
            "email": "testuser2@gmail.com",
            "password": "Testuser2"
        }
        response = self.client.post(reverse('login'),
                                    login_data)
        
        access_token=response.data["data"]["access_token"]
    
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        
        
    
    def setUp(self):
        # self.factory = APIRequestFactory()
        # self.view= PostListCreatGenericAPIViews.as_view()
        self.url= reverse("posts")
      
      
        # self.user = User.objects.create(
        #     username="testuser1",
        #     email="testuser1@gmail.com",
        #     password="Testuser1",
        #     date_of_birth="2000-01-01",
        # )
    
    
    def test_post_list(self):
        print("Testing the post list")
        self.authenticate()
        
        
        # request = self.factory.get(self.url)
        # request.user= self.user
        # response= self.view(request)
        response= self.client.get(self.url)
      
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
        self.assertEqual(response.data['results'], [])
        
    def test_post_create(self):
        print("Creating a new post Test")
        
        self.authenticate()
        
        sample_post= {
            "title": "New Post",
            "content": "This is a new post",
      
        }
        
        # request = self.factory.post(self.url, sample_post)
        # request.user= self.user
        
        # response= self.view(request)
        response= self.client.post(self.url, sample_post)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], sample_post['title'])
     
       
