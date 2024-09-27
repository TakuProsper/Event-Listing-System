from django import forms
from .models import Event, Booking

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'description', 'date', 'time', 'location', 'ticket_capacity', 'ticket_price')
        
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ('ticket_quantity',)