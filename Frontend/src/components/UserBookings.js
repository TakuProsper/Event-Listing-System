// UserBookings.js
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Calendar from 'react-calendar';
import { useNavigate } from 'react-router-dom';
import 'react-calendar/dist/Calendar.css';

const UserBookings = ({ userId }) => {
  const [bookings, setBookings] = useState([]);
  const [calendarBookings, setCalendarBookings] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    axios.get(`http://localhost:8000/api/users/${userId}/bookings/`)
      .then(response => {
        setBookings(response.data);
        // Map bookings to dates in 'calendarBookings'
        const bookingDates = response.data.map(booking => ({
          date: new Date(booking.event_date),  // Use event_date from API
          id: booking.id
        }));
        setCalendarBookings(bookingDates);
      })
      .catch(error => {
        console.error(error);
      });
  }, [userId]);

  // Handle date clicks in the calendar
  const handleDateClick = (date) => {
    const booking = calendarBookings.find(booking => 
      booking.date.toDateString() === date.toDateString()
    );
    if (booking) {
      // Navigate to the booking details page
      navigate(`/bookings/${booking.id}`);
    }
  };

  return (
    <div>
      <h2>My Bookings</h2>
      <Calendar
        onClickDay={handleDateClick}
        tileClassName={({ date, view }) => {
          // Highlight the days where the user has bookings
          if (view === 'month') {
            return calendarBookings.some(booking => 
              booking.date.toDateString() === date.toDateString()
            ) ? 'highlight' : null;
          }
        }}
      />
      <style>
        {`
          .highlight {
            background-color: #90EE90 !important;
            color: white !important;
          }
        `}
      </style>
    </div>
  );
};

export default UserBookings;
