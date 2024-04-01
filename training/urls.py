
from django.urls import path
from .views import ActivityView, UserActivityLogView, UserActivityView

urlpatterns = [
    path('activities/all', ActivityView.as_view(), name="all_activities"),
    path('activities', UserActivityView.as_view(), name="user_activities"),
    path('activity_logs', UserActivityLogView.as_view(), name="activity_logs")
]