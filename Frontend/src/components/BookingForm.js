import React, { useState } from 'react';
import axios from 'axios';

function BookingForm({ eventId, ticketPrice }) {
  const [ticketQuantity, setTicketQuantity] = useState(1);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Retrieve the token from localStorage
    const token = localStorage.getItem("authTokens");
    if (!token) {
      setError("You must be logged in to make a booking.");
      return;
    }

    const accessToken = JSON.parse(token).access;

    try {
      const response = await axios.post(
        'http://localhost:8000/api/bookings/',
        {
          event: eventId,
          ticket_quantity: ticketQuantity,
        },
        {
          headers: {
            'Authorization': `Bearer ${accessToken}`,  // Pass the token here
            'Content-Type': 'application/json',
          }
        }
      );
      
      setSuccess(true);
    } catch (error) {
      setError(error.response?.data?.error || "An error occurred.");
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {success ? (
        <p>Booking successful!</p>
      ) : (
        <>
          <div>
            <label>Ticket Quantity:</label>
            <input
              type="number"
              value={ticketQuantity}
              onChange={(e) => setTicketQuantity(e.target.value)}
            />
          </div>
          <button type="submit">Book Now</button>
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </>
      )}
    </form>
  );
}

export default BookingForm;
