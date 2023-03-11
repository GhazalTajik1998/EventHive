from django.urls import path, include
from rest_framework import routers
from .views import (
    UserModelViewSet,
    EventList, 
    EventDetailView, 
    EventListGenric, 
    EventModelViewSet,
    ReserveEvent,
    remove_subscription
)

router = routers.SimpleRouter()
router.register(r'events', EventModelViewSet)
router.register(r'users', UserModelViewSet)
# urlpatterns = router.urls

urlpatterns = [ 
    path('', include(router.urls)),
    path('reserve/event/<int:pk>', ReserveEvent.as_view(),name="reserve"),
    path('remove/event/<int:pk>', remove_subscription, name="remove_reserve")
    # path('events/', EventList.as_view(), name='event_list'),
    # path('event/<int:pk>', EventDetailView.as_view(), name="detail_event"),
    # path('event/create-list', EventListGenric.as_view(), name='list-create')

]