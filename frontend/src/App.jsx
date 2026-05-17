import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './context/AuthContext'
import Layout from './components/Layout'
import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import CareerGuidance from './pages/CareerGuidance'
import CollegePredictor from './pages/CollegePredictor'
import ResumeAnalyzer from './pages/ResumeAnalyzer'
import ChatAssistant from './pages/ChatAssistant'

// Route guard for authenticated pages
const PrivateRoute = ({ children }) => {
  const { user, loading } = useAuth()
  if (loading) return (
    <div className="flex items-center justify-center min-h-screen">
      <div className="w-10 h-10 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
    </div>
  )
  return user ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <Routes>
      {/* Public pages */}
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected pages — wrapped in sidebar layout */}
      <Route path="/dashboard" element={<PrivateRoute><Layout><Dashboard /></Layout></PrivateRoute>} />
      <Route path="/career" element={<PrivateRoute><Layout><CareerGuidance /></Layout></PrivateRoute>} />
      <Route path="/college" element={<PrivateRoute><Layout><CollegePredictor /></Layout></PrivateRoute>} />
      <Route path="/resume" element={<PrivateRoute><Layout><ResumeAnalyzer /></Layout></PrivateRoute>} />
      <Route path="/chat" element={<PrivateRoute><Layout><ChatAssistant /></Layout></PrivateRoute>} />

      {/* 404 */}
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
