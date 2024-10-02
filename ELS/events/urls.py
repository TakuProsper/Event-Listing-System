from django.urls import path
from . import views

urlpatterns = [
    #Events urls
    path('api/events/', views.EventListView.as_view(), name='event_list_api'),
    path('api/events/<pk>/', views.EventDetailView.as_view(), name='event_detail_api'),
    
    #Booking urls
    path('api/bookings/', views.create_booking, name='create-booking'),
    path('api/users/<int:user_id>/bookings/', views.user_bookings),
    path('api/bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('api/cancel-booking/<pk>/', views.CancelBookingView.as_view(), name='cancel_booking'),
    

]