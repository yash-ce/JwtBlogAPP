from django.urls import path

from .views import *

urlpatterns = [
    path('create/', CreateBlogPostView.as_view(), name='create-blog-post'),
    path('<int:blog_post_id>/comments/create/', CreateCommentView.as_view(), name='create-comment'),
    path('list/', ListBlogPostsView.as_view(), name='list-blog-posts'),
    path('<int:blog_post_id>/comments/list/', ListCommentsView.as_view(), name='list-comments'),
    path('<int:blog_post_id>/update/', UpdateDeleteBlogPostView.as_view(), name='update-blog-post'),

]
