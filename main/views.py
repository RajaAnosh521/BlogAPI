from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import BlogPost
from .serializers import *

# Create your views here.
class BlogView(APIView):
    permission_classes = [IsAuthenticated] 
    def get(self, request):
        # Get the blog posts from the database
        blog_posts = BlogPost.objects.all() 
        serializer = BlogSerializer(blog_posts, many=True)
        return Response({"data": serializer.data}) 
    

class BlogPostCreateView(APIView):
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        serializer = BlogSerializer(data=request.data) 
        if serializer.is_valid():
            serializer.save(author=request.user)  # Automatically assign the logged-in user as the author
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BlogPostUpdateView(APIView):
    permission_classes = [IsAuthenticated] 
    def put(self, request, pk):
        blog_post = BlogPost.objects.get(pk=pk)
        serializer = BlogSerializer(blog_post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
    
class BlogPostDeleteView(APIView):
    permission_classes = [IsAuthenticated] 
    def delete(self, request, pk):
        try:
            blog_post = BlogPost.objects.get(pk=pk)
            blog_post.delete()
            return Response({"message": "Successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except BlogPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)