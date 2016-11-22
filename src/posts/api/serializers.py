from rest_framework.serializers import ModelSerializer
from posts.models import Post


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'content', 'publish']
