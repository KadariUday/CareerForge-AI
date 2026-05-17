import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import { 
  Target, 
  School, 
  FileText, 
  MessageSquare, 
  ArrowRight,
  Sparkles,
  Activity,
  TrendingUp,
  BrainCircuit
} from 'lucide-react'

const MODULES = [
  { 
    to: '/career', 
    icon: <Target className="w-6 h-6" />, 
    title: 'Career Guidance', 
    desc: 'Discover your ideal career path with AI', 
    color: 'from-indigo-500 to-purple-600',
    shadow: 'shadow-indigo-500/20'
  },
  { 
    to: '/college', 
    icon: <School className="w-6 h-6" />, 
    title: 'College Predictor', 
    desc: 'NEET / JEE / EAMCET rank analysis', 
    color: 'from-blue-500 to-cyan-600',
    shadow: 'shadow-blue-500/20'
  },
  { 
    to: '/resume', 
    icon: <FileText className="w-6 h-6" />, 
    title: 'Resume Analyzer', 
    desc: 'ATS scoring & AI improvement tips', 
    color: 'from-violet-500 to-pink-600',
    shadow: 'shadow-violet-500/20'
  },
  { 
    to: '/chat', 
    icon: <MessageSquare className="w-6 h-6" />, 
    title: 'AI Assistant', 
    desc: 'Expert answers to your career queries', 
    color: 'from-emerald-500 to-teal-600',
    shadow: 'shadow-emerald-500/20'
  },
]

const QUICK_ACTIONS = [
  { label: 'Upload Resume', icon: <FileText className="w-4 h-4" />, to: '/resume' },
  { label: 'Predict College', icon: <School className="w-4 h-4" />, to: '/college' },
  { label: 'Ask AI Assistant', icon: <MessageSquare className="w-4 h-4" />, to: '/chat' },
]

