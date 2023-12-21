
from django.urls import path
from.import views
urlpatterns = [
    path('', views.create_participant_and_vehicle, name='participant'),
   
]
