from django.urls import path, include
from rest_framework import routers
from .views import UserListView, EventList, EventDetailView, EventListGenric, EventModelViewSet

router = routers.SimpleRouter()
router.register(r'events', EventModelViewSet)

# urlpatterns = router.urls

urlpatterns = [
    path('users/', UserListView.as_view(), name="users_list"),
    path('', include(router.urls))
    # path('events/', EventList.as_view(), name='event_list'),
    # path('event/<int:pk>', EventDetailView.as_view(), name="detail_event"),
    # path('event/create-list', EventListGenric.as_view(), name='list-create')

]