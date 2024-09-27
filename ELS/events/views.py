from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Event, Booking
from .forms import EventForm, BookingForm
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

def home(request):
    return render(request, 'events/home.html')

@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

@login_required
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_detail(request, pk):
    event = Event.objects.get(pk=pk)
    return render(request, 'events/event_detail.html', {'event': event})

@login_required
def edit_event(request, pk):
    event = Event.objects.get(pk=pk)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm(instance=event)
    return render(request, 'events/edit_event.html', {'form': form})

@login_required
def delete_event(request, pk):

    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':

        event.delete()

        return redirect('event_list')  # Redirect to the event list page

    return render(request, 'events/delete_event.html', {'event': event})

@login_required
def make_booking(request, pk):

    event = Event.objects.get(id=pk)

    if request.method == 'POST':

        ticket_quantity = int(request.POST.get('ticket_quantity'))

        if ticket_quantity > event.available_tickets:

            return render(request, 'events/make_booking.html', {

                'event': event,

                'error_message': 'Not enough tickets available.'

            })

        booking = Booking(user=request.user, event=event, ticket_quantity=ticket_quantity)

        booking.save()

        return redirect('home')

    return render(request, 'events/make_booking.html', {'event': event})

@login_required
def booking_success(request):
    return render(request, 'events/booking_success.html')

def view_bookings(request, event_id):
    event = Event.objects.get(pk=event_id)
    bookings = Booking.objects.filter(event=event)
    context = {
        'event': event,
        'bookings': bookings
    }
    return render(request, 'events/view_bookings.html', context)

@login_required

def my_bookings(request):

    bookings = Booking.objects.filter(user=request.user)

    events = [booking.event for booking in bookings]

    return render(request, 'bookings/my_bookings.html', {'events': events})

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EventSerializer
from .models import Event
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Event, Booking
from .serializers import EventSerializer

class EventListView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')  # Get user_id from query params
        location = request.query_params.get('location', '')
        date = request.query_params.get('date', '')
        month = request.query_params.get('month', '')
        year = request.query_params.get('year', '')

        events = Event.objects.all()

        if user_id:
            # Exclude events that the user has booked
            booked_events = Booking.objects.filter(user_id=user_id).values_list('event_id', flat=True)
            events = events.exclude(id__in=booked_events)

        if location:
            events = events.filter(location__icontains=location)

        if date:
            events = events.filter(date=date)

        if month:
            # Filtering by month regardless of year
            events = events.filter(date__month=month)

        if year:
            events = events.filter(date__year=year)

        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailView(APIView):
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_booking(request):
    user = request.user
    event_id = request.data.get('event')
    ticket_quantity = request.data.get('ticket_quantity')

    if not event_id or not ticket_quantity:
        return Response({"error": "Missing event or ticket quantity"}, status=400)

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)

    booking = Booking.objects.create(
        user=user,
        event=event,
        ticket_quantity=ticket_quantity,
        total_cost=event.ticket_price * int(ticket_quantity)
    )
    
    return Response({"message": "Booking successful"}, status=201)

# views.py
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Booking
from .serializers import BookingSerializer

@api_view(['GET'])
def user_bookings(request, user_id):
    bookings = Booking.objects.filter(user_id=user_id)
    data = []
    
    for booking in bookings:
        data.append({
            'id': booking.id,
            'event': booking.event.name,
            'event_date': booking.event.date,  # Event date
            'ticket_quantity': booking.ticket_quantity,
            'total_cost': booking.total_cost,
        })
    
    return Response(data)

# views.py
from rest_framework.generics import RetrieveAPIView
from .models import Booking
from .serializers import BookingSerializer

class BookingDetailView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

# views.py
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Booking
from .serializers import BookingSerializer

class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            if booking.user != request.user:
                return Response({"error": "You do not have permission to cancel this booking"}, status=status.HTTP_403_FORBIDDEN)
            booking.delete()
            return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)



    
