from django.shortcuts import render

from django.http import JsonResponse, HttpRequest
from rest_framework.permissions import IsAuthenticated

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, generics, mixins, viewsets
from rest_framework.decorators import api_view, APIView
from .models import Post
from.serializers import PostSerializer
from django.shortcuts import get_object_or_404
from .permissions import IsLoggedIn, IsOwner, IsAdmin, ReadOnly




"""The following index, homePage, createPost, posts, get_post_by_id, update_post, delete_post  are function based views"""
def index(request:HttpRequest):
    return JsonResponse({'message':'Hello, World!'})

@api_view(http_method_names= ['GET'])
def homePage(request:Request):
    return Response(data= {'message':'Home page!'}, status=status.HTTP_200_OK)

@api_view(http_method_names= ['POST'])
def createPost(request:Request):
    return Response(data= {'message':'Create a post!'}, status=status.HTTP_201_CREATED)

@api_view(http_method_names= ['GET', 'POST'])
def posts(request:Request):
    if request.method == 'POST':
        data= request.data
        serializer = PostSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            response= {
                'message': 'Post created successfully!',
                'data': serializer.data
            }
            return Response(data= response, status=status.HTTP_201_CREATED)
        else:
            return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    elif request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(instance= posts, many=True)

        return Response(data= serializer.data, status=status.HTTP_200_OK)

@api_view(http_method_names= ['GET'])
def get_post_by_id(request:Request, id):
    post = get_object_or_404(Post, pk=id)
    # post = next((post for post in posts if post['id'] == id), None)
    if post:
        serializer = PostSerializer(instance= post)
        response = {
            'message': 'Post details',
            'data': serializer.data
        }
        return Response(data= response, status=status.HTTP_200_OK)
    else:
        return Response(data= {'message':'Post not found!'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(http_method_names= ['PUT'])
def update_post(request:Request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'PUT':
        data = request.data
        serializer = PostSerializer(instance=post, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Post updated successfully!',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    else:
        return Response(data={'message': 'Invalid request method!. Supported method is PUT'}, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(http_method_names= ['DELETE'])
def delete_post(request:Request, id):
    post = get_object_or_404(Post, pk=id)
    if request.method == 'DELETE':
        post.delete()
        return Response(data={'message': 'Post deleted successfully!'}, status=status.HTTP_200_OK)
    
    else:
        return Response(data={'message': 'Invalid request method!. Supported methos is DELETE'}, status=status.HTTP_400_BAD_REQUEST)
    


#***********Class based  API Views for creating and listing posts************
class PostListCreatClassBasedAPIView(APIView):
    """class based views for creating and listing posts """
    serializer_class = PostSerializer
    permission_classes=[ IsLoggedIn]
    def get(self, request:Request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = self.serializer_class(instance= posts, many=True)
        return Response(data= serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request:Request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data= data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            response = {
                'message': 'Post created successfully!',
                'data': serializer.data
            }
            return Response(data= response, status=status.HTTP_201_CREATED)
        else:
            return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

#***********Class based API Views for getting details, updating and deleting post************
class PostRetrieveUpdateDeleteClassBasedAPIView(APIView):
    """class based view for getting details, updating and deleting post """
    serializer_class = PostSerializer
    permission_classes=[ IsLoggedIn, IsOwner]
    def get(self, request:Request, id:int ,*args, **kwargs):
        post = get_object_or_404(Post, pk=id)

        serializer = self.serializer_class(instance= post)
        user= request.user

        author_info = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'date_of_birth': user.date_of_birth

        }

        data= serializer.data

        data['author'] = author_info

    
        response = {
            'message': 'Post details',
            'post': data,
        }
        return Response(data= response, status=status.HTTP_200_OK)

    def put(self, request:Request, id:int, *args, **kwargs):
        post = get_object_or_404(Post, pk=id)
        data = request.data
        serializer = self.serializer_class(instance=post, data=data)
        if serializer.is_valid():
            serializer.save()

            user= request.user

            author_info = {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'date_of_birth': user.date_of_birth
            }

            data= serializer.data

            data['author'] = author_info


            response = {
                'message': 'Post updated successfully!',
                'post': data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request:Request, id:int, *args, **kwargs):
        post = get_object_or_404(Post, pk=id)
        post.delete()
        return Response(data={'message': 'Post deleted successfully!'}, status=status.HTTP_200_OK)
    

# *********Generic API View and Model Mixins for creating and listing posts ****************
class PostListCreatGenericAPIViews(generics.GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    """generic api views for creating and listing posts """
  
    serializer_class = PostSerializer
    permission_classes=[ IsLoggedIn]
    queryset = Post.objects.all()

    def get(self, request:Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request:Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user) 
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    


# *********Generic API View and Model Mixins for getting details, updating and deleting post ****************
class PostRetrieveUpdateDeleteGenericAPIView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    """generic api views for getting details, updating and deleting post """
    serializer_class = PostSerializer
    permission_classes=[ IsLoggedIn, IsOwner]
    queryset = Post.objects.all()

    def get(self, request:Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request:Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request:Request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    


#***********Using ViewSets and Routers for creating and listing posts API************
    
class PostViewSets(viewsets.ViewSet):
    
    def list(self, request:Request):
        queryset = Post.objects.all()
        serializer = PostSerializer(instance= queryset, many=True)
        response= {
            'message': 'Posts',
            'data': serializer.data
        }
        return Response(data= response, status=status.HTTP_200_OK)
    
    def create(self, request:Request):
        data = request.data
        serializer = PostSerializer(data= data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Post created successfully!',
                'data': serializer.data
            }
            return Response(data= response, status=status.HTTP_201_CREATED)
        else:
            return Response(data= serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def retrieve(self, request:Request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(instance= post)
        response = {
            'message': 'Post details',
            'data': serializer.data
        }
        return Response(data= response, status=status.HTTP_200_OK)
    
    def update(self, request:Request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        data = request.data
        serializer = PostSerializer(instance=post, data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                'message': 'Post updated successfully!',
                'data': serializer.data
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request:Request, pk=None):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return Response(data={'message': 'Post deleted successfully!'}, status=status.HTTP_200_OK)




#***********Using Model ViewSets and Routers for posts CRUP APIs************
class PostModelViewSets(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    


class ListPostsForAuthor(generics.ListAPIView,mixins.ListModelMixin):
    
    queryset= Post.objects.all()
    serializer_class = PostSerializer
    permission_classes=[ IsLoggedIn, IsOwner]
    
    
    def get_queryset(self):
        
        
        ###### Filtering using query parameters ########
        username =self.request.query_params.get('username') or None
        
        print(f"Query parameter is {username}")
        
        if username is not None:
            return Post.objects.filter(author__email=username)
        
        else:
            queryset = Post.objects.all()
            return queryset
        
        
        
        ###### Filtering using path parameters ########
        # username= self.kwargs.get('username')
        # return Post.objects.filter(author__email=username)
    
    
    
         ###### Filtering using logged in user ########
        # return Post.objects.filter(author=self.request.user)
    
    
    
    # def get(self, request:Request, *args, **kwargs):
    #     # queryset = self.get_queryset().filter(author=request.user)
    #     # serializer = self.serializer_class(instance= queryset, many=True)
    #     # return Response(data= serializer.data, status=status.HTTP_200_OK)
        
    #     return self.list(request, *args, **kwargs)
    
    



    

   