# Django
from django.shortcuts import get_object_or_404

# Django REST Framework
from rest_framework import filters, generics, status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response  import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from rest_framework.views import APIView

# Django Filters
from django_filters.rest_framework import DjangoFilterBackend
from watchlist_app.api.pagination import WatchlistFilterPagination

# Local imports
from watchlist_app.models import Review, Watchlist, StreamPlatform
from watchlist_app.api.permissions import IsAdminOrReadOnly, IsReviewUserOrReadOnly
from watchlist_app.api.serializers import ReviewSerializer, StreamPlatformSerializer, WatchlistSerializer
from watchlist_app.api.throttling import ReviewCreateThrottle, ReviewListThrottle


# Class based view
# Watchlist

class WatchlistFilterView(generics.ListAPIView):
    queryset = Watchlist.objects.all()
    serializer_class = WatchlistSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    pagination_class = WatchlistFilterPagination
    search_fields  = ['title', '=platform__name']
    ordering_fields = ['average_rating',]
    

class WatchlistView(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    
    def get(self, request):
        watchlists = Watchlist.objects.all()
        serializer = WatchlistSerializer(watchlists, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = WatchlistSerializer(data=request.data, many=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class WatchlistDetailView(APIView):
    permission_classes = (IsAuthenticated, IsAdminOrReadOnly)
    
    def get(self, request, pk):
        watchlist = get_object_or_404(Watchlist, pk=pk)
        serializer = WatchlistSerializer(watchlist)
        return Response(serializer.data)
    
    def put(self, request, pk):
        watchlist = get_object_or_404(Watchlist, pk=pk)
        serializer = WatchlistSerializer(watchlist, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
    def delete(self, request, pk):
        watchlist = get_object_or_404(Watchlist, pk=pk)
        watchlist.delete()
        return Response('Item deleted', status=status.HTTP_204_NO_CONTENT)

# Generics Views
class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthenticated,)
    throttle_classes = (ReviewCreateThrottle, AnonRateThrottle)
    
    def get_queryset(self):
        return Review.objects.all()
    
    def perform_create(self, serializer):
        watchlist = get_object_or_404(Watchlist, pk=self.kwargs['pk'])
        
        review_user = self.request.user
        review_queryset = Review.objects.filter(watchlist=watchlist, review_user=review_user)
        
        if review_queryset.exists():
            raise ValidationError('You have already reviewed this movie')
        
        if watchlist.number_of_ratings == 0:
            watchlist.average_rating = serializer.validated_data['rating']
        else:
            watchlist.average_rating = (watchlist.average_rating + serializer.validated_data['rating']) / 2
        
        watchlist.number_of_ratings += 1
        serializer.is_valid(raise_exception=True)
        watchlist.save()
        serializer.save(watchlist=watchlist, review_user=review_user)

class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    throttle_classes = (ReviewListThrottle, AnonRateThrottle)
    
    def get_queryset(self):
        return Review.objects.filter(watchlist=self.kwargs['pk'])

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (IsReviewUserOrReadOnly,)
    throttle_classes = (ScopedRateThrottle,)
    throttle_scope = 'review-detail'
    
class UserReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username', 'active']
    
    # def get_queryset(self):
    #     username = self.kwargs['username']
    #     return Review.objects.filter(review_user__username=username)
    
    # def get_queryset(self):
    #     username = self.request.query_params.get('username', None)
    #     return Review.objects.filter(review_user__username=username)
    


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = (IsAdminOrReadOnly,)