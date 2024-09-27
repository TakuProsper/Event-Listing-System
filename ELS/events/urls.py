from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('create/', views.create_event, name='create_event'),
    path('list/', views.event_list, name='event_list'),
    path('<pk>/', views.event_detail, name='event_detail'),
    path('<pk>/edit/', views.edit_event, name='edit_event'),
    path('events/<pk>/make-booking/', views.make_booking, name='make_booking'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('events/<int:event_id>/bookings/', views.view_bookings, name='view_bookings'),
    path('events/<pk>/delete/', views.delete_event, name='delete_event'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    
     # API views

    path('api/events/', views.EventListView.as_view(), name='event_list_api'),

    path('api/events/<pk>/', views.EventDetailView.as_view(), name='event_detail_api'),
    path('api/bookings/', views.create_booking, name='create-booking'),
    path('api/users/<int:user_id>/bookings/', views.user_bookings),
    path('api/bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('api/cancel-booking/<pk>/', views.CancelBookingView.as_view(), name='cancel_booking'),

]