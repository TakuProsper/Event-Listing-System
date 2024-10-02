import React, { useState } from 'react';
import axios from 'axios';

function BookingForm({ eventId, ticketPrice }) {
  const [ticketQuantity, setTicketQuantity] = useState(1);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false); // State for loading

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Retrieve the token from localStorage
    const token = localStorage.getItem("authTokens");
    if (!token) {
      setError("You must be logged in to make a booking.");
      return;
    }

    const accessToken = JSON.parse(token).access;

    setLoading(true); // Set loading to true when submitting

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
      setError(null); // Clear any previous errors
    } catch (error) {
      setError(error.response?.data?.error || "An error occurred.");
    } finally {
      setLoading(false); // Set loading to false when done
    }
  };

  return (
    <form onSubmit={handleSubmit} className='BookingForm'>
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
          <button className='btn button mt-4' type="submit" disabled={loading}>
            {loading ? "Processing..." : "Book Now"} {/* Change button text based on loading state */}
          </button>
          {error && <p style={{ color: 'red' }}>{error}</p>}
        </>
      )}
    </form>
  );
}

export default BookingForm;
