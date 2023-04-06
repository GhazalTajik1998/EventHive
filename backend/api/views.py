from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework import views, authentication, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from account.models import User
from .serializers import UserSerializer, EventSerializer
from .permissions import AuthorOrReadOnly, UserOrReadOnly
from .tasks import event_reserved
from events.models import Event



# Create your views here.
class UserModelViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class =  UserSerializer
    permission_classes = [UserOrReadOnly, IsAuthenticated]

    @action(detail=True, methods=['get'])
    def reserved_events(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)
        queryset = Event.objects.filter(subscriptions=user)
        serializer = EventSerializer(queryset, many=True)
        return Response(serializer.data)
    

# Viewsets for Event
class EventModelViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [AuthorOrReadOnly]
    

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)



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
    
    





# Views in Function Based way

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_item(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return Response(EventSerializer(event).data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):
    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def events_list(request):
    events = Event.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def udpate_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    serializer = EventSerializer(event, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Generic Views
class EventListGenric(ListModelMixin, CreateModelMixin, GenericAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    



# ----------------------------------------------------------------------------------- #

class ReserveEvent(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        event = get_object_or_404(Event, pk=pk)
        event.subscriptions.add(request.user)
        event_reserved.delay(event.id)
        serializer = EventSerializer(event)
        return Response(serializer.data)
    


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_subscription(request, pk):

    event = get_object_or_404(Event, pk=pk)
    event.subscriptions.remove(request.user)
    serializer = EventSerializer(event)
    return Response(serializer.data)