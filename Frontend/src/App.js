import React from 'react';
import { BrowserRouter, Routes, Route} from 'react-router-dom';
import EventDetail from './components/EventDetail';
import BookingForm from './components/BookingForm';
import LoginPage from './pages/LoginPage';
import UserDashboard from './pages/Dashboard'
import PrivateRoute from './utils/PrivateRoute'; 
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import RegisterPage from './pages/RegisterPage';
import Footer from './components/Footer';
import BookingDetails from './components/BookingDetails';
import UserBookings from './components/UserBookings';

function App() {
  return (
    
      <BrowserRouter>
      <AuthProvider>
        <div>
          <Navbar />
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/events/:eventId" element={<EventDetail />} />
            <Route path="/booking-form" element={<BookingForm />} />
            <Route path="/" element={<PrivateRoute><UserDashboard /></PrivateRoute>} />
            <Route path="/register" exact element={<RegisterPage />} />
            <Route path="/bookings/:id" element={<BookingDetails />} />
            <Route path="/bookings" element={<UserBookings/>} />

          </Routes>
          <Footer/>
        </div>
        </AuthProvider>
      </BrowserRouter>
    
  );
}

export default App;