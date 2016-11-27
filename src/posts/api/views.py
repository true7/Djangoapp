from posts.models import Post
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from rest_framework.generics import (
    ListAPIView, RetrieveAPIView,
    DestroyAPIView, CreateAPIView,
    RetrieveUpdateAPIView,
)

from .serializers import (
    PostListSerializer, PostDetailSerializer,
    PostCreateUpdateSerializer,
)


class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ['title', 'content', 'user__username']
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            ).distinct()
        return queryset_list


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)