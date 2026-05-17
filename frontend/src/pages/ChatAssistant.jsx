import { useState, useRef, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { chatAPI } from '../api/axios'
import toast from 'react-hot-toast'
import { 
  MessageSquare, 
  Send, 
  Trash2, 
  Sparkles, 
  User, 
  HelpCircle,
  Plus,
  Activity,
  Command
} from 'lucide-react'

const QUICK_PROMPTS = [
  'Best career after BDS?',
  'Colleges for NEET rank 25000?',
  'How to improve my resume?',
  'Career options after 12th PCM?',
  'What skills for Data Science?',
]

export default function ChatAssistant() {
  const [messages, setMessages] = useState([
    { 
      role: 'assistant', 
      content: "Welcome to CareerForge Intelligence 🎯. I'm your dedicated AI counselor.\n\nI can help you navigate college admissions, optimize your resume, and discover career paths that align with your personality. How can I assist you today?" 
    }
  ])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [suggestions, setSuggestions] = useState(QUICK_PROMPTS)
  const bottomRef = useRef(null)

  useEffect(() => { 
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' }) 
  }, [messages])

  const sendMessage = async (text) => {
    const msg = text || input.trim()
    if (!msg) return
    setInput('')
    setMessages(prev => [...prev, { role: 'user', content: msg }])
    setLoading(true)
    try {
      const { data } = await chatAPI.sendMessage({ message: msg, session_id: sessionId })
      setSessionId(data.session_id)
      setMessages(prev => [...prev, { role: 'assistant', content: data.reply }])
      if (data.suggestions?.length) setSuggestions(data.suggestions)
    } catch (err) {
      toast.error('Failed to connect to AI engine. Please retry.')
      setMessages(prev => [...prev, { role: 'assistant', content: 'Apologies, I encountered a connection issue. Please check your network and try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => { 
    if (e.key === 'Enter' && !e.shiftKey) { 
      e.preventDefault()
      sendMessage() 
    } 
  }

  const clearChat = async () => {
    if (sessionId) { try { await chatAPI.clearSession(sessionId) } catch {} }
    setMessages([{ 
      role: 'assistant', 
      content: "Chat cleared. I'm ready for new inquiries. What would you like to explore?" 
    }])
    setSessionId(null)
    setSuggestions(QUICK_PROMPTS)
  }

  return (
    <div className="flex flex-col h-[calc(100vh-6rem)] max-w-5xl mx-auto">
      {/* Header */}
      <motion.div 
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="flex items-center justify-between mb-8"
      >
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400">
            <MessageSquare className="w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white tracking-tight">AI Counselor</h1>
            <div className="flex items-center gap-2 mt-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-slate-500 text-[10px] font-bold uppercase tracking-widest">Neural Link Active</span>
            </div>
          </div>
        </div>
        <button 
          onClick={clearChat} 
          className="p-3 rounded-xl bg-white/5 border border-white/5 text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-all group"
          title="Clear Conversation"
        >
          <Trash2 className="w-5 h-5 group-hover:scale-110 transition-transform" />
        </button>
      </motion.div>

      {/* Messages Window */}
      <div className="flex-1 glass-card p-6 overflow-y-auto space-y-8 no-scrollbar mb-6 scroll-smooth border-white/5">
        <AnimatePresence mode="popLayout">
          {messages.map((msg, i) => (
            <motion.div 
              key={i} 
              initial={{ opacity: 0, y: 10, scale: 0.98 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex max-w-[85%] gap-4 ${msg.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                <div className={`w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0 mt-1 shadow-lg ${
                  msg.role === 'user' 
                  ? 'bg-slate-800 text-slate-400 border border-white/10' 
                  : 'bg-indigo-600 text-white border border-indigo-500/50'
                }`}>
                  {msg.role === 'user' ? <User className="w-5 h-5" /> : <Sparkles className="w-5 h-5" />}
                </div>
                
                <div className={`p-5 rounded-3xl text-sm leading-relaxed whitespace-pre-wrap ${
                  msg.role === 'user' 
                  ? 'bg-indigo-600 text-white rounded-tr-none shadow-xl shadow-indigo-600/10' 
                  : 'glass-card text-slate-200 rounded-tl-none border-indigo-500/10'
                }`}>
                  {msg.content}
                </div>
              </div>
            </motion.div>
          ))}
          
          {loading && (
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="flex justify-start"
            >
              <div className="flex max-w-[85%] gap-4">
                <div className="w-10 h-10 rounded-2xl bg-indigo-600/20 text-indigo-400 flex items-center justify-center flex-shrink-0 animate-pulse border border-indigo-500/20">
                  <Activity className="w-5 h-5" />
                </div>
                <div className="glass-card flex items-center gap-2 px-6 py-4 rounded-3xl rounded-tl-none">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '200ms' }} />
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400 animate-bounce" style={{ animationDelay: '400ms' }} />
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
        <div ref={bottomRef} />
      </div>

      {/* Input Area */}
      <div className="space-y-4">
        {/* Quick Actions */}
        <div className="flex gap-2 overflow-x-auto no-scrollbar pb-1">
          <div className="flex items-center gap-2 text-slate-600 text-[10px] font-bold uppercase tracking-widest px-2 mr-2">
            <Command className="w-3 h-3" />
            Quick Actions
          </div>
          {suggestions.map((s, i) => (
            <button 
              key={i} 
              onClick={() => sendMessage(s)} 
              disabled={loading}
              className="whitespace-nowrap px-4 py-2 rounded-xl text-xs font-bold border border-white/5 text-slate-400 hover:text-indigo-400 hover:bg-indigo-500/10 hover:border-indigo-500/20 transition-all disabled:opacity-50"
            >
              {s}
            </button>
          ))}
        </div>

        <div className="relative group">
          <textarea 
            value={input} 
            onChange={e => setInput(e.target.value)} 
            onKeyDown={handleKey}
            disabled={loading} 
            rows={1}
            className="input-field w-full pl-6 pr-16 py-5 rounded-3xl resize-none transition-all duration-300 focus:ring-2 focus:ring-indigo-500/50"
            placeholder="Describe your career goals or ask for specific advice..."
            style={{ minHeight: '64px', maxHeight: '160px' }}
          />
          <div className="absolute right-3 bottom-3 flex items-center gap-2">
            <button 
              onClick={() => sendMessage()} 
              disabled={loading || !input.trim()} 
              className={`w-10 h-10 rounded-2xl flex items-center justify-center transition-all duration-300 ${
                input.trim() 
                ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/40 hover:scale-105 active:scale-95' 
                : 'bg-white/5 text-slate-600'
              }`}
            >
              {loading ? (
                <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <Send className="w-5 h-5" />
              )}
            </button>
          </div>
        </div>
        <p className="text-[10px] text-slate-600 text-center uppercase tracking-widest font-bold flex items-center justify-center gap-2">
          <HelpCircle className="w-3 h-3" />
          Press Enter to send message · Shift + Enter for new line
        </p>
      </div>
    </div>
  )
}

