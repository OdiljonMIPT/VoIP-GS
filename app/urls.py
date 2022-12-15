from django.urls import path
from .views import home, agent, agent_detail

urlpatterns = [
    path('', home),
    path('agent/', agent),
    path('agent/<int:pk>', agent_detail),
]
