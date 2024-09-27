import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

const BookingDetails = () => {
  const { id } = useParams(); // Get booking ID from URL parameters
  const [booking, setBooking] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [cancelled, setCancelled] = useState(false);

  useEffect(() => {
    // Fetch booking details by ID
    axios.get(`http://localhost:8000/api/bookings/${id}/`)
      .then(response => {
        setBooking(response.data);
        setLoading(false);
      })
      .catch(error => {
        console.error(error);
        setError('Failed to fetch booking details');
        setLoading(false);
      });
  }, [id]);

  const handleCancel = async () => {
    // Retrieve the token from localStorage
    const token = localStorage.getItem("authTokens");
    if (!token) {
      setError("You must be logged in to cancel a booking.");
      return;
    }

    const accessToken = JSON.parse(token).access;

    try {
      const response = await axios.delete(
        `http://localhost:8000/api/cancel-booking/${id}/`,
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,  // Pass the token here
            'Content-Type': 'application/json',
          }
        }
      );
      
      setCancelled(true);
    } catch (error) {
      setError(error.response?.data?.error || "An error occurred.");
    }
  };

  if (loading) return <p>Loading booking details...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div>
      <h2>Booking Details</h2>
      {booking ? (
        <div>
          <p><strong>Event:</strong> {booking.event_name}</p>
          <p><strong>Date:</strong> {new Date(booking.event_date).toLocaleDateString()}</p>
          <p><strong>Ticket Quantity:</strong> {booking.ticket_quantity}</p>
          <p><strong>Total Cost:</strong> ${booking.total_cost}</p>
          <p><strong>Location:</strong> {booking.event_location}</p>
          <p><strong>Notes:</strong> {booking.event_description}</p>
          <p><strong>Time:</strong> {booking.event_time}</p>
          {/* You can add more booking details here */}
          {!cancelled && (
            <button type="button" onClick={handleCancel}>Cancel Booking</button>
          )}
          {cancelled && (
            <p>Booking cancelled!</p>
          )}
        </div>
      ) : (
        <p>No booking details found.</p>
      )}
    </div>
  );
};

export default BookingDetails;