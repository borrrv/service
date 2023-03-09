from django.shortcuts import render
from .models import Tag
from rest_framework.decorators import action
from .serializers import TagSerializers
from rest_framework.response import Response
from rest_framework import viewsets


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
    pagination_class = None