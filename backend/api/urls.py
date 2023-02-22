from django.urls import path, include
from rest_framework import routers
from .views import UserListView, EventViewSet

router = routers.SimpleRouter()
router.register(r'events', EventViewSet)

urlpatterns = router.urls

urlpatterns += [
    path('users/', UserListView.as_view(), name="users_list")
]