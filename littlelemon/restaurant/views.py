import json
from datetime import datetime
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Menu, Booking
from .serializers import MenuSerializer, BookingSerializer
from .forms import BookingForm

# Web-based views
def index(request):
  return render(request, 'index.html')

def about(request):
  return render(request, 'about.html')

def menu(request):
  menu_data = Menu.objects.all()
  main_data = {"menu": menu_data}
  return render(request, 'menu.html', {"menu": main_data})

def menu_item(request, pk=None):
  if pk:
      menu_item = Menu.objects.get(pk=pk)
  else:
      menu_item = ""
  return render(request, 'menu_item.html', {"menu_item": menu_item})

def book(request):
  form = BookingForm()
  if request.method == 'POST':
      form = BookingForm(request.POST)
      if form.is_valid():
          form.save()
  context = {'form':form}
  return render(request, 'book.html', context)

@csrf_exempt
def bookings(request):
  if request.method == 'POST':
      data = json.load(request)
      value = datetime.strptime(data['BookingDate'], "%Y-%m-%dT%H:%M")
      exist = Booking.objects.filter(BookingDate__year=value.year,
                                     BookingDate__month=value.month,
                                     BookingDate__day=value.day,
                                     BookingDate__hour=value.hour).exists()
      if exist == False:
          booking = Booking(
              Name=data['Name'],
              No_of_guests=data['No_of_guests'],
              BookingDate=data['BookingDate'],
          )
          booking.save()
      else:
          return HttpResponse("{'error':1}", content_type='application/json')

  date = request.GET.get('date', datetime.today().date().isoformat())
  year, month, day = date.split('-')
  bookings = Booking.objects.all().filter(BookingDate__year=year, BookingDate__month=month, BookingDate__day=day)

  booking_json = serializers.serialize('json', bookings)
  return HttpResponse(booking_json, content_type='application/json')

def reservations(request):
    bookings = Booking.objects.all()
    return render(request, 'bookings.html',{"bookings":bookings})

# API views
class MenuItemsView(generics.ListCreateAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer

  def get_permissions(self):
    permission_classes = []
    if self.request.method != 'GET':
      permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]

class SingleMenuItemView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Menu.objects.all()
  serializer_class = MenuSerializer

  def get_permissions(self):
    permission_classes = []
    if self.request.method != 'GET':
      permission_classes = [IsAdminUser]
    return [permission() for permission in permission_classes]

class BookingViewSet(viewsets.ModelViewSet):
  queryset = Booking.objects.all()
  serializer_class = BookingSerializer
  permission_classes = [IsAuthenticatedOrReadOnly]
