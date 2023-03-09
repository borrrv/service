from django.shortcuts import render
from .models import Tag
from rest_framework.decorators import action
from .serializers import TagSerializers
from rest_framework.response import Response

@action(['GET'])
def get_tag(request):
    tags = Tag.objects.all()
    serializer = self.get_serializer(tags, many=True)
    return Response(serializer.data)