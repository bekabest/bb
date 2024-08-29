from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from django.contrib.auth import get_user_model
from .models import Post, Comment, Rating
from .serializers import UserSerializer, PostSerializer, CommentSerializer, RatingSerializer
from .utils import send_telegram_message

class PostViewSet(viewsets.ModelViewSet):
    ...
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        post = self.get_object()
        send_telegram_message(post.author.telegram_chat_id, f"Ваш пост успешно опубликован: {post.text[:20]}")
        return response

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        # Тут добавьте код для отправки уведомления в Telegram
        # Например, вызов функции отправки уведомления в Телеграм
        return response

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        rating = Rating.objects.filter(post=request.data['post'], user=request.user).first()
        if rating:
            rating.rating = request.data['rating']
            rating.save()
            return Response(status=status.HTTP_200_OK)
        return super().create(request, *args, **kwargs)
