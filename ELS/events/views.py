from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import requests
import json
from decimal import Decimal
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from .models import Event, Booking
from .serializers import EventSerializer, BookingSerializer
from django.utils import timezone
from datetime import date

class BookingDetailView(RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer


def send_booking_email(user, event, action):
    subject = f"Booking {action.capitalize()} Confirmation"
    message = f"""
    Dear {user.username},

    Your booking for the event '{event.name}' has been {action}.

    Event Details:
    Name: {event.name}
    Date: {event.date}
    {"Ticket Quantity: " + str(Booking.objects.get(user=user, event=event).ticket_quantity) if action == "created" else ""}
    {"Total Cost: $" + str(Booking.objects.get(user=user, event=event).total_cost) if action == "created" else ""}

    Thank you for using our service!

    Best regards,
    The Booking Team
    """
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, from_email, recipient_list)


class EventListView(APIView):
    def get(self, request):
        user_id = request.query_params.get('user_id')
        location = request.query_params.get('location', '')
        date = request.query_params.get('date', '')
        month = request.query_params.get('month', '')
        year = request.query_params.get('year', '')
        
        # Get current date
        current_date = timezone.now().date()
        
        # Filter events to include only upcoming events
        events = Event.objects.filter(date__gte=current_date)
        
        if user_id:
            booked_events = Booking.objects.filter(user_id=user_id).values_list('event_id', flat=True)
            events = events.exclude(id__in=booked_events)
        
        if location:
            events = events.filter(location__icontains=location)
        
        if date:
            events = events.filter(date=date)
        
        if month:
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
    
    # Send creation email
    send_booking_email(user, event, "created")
    
    return Response({"message": "Booking successful"}, status=201)


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


class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk)
            if booking.user != request.user:
                return Response({"error": "You do not have permission to cancel this booking"}, status=status.HTTP_403_FORBIDDEN)
            event = booking.event
            booking.delete()
            # Send cancellation email
            send_booking_email(request.user, event, "cancelled")
            return Response({"message": "Booking cancelled successfully"}, status=status.HTTP_200_OK)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)
    

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def create_booking(request):
#     user = request.user
#     event_id = request.data.get('event')
#     ticket_quantity = request.data.get('ticket_quantity')

#     if not event_id or not ticket_quantity:
#         return Response({"error": "Missing event or ticket quantity"}, status=400)

#     try:
#         event = Event.objects.get(id=event_id)
#     except Event.DoesNotExist:
#         return Response({"error": "Event not found"}, status=404)

#     # Calculate total cost
#     total_cost = event.ticket_price * int(ticket_quantity)

#     # Create a new booking with 'pending' status
#     booking = Booking.objects.create(
#         user=user,
#         event=event,
#         ticket_quantity=ticket_quantity,
#         total_cost=total_cost,
#         status='pending'
#     )
    
#     # Prepare payment payload for PesePay, converting total_cost to float
#     payment_payload = {
#         'amount': float(total_cost),  # Convert Decimal to float
#         'currency': 'USD',  # Adjust as needed
#         'reference': f'TICKET-{booking.id}',
#         'email': user.email,
#         'callback_url': 'http://localhost:3000/',
#         'return_url': 'http://localhost:3000/',
#         'merchant_id': settings.PESEPAY_MERCHANT_ID
#     }

#     # Set the headers for the PesePay API request
#     headers = {
#         'Authorization': f'Bearer {settings.PESEPAY_API_KEY}',
#         'Content-Type': 'application/json'
#     }

#     # Send payment request to PesePay
#     response = requests.post(settings.PESEPAY_API_URL, json=payment_payload, headers=headers)

#     if response.status_code == 200:
#         payment_data = response.json()
#         booking.payment_id = payment_data.get('payment_id')
#         booking.save()
        
#         # Send creation email
#         send_booking_email(user, event, "created")
        
#         return Response({
#             'message': 'Booking successful',
#             'payment_url': payment_data.get('payment_url')
#         }, status=201)
#     else:
#         # Log the response text to understand the error
#         print("PesePay Error Response:", response.text)
#         return Response({
#             'error': 'Failed to initiate payment',
#             'details': response.text  # Return the error details from PesePay
#         }, status=400)


# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from .models import Booking
# import json

# @csrf_exempt
# def payment_callback(request):
#     if request.method == 'POST':
#         try:
#             # Parse callback data from PesePay
#             callback_data = json.loads(request.body)
            
#             # Extract the booking reference and booking ID
#             booking_reference = callback_data.get('reference', '')
#             booking_id = booking_reference.split('-')[1] if '-' in booking_reference else None

#             if not booking_id:
#                 return JsonResponse({'error': 'Invalid booking reference'}, status=400)
            
#             # Retrieve the booking record
#             try:
#                 booking = Booking.objects.get(id=booking_id)
#             except Booking.DoesNotExist:
#                 return JsonResponse({'error': 'Booking not found'}, status=404)

#             # Update booking based on payment status
#             payment_status = callback_data.get('status', '').lower()
            
#             if payment_status == 'success':
#                 booking.status = 'paid'
#                 booking.save()
#                 print(f"Payment successful for booking {booking_id}")
#             elif payment_status == 'failed':
#                 booking.status = 'failed'
#                 booking.save()
#                 print(f"Payment failed for booking {booking_id}")
#             else:
#                 return JsonResponse({'error': 'Unknown payment status'}, status=400)
            
#             return JsonResponse({'status': 'success'})
#         except json.JSONDecodeError:
#             return JsonResponse({'error': 'Invalid JSON data'}, status=400)
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=500)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

