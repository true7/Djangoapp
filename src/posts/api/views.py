from rest_framework.generics import ListAPIView
from posts.models import Post
from .serializers import PostListSerializer


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
