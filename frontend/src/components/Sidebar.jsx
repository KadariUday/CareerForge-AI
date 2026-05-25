import { NavLink, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import toast from 'react-hot-toast'
import { 
  LayoutDashboard, 
  Target, 
  School, 
  FileText, 
  MessageSquare, 
  LogOut,
  Rocket
} from 'lucide-react'

const NAV_ITEMS = [
  { to: '/dashboard', icon: <LayoutDashboard className="w-5 h-5" />, label: 'Dashboard' },
  { to: '/career', icon: <Target className="w-5 h-5" />, label: 'Career Guidance' },
  { to: '/college', icon: <School className="w-5 h-5" />, label: 'College Predictor' },
  { to: '/resume', icon: <FileText className="w-5 h-5" />, label: 'Resume Analyzer' },
  { to: '/chat', icon: <MessageSquare className="w-5 h-5" />, label: 'AI Assistant' },
]

export default function Sidebar({ onClose }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    toast.success('Logged out successfully')
    navigate('/')
    if (onClose) onClose()
  }

  return (
    <motion.aside 
      initial={{ x: -300, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 100, damping: 20 }}
      className="h-full w-64 flex flex-col border-r border-white/5 bg-slate-950 lg:bg-slate-950/50 backdrop-blur-xl shadow-2xl"
    >
      {/* Logo */}
      <div className="p-8">
        <div className="flex items-center gap-3">
          <motion.div 
            whileHover={{ scale: 1.1, rotate: 10 }}
            className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-[0_0_20px_rgba(99,102,241,0.2)]"
          >
            <Rocket className="w-6 h-6 text-white" />
          </motion.div>
          <div>
            <div className="font-bold text-white text-lg tracking-tight leading-none">CareerForge</div>
            <div className="text-[10px] text-indigo-400 font-bold uppercase tracking-widest mt-1">AI Engine</div>
          </div>
        </div>
      </div>

      {/* User Profile */}
      <div className="px-6 pb-8 border-b border-white/5">
        <div className="p-4 rounded-2xl bg-white/5 border border-white/5 flex items-center gap-3 hover:bg-white/10 transition-colors cursor-pointer">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-sm font-bold text-white shadow-lg shadow-indigo-500/20">
            {user?.name?.[0]?.toUpperCase() || 'U'}
          </div>
          <div className="min-w-0">
            <div className="text-sm font-bold text-white truncate">{user?.name || 'User'}</div>
            <div className="text-[10px] text-slate-500 font-medium truncate">{user?.email}</div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 py-8 space-y-2 overflow-y-auto no-scrollbar">
        <p className="px-4 text-[10px] font-bold text-slate-600 uppercase tracking-[0.2em] mb-4">Core Modules</p>
        {NAV_ITEMS.map((item, i) => (
          <motion.div key={item.to} initial={{ opacity: 0, x: -20 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.1 }}>
            <NavLink
              to={item.to}
              className={({ isActive }) => `nav-link ${isActive ? 'active' : ''}`}
            >
              {item.icon}
              <span className="font-semibold">{item.label}</span>
            </NavLink>
          </motion.div>
        ))}
      </nav>

      {/* Logout */}
      <div className="p-4 border-t border-white/5">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-all duration-300 group"
        >
          <LogOut className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          <span>Sign Out</span>
        </button>
      </div>
    </motion.aside>
  )
}
