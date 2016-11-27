from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField,
)
from posts.models import Post

post_detail_url = HyperlinkedIdentityField(
    view_name='posts-api:detail',
    lookup_field='slug',
)


class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['url', 'user', 'title', 'content', 'publish']

    def get_user(self, obj):
        return str(obj.user.username)


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = SerializerMethodField()
    main_image = SerializerMethodField()
    html = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['url', 'id', 'user', 'main_image', 'html', 'title', 'slug', 'content', 'publish']

    def get_user(self, obj):
        return str(obj.user.username)

    def get_html(self, obj):
        return obj.get_markdown()

    def get_main_image(self, obj):
        try:
            main_image = obj.image.url
        except:
            main_image = None
        return main_image


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'publish']
