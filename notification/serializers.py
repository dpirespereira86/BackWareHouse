from rest_framework import serializers
from notifications.models import Notification

from Usuario.models import Usuario
from Usuario.serializers import UserNotificationSerializers



class NotificationSerializer(serializers.Serializer):
    actor = UserNotificationSerializers(Usuario, read_only=True)
    recipient = UserNotificationSerializers(Usuario, read_only=True)
    unread = serializers.BooleanField(read_only=True)
    verb = serializers.CharField(max_length=200)

    class Meta:
        model = Notification
        fields = ('verb')