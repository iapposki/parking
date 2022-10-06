from email import message
from threading import Timer
from django.shortcuts import HttpResponseRedirect, get_object_or_404, render
from django.http import Http404, HttpResponse
from django.urls import reverse
from .config import *

from .models import ParkingSpace


def index(request):
    context = {}
    # return HttpResponse("Homepage of parking app")
    return render(request, 'parking/index.html', context)

def book(request):
    try:
        parking_space = ParkingSpace.objects.filter(availability=True, in_process=False)[0]
    except:
        raise Http404("Parking space is unavailable.")
    # print(parking_space)
    parking_space.in_process = True
    parking_space.save()

    t = Timer(float(booking_timeout_interval), in_process_timeout,[parking_space])
    t.start()

    context = {
        'parking_space':parking_space
    }
    return render(request, 'parking/book.html', context)

def confirmation(request, parking_address):
    parking_space = ParkingSpace.objects.get(parking_address=parking_address)
    if not parking_space.in_process:
        message = "Timed Out"
        return render(request, 'parking/book.html', {"message": message, 'parking_space':parking_space})
    if request.POST['is_confirmed'] == "Yes" and request.POST['vehicle_id']:
        parking_space.paid = True
        parking_space.in_process = False
        parking_space.vehicle_id = request.POST['vehicle_id']
        parking_space.availability = False
        parking_space.save()
        message = "Booking done at : " + parking_address
        return render(request, 'parking/book.html', {"message": message, 'parking_space':parking_space})
    # print(request.POST['is_confirmed'])
    parking_space.in_process = False
    parking_space.save()
    if not request.POST['vehicle_id']:
        message = "Vehicle ID not provided."
    else:
        message = "Unable to book at " + parking_address + ". Payment not confirmed."
    return render(request, 'parking/book.html', {"message": message, 'parking_space':parking_space})


def result(request):
    return render(request, 'parking/result.html')

def checkout_page(request):
    message = ""
    return render(request, 'parking/checkout.html', {"message" : message})

def checkout(request):
    vehicle_id = request.POST['vehicle_id']
    if vehicle_id:
        try :
            parking_space = ParkingSpace.objects.get(vehicle_id=vehicle_id)
            # print(parking_space.vehicle_id)
            set_parking_space_to_default(parking_space)
            message = "Vehicle checked out from parking space " + parking_space.parking_address 
        except:
            message = "Invalid vehicle ID"
    else:
        message = "Enter the vehicle ID."
    return render(request, 'parking/checkout.html', {"message":message})

def in_process_timeout(parking_space):
    parking_space = ParkingSpace.objects.get(parking_address=parking_space.parking_address)
    if not parking_space.paid:
        parking_space.in_process = False
        parking_space.save()

def set_parking_space_to_default(parking_space):
    parking_space.availability = True
    parking_space.paid = False
    parking_space.in_process = False
    parking_space.vehicle_id = ""
    parking_space.save()