from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import BlogPostSerializer, CommentSerializer, BlogPostUpdateSerializer
from .models import BlogPost, Comment
from rest_framework import permissions

class CreateBlogPostView(APIView):
    permission_classes = [ IsAuthenticated] 
    def post(self, request):
        serializer = BlogPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, blog_post_id):
        try:
            blog_post = BlogPost.objects.get(id=blog_post_id)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, blog_post=blog_post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListBlogPostsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        blog_posts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blog_posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ListCommentsView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, blog_post_id):
        try:
            blog_post = BlogPost.objects.get(id=blog_post_id)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            comments = Comment.objects.filter(blog_post__id=blog_post_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comments not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateDeleteBlogPostView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, blog_post_id):
        try:
            blog_post = BlogPost.objects.get(id=blog_post_id)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if blog_post.author != request.user:
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = BlogPostUpdateSerializer(blog_post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, blog_post_id):
        try:
            blog_post = BlogPost.objects.get(id=blog_post_id)
        except BlogPost.DoesNotExist:
            return Response({'error': 'Blog post not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if blog_post.author != request.user:
            return Response({'error': 'You are not authorized to perform this action'}, status=status.HTTP_403_FORBIDDEN)
        
        blog_post.delete()
        return Response({'message': 'Blog post deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

