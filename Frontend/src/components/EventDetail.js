import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import BookingForm from './BookingForm';

function EventDetail() {
  const { eventId } = useParams();  // Get the event ID from the route
  console.log(`eventId: ${eventId}`); // Log the eventId value for debugging

  const [event, setEvent] = useState({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!eventId) {
      setError('Event ID is required');
      setLoading(false);
      return;
    }

    // Fetch the event details from the backend using the eventId
    axios.get(`http://localhost:8000/api/events/${eventId}/`)
      .then(response => {
        setEvent(response.data);  // Set the event data
        setLoading(false);
      })
      .catch(error => {
        setError(error.message);  // Capture error message
        setLoading(false);
      });
  }, [eventId]);

  return (
    <div>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p>Error: {error}</p>
      ) : (
        <div>
          <h2>{event.name}</h2>
          <p><strong>Description:</strong> {event.description}</p>
          <p><strong>Date:</strong> {event.date}</p>
          <p><strong>Time:</strong> {event.time}</p>
          <p><strong>Location:</strong> {event.location}</p>
          <p><strong>Ticket Capacity:</strong> {event.ticket_capacity}</p>
          <p><strong>Available Tickets:</strong> {event.available_tickets}</p>
          <p><strong>Ticket Price:</strong> {event.ticket_price}</p>
          {/* Pass eventId and ticketPrice to BookingForm */}
          <BookingForm eventId={event.id} ticketPrice={event.ticket_price} />
        </div>
      )}
    </div>
  );
}

export default EventDetail;
