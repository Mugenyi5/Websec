# myapp/views.py
from django.shortcuts import render, redirect
from .forms import ParticipantForm, VehicleForm
import logging

def create_participant_and_vehicle(request):
    participant_form = ParticipantForm(request.POST or None, prefix='participant')
    vehicle_form = VehicleForm(request.POST or None, prefix='vehicle')

    participant = None  

    if request.method == 'POST':
        if participant_form.is_valid():
            participant = participant_form.save()
            participant_form = ParticipantForm(prefix='participant')  # Clear participant form fields

    if request.method == 'POST':
        if vehicle_form.is_valid():
            vehicle = vehicle_form.save()
            vehicle_form = VehicleForm(prefix='vehicle') 


    return render(
        request,
        'participant_vehicle.html',
        {'participant_form': participant_form, 'vehicle_form': vehicle_form}
    )
# views.py

def my_view(request):
    # Your view logic here
    logging.debug('This is a debug message')
    logging.info('This is an info message')
    logging.warning('This is a warning message')
    logging.error('This is an error message')
    logging.critical('This is a critical message')

