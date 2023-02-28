from django.urls import path, include
from rest_framework import routers
from .views import UserListView, EventList, EventDetailView

# router = routers.SimpleRouter()
# router.register(r'events', EventViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('users/', UserListView.as_view(), name="users_list"),
    path('events/', EventList.as_view(), name='event_list'),
    path('event/<int:pk>', EventDetailView.as_view(), name="detail_event"),

]