from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.response import Response

from notifications.models import Notification
from .serializers import NotificationSerializer




class NotificacaoViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def get_unread_notifications(self,user):
        unread_notifications = Notification.objects.unread().filter(recipient=user)
        return unread_notifications

    def list(self, request, *args, **kwargs):
        queryset = self.get_unread_notifications(request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class CountNotificacaoViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,TokenAuthentication]

    def count_notifications_unread_user(self,user):
        unread_notifications = Notification.objects.unread().filter(recipient=user)
        return unread_notifications.count()

    def list(self, request, *args, **kwargs):
        print(request.user)
        queryset = self.count_notifications_unread_user(request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)