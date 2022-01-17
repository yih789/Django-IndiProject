from rest_framework import  serializers
from .models import Content

class ContentSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    
    class Meta:
        model = Content
        fields = ('title', 'text', 'image')