from rest_framework import serializers
from .models import Ratings


class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ratings
        fields = ['student', 'xp']
