from rest_framework import serializers
from .models import Event, Booking

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'description', 'date', 'time', 'location', 'ticket_capacity', 'available_tickets', 'ticket_price', 'num_tickets_sold']
        

class BookingSerializer(serializers.ModelSerializer):
    event_date = serializers.DateField(source='event.date', read_only=True)
    event_description = serializers.CharField(source='event.description', read_only=True)
    event_location = serializers.CharField(source='event.location', read_only=True)
    event_name = serializers.CharField(source='event.name', read_only=True)
    event_time = serializers.TimeField(source='event.time', read_only=True)

    class Meta:
        model = Booking
        fields = ['id', 'event', 'event_date', 'ticket_quantity', 'total_cost', 'event_description', 'event_location', 'event_name', 'event_time']


    def create(self, validated_data):
        
        return super().create(validated_data)

        
