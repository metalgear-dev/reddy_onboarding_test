from rest_framework import serializers

from training.models import Activity, UserActivity, UserActivityLog

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"


class UserActivitySerializer(serializers.ModelSerializer):
    activity = ActivitySerializer(read_only = True)
    activity_id = serializers.IntegerField(write_only = True)

    class Meta:
        model = UserActivity
        fields = (
            'id',
            'activity',
            'created_at',
            'updated_at',
            'completed',
            'activity_id'
        )
        extra_kwargs = {
            'completed': { 'read_only': True }
        }

    def create(self, validated_data):
        activity_id = validated_data.pop('activity_id')

        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

            try:
                activity = Activity.objects.get(pk = activity_id)

                # TODO: check if there is any activity created and not finished

                new_user_activity = UserActivity.objects.create(user = user, activity = activity)
                UserActivityLog.objects.create(user_activity = new_user_activity, score = 0, ended_at = None)
                return new_user_activity
            except:
                return serializers.ValidationError('Activity is not found')
        else:
            return serializers.ValidationError("Unauthenticated error")

    

class UserActivityLogSerializer(serializers.ModelSerializer):
    user_activity = UserActivitySerializer(read_only = True)

    class Meta:
        model = UserActivityLog
        fields = "__all__"


class LeaderBoardSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    total_score = serializers.IntegerField()
    username = serializers.StringRelatedField()