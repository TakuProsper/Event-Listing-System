from django.db import models
from users.models import CustomUser

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    ticket_capacity = models.IntegerField()
    available_tickets = models.IntegerField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    num_tickets_sold = models.IntegerField(default=0) 

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):

        self.available_tickets = self.ticket_capacity - self.num_tickets_sold

        super().save(*args, **kwargs)    
    
class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)
    ticket_quantity = models.IntegerField()  
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)  

    # Payment-related fields
    payment_id = models.CharField(max_length=100, blank=True, null=True)  # To store the payment gateway's transaction ID
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed')
    ], default='pending')

    def save(self, *args, **kwargs):
        # Ensure ticket_quantity is an integer
        self.ticket_quantity = int(self.ticket_quantity)
        
        # Calculate the total cost of the booking based on event's ticket price
        self.total_cost = self.event.ticket_price * self.ticket_quantity
        
        super().save(*args, **kwargs)

        # Update the num_tickets_sold field in the Event model
        self.event.num_tickets_sold += self.ticket_quantity
        self.event.save()

    def __str__(self):
        return f"Booking for {self.event.name} by {self.user.username} - Status: {self.status}"
