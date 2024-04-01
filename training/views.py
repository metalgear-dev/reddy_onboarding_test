from django.shortcuts import render
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ActivitySerializer, UserActivityLogSerializer, UserActivitySerializer
from .models import Activity, UserActivity, UserActivityLog

# Create your views here.

class ActivityView(
    mixins.ListModelMixin,
    generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ActivitySerializer
    queryset = Activity.objects.filter(is_active = True)

    def get(self, request):
        return self.list(request)

class UserActivityView(
    generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserActivitySerializer
    
    def get(self, request):
        queryset = UserActivity.objects.filter(user = request.user).order_by('-created_at')
        return Response(
            UserActivitySerializer(
                queryset,
                many = True
            ).data,
            status = status.HTTP_200_OK
        )

    def post(self, request):
        return self.create(request)

class UserActivityLogView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserActivityLogSerializer

    def get_queryset(self, request):
        return UserActivityLog.objects.filter(user_activity__user = request.user).order_by('-created_at')