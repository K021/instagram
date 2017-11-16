from django.http import Http404
from rest_framework import status, mixins, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from member.serializers import UserSerializer
from utils.permissions import IsAuthorOrReadOnly
from .models import Post
from .serializers import PostSerializer


# class PostList(APIView):
#     def get(self, *args, **kwargs):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(author=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    # self.create 함수 안에서 쓰인다
    # APIView 안에 있는 dispatch 안에 self.request = request가 들어있다.
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
    )

    # def get_object(self, pk):
    #     try:
    #         return Post.objects.get(pk=pk)
    #     except Post.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk, format=None):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(post)
    #     return Response(serializer.data)
    #
    # def put(self, request, pk, format=None):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(post, data=request.data)
    #     if request.user.is_authenticated and serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, pk, format=None):
    #     if request.user.is_authenticated:
    #         post = self.get_object(pk)
    #         post.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeToggle(generics.GenericAPIView):
    queryset = Post.objects.all()
    # url 의 그룹 이름이 <pk>로 되어 있기 때문에 self.get_object() 에서 알아서 해당 pk의 인스턴스를 가져온다
    # 그룹이름이 <post_pk>와 같이 pk가 아닐 경우, lookup_url_kwarg = 'post_pk' 라고 정의해주어야 한다

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        # user.liked_posts.filter
        # `instance in user.liked_posts.all():`
        if user.liked_posts.filter(pk=instance.pk):
            user.liked_posts.remove(instance)
            like_status = False
        else:
            user.liked_posts.add(instance)
            like_status = True
        data = {
            'user': UserSerializer(user).data,
            'post': PostSerializer(instance).data,
            'result': like_status,
        }
        return Response(data)
