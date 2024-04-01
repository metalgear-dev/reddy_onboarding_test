from datetime import datetime
from django.shortcuts import render
from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import ActivitySerializer, UserActivityLogSerializer, UserActivitySerializer
from .models import Activity, UserActivity, UserActivityLog, do_training
from rest_framework.decorators import permission_classes, api_view
from django.db.models import Sum, F

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
    

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def train_activity(request, user_activity_id):
    try:
        user_activity = UserActivity.objects.get(pk = user_activity_id)
    except UserActivity.DoesNotExist:
        return Response(
            status = status.HTTP_404_NOT_FOUND
        )
    
    # if the activity does not belong to user, it returns 403
    if user_activity.user != request.user:
        return Response(            
            status = status.HTTP_403_FORBIDDEN
        )
    
    # if the activity has already completed, it returns 400
    if user_activity.completed:
        return Response(            
            status = status.HTTP_400_BAD_REQUEST
        )
    
    # if the activity log is not created, it returns 400
    if UserActivityLog.objects.filter(user_activity__id = user_activity_id).count() == 0:
        return Response(
            status = status.HTTP_400_BAD_REQUEST
        )    
    
    # update the log
    log = UserActivityLog.objects.get(user_activity__id = user_activity_id)
    log.score = do_training()
    log.ended_at = datetime.now()
    log.save()

    # update the user activity
    user_activity.completed = True
    user_activity.save()

    return Response(
        UserActivityLogSerializer(log).data
    )

@api_view(['GET'])
@permission_classes([AllowAny])
def leader_board(request):
    logs = UserActivityLog.objects. \
        values('user_activity__user'). \
        annotate(total_score = Sum('score')). \
        annotate(username = F('user_activity__user__username')). \
        annotate(id = F('user_activity__user__id')). \
        order_by('-total_score') \
        
    return Response(logs)