import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import LoginUser from './components/Login-user';    // Changed name to LoginUser
import LoginDoctor from './components/Login-doctor'; // Changed name to LoginDoctor
import Welcome from './components/WelcomePage';
import UserDashboard from './components/user-dashboard'; // Import the UserDashboard component

const App = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<Welcome />}/>
                <Route path="/Login-user" element={<LoginUser />} />  {/* Use LoginUser */}
                <Route path="/Login-doctor" element={<LoginDoctor />} /> {/* Use LoginDoctor */}
                <Route path="/user-dashboard" element={<UserDashboard />} /> {/* Add this new route */}
            </Routes>
        </Router>
    );
};

export default App;
