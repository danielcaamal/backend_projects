# Django REST Framework
from platform import platform
from rest_framework import serializers

# Local imports
from watchlist_app.models import Watchlist, StreamPlatform, Review


# Review Serializer
class ReviewSerializerS(serializers.ModelSerializer):
    
    class Meta:
        model = Review
        fields = ['rating', 'description']

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        exclude = ('watchlist',)


# Model Serializer
class WatchlistSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializerS(many=True, read_only=True)
    platform = serializers.CharField(source='platform.name', read_only=True)

    class Meta:
        model = Watchlist
        fields = "__all__"
class StreamPlatformSerializer(serializers.ModelSerializer):
    watchlist = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        fields = "__all__"