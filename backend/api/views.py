from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import views, authentication, status
from rest_framework.response import Response
from account.models import User
from .serializers import UserSerializer, EventSerializer
from events.models import Event

# Create your views here.
class UserListView(ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class =  UserSerializer
    permission_classes = [IsAuthenticated]


# Viewsets for Event
# class EventViewSet(ModelViewSet):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer



# Using APIView 
class EventList(views.APIView):
    # auhtentication_classes = [authentication.TokenAuthentication]
    # serializer_class = EventSerializer

    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(views.APIView):
    def get(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    def delete(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.delete()
        return Response(status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    


    

# # Generic Views
# class EventList(ListAPIView):
#     queryset = Event.objects.all()
#     serializer_class = EventSerializer