export default function Dashboard() {
  const { user } = useAuth()
  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Good morning' : hour < 17 ? 'Good afternoon' : 'Good evening'

  return (
    <div className="space-y-10">
      {/* Welcome Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex-1"
        >
          <h1 className="text-3xl sm:text-4xl font-bold text-white tracking-tight">
            {greeting}, <span className="gradient-text">{user?.name?.split(' ')[0] || 'Explorer'}</span> 👋
          </h1>
          <p className="text-slate-400 mt-2 text-base sm:text-lg">Your personalized career command center is ready.</p>
        </motion.div>
        
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex flex-wrap gap-2 sm:gap-3"
        >
          {QUICK_ACTIONS.map((action) => (
            <Link 
              key={action.label} 
              to={action.to}
              className="btn-secondary py-2 px-3 sm:px-4 text-[10px] sm:text-xs flex items-center gap-2 border-white/5 bg-white/5 hover:bg-white/10 flex-1 sm:flex-none justify-center whitespace-nowrap"
            >
              {action.icon}
              {action.label}
            </Link>
          ))}
        </motion.div>
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Left Column: Modules */}
        <div className="lg:col-span-2 space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-white flex items-center gap-2">
              <BrainCircuit className="w-5 h-5 text-indigo-400" />
              Core Modules
            </h2>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-widest">Select to Start</span>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {MODULES.map((m, i) => (
              <motion.div
                key={m.to}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <Link to={m.to} className="glass-card p-6 group block hover:border-white/20 transition-all duration-300">
                  <div className="flex items-center gap-5">
                    <div className={`w-14 h-14 rounded-2xl bg-gradient-to-br ${m.color} flex items-center justify-center text-white shadow-xl ${m.shadow} group-hover:scale-110 transition-transform duration-300`}>
                      {m.icon}
                    </div>
                    <div className="flex-1 min-w-0">
                      <h3 className="font-bold text-white text-lg group-hover:text-indigo-400 transition-colors">{m.title}</h3>
                      <p className="text-slate-400 text-sm mt-1 line-clamp-1">{m.desc}</p>
                    </div>
                    <div className="w-10 h-10 rounded-full bg-white/5 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                      <ArrowRight className="w-5 h-5 text-white" />
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>

          {/* AI Insights / Tips Widget */}
          <div className="glass-card p-8 bg-gradient-to-br from-indigo-600/10 to-purple-600/10 border-indigo-500/20">
            <div className="flex items-start justify-between mb-6">
              <div>
                <h3 className="text-xl font-bold text-white mb-2 flex items-center gap-2">
                  <Sparkles className="w-5 h-5 text-amber-400" />
                  AI Daily Insights
                </h3>
                <p className="text-slate-400 text-sm">Personalized tips based on your profile</p>
              </div>
              <div className="px-3 py-1 rounded-full bg-indigo-500/20 border border-indigo-500/30 text-[10px] font-bold text-indigo-400 uppercase tracking-wider">
                Updated Just Now
              </div>
            </div>
            
            <div className="space-y-4">
              {[
                { tip: "Your resume score is in the top 15% for Software Engineering roles.", icon: <TrendingUp className="w-4 h-4 text-emerald-400" /> },
                { tip: "Based on current trends, Data Science roles in Bangalore are seeing 40% growth.", icon: <Activity className="w-4 h-4 text-amber-400" /> },
                { tip: "Complete your skill profile to get more accurate college predictions.", icon: <BrainCircuit className="w-4 h-4 text-purple-400" /> }
              ].map((item, i) => (
                <div key={i} className="flex items-center gap-4 p-4 rounded-xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                  <div className="flex-shrink-0 w-8 h-8 rounded-lg bg-slate-900 flex items-center justify-center">
                    {item.icon}
                  </div>
                  <p className="text-slate-300 text-sm leading-relaxed">{item.tip}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Column: Profile & Stats */}
        <div className="space-y-8">
          <div className="glass-card p-8 text-center relative overflow-hidden">
             {/* Subtle background glow */}
            <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-32 bg-indigo-500/20 blur-3xl -z-10" />
            
            <div className="w-24 h-24 rounded-3xl bg-gradient-to-br from-indigo-500 to-purple-600 mx-auto mb-6 flex items-center justify-center text-3xl font-bold text-white shadow-2xl shadow-indigo-500/40">
              {user?.name?.[0]?.toUpperCase() || 'U'}
            </div>
            <h3 className="text-2xl font-bold text-white mb-1">{user?.name || 'User'}</h3>
            <p className="text-slate-500 text-sm mb-6">{user?.email}</p>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                <div className="text-xl font-bold text-white">12</div>
                <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mt-1">AI Analyses</div>
              </div>
              <div className="p-4 rounded-2xl bg-white/5 border border-white/5">
                <div className="text-xl font-bold text-white">85%</div>
                <div className="text-[10px] text-slate-500 font-bold uppercase tracking-widest mt-1">Profile Strength</div>
              </div>
            </div>
            
            <button className="btn-primary w-full mt-8 py-3 text-sm">
              Complete Profile
            </button>
          </div>

          <div className="glass-card p-6">
            <h4 className="text-sm font-bold text-white mb-4 uppercase tracking-widest">Platform Activity</h4>
            <div className="space-y-6">
              {[
                { label: 'Resume Scanned', time: '2 hours ago', color: 'bg-emerald-500' },
                { label: 'College Predicted', time: 'Yesterday', color: 'bg-blue-500' },
                { label: 'Career Analyzed', time: '3 days ago', color: 'bg-purple-500' },
              ].map((act, i) => (
                <div key={i} className="flex items-center gap-4">
                  <div className={`w-2 h-2 rounded-full ${act.color} shadow-[0_0_8px_rgba(0,0,0,0.5)]`} />
                  <div className="flex-1">
                    <div className="text-sm font-semibold text-slate-200">{act.label}</div>
                    <div className="text-xs text-slate-500">{act.time}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

