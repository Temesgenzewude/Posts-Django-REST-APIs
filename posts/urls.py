from . import views

from django.urls import path

urlpatterns = [
  
    path('home', views.homePage, name='home'),
    
    path('', views.PostListCreatGenericAPIViews.as_view(), name='posts'),
    # path('<int:id>/', views.PostRetrieveUpdateDeleteClassBasedAPIView.as_view(), name='post-details'),
    path('<int:pk>/', views.PostRetrieveUpdateDeleteGenericAPIView.as_view(), name='post-details'),

    # path('<int:id>', views.get_post_by_id, name='post-details'),

    # path('update/<int:id>', views.update_post, name='update-post'),
    # path('delete/<int:id>', views.delete_post, name='delete-post'),
]