from rest_framework.serializers import Serializer
from rest_framework.serializers import ModelSerializer
from .models import User

class userSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'name',
        ]