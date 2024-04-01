
from django.urls import path
from .views import ActivityView, UserActivityLogView, UserActivityView, leader_board, train_activity

urlpatterns = [
    path('activities/leaderboard', leader_board, name="leader_board"),
    path('activities/all', ActivityView.as_view(), name="all_activities"),
    path('activities/<int:user_activity_id>/train', train_activity, name="train_activity"),
    path('activities', UserActivityView.as_view(), name="user_activities"),
    path('activity_logs', UserActivityLogView.as_view(), name="activity_logs")
]