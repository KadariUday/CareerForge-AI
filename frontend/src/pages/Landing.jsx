import { useState } from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import api from '../api/axios'
import toast from 'react-hot-toast'
import { 
  Rocket, 
  Target, 
  School, 
  FileText, 
  MessageSquare, 
  ArrowRight,
  ShieldCheck,
  Activity,
  Star,
  Send,
  Mail,
  User,
  Phone
} from 'lucide-react'

const FEATURES = [
  { 
    icon: <Target className="w-6 h-6 text-indigo-400" />, 
    title: 'AI Career Guidance', 
    desc: 'Get personalized career paths based on your interests, skills, and academic scores using GPT-4.',
    color: 'indigo'
  },
  { 
    icon: <School className="w-6 h-6 text-purple-400" />, 
    title: 'College Predictor', 
    desc: 'Predict admission chances for NEET, JEE & EAMCET with Safe / Target / Dream classification.',
    color: 'purple'
  },
  { 
    icon: <FileText className="w-6 h-6 text-pink-400" />, 
    title: 'Resume Analyzer', 
    desc: 'Upload your resume for ATS scoring, keyword analysis, and AI-powered improvement suggestions.',
    color: 'pink'
  },
  { 
    icon: <MessageSquare className="w-6 h-6 text-blue-400" />, 
    title: 'AI Chat Assistant', 
    desc: 'Ask anything — "Best careers after BDS?" or "Colleges for rank 25k?" — and get instant answers.',
    color: 'blue'
  },
]

const STATS = [
  { value: '50K+', label: 'Students Helped', icon: <Rocket className="w-4 h-4" /> },
  { value: '500+', label: 'Colleges Listed', icon: <School className="w-4 h-4" /> },
  { value: '95%', label: 'Accuracy Rate', icon: <ShieldCheck className="w-4 h-4" /> },
  { value: '24/7', label: 'AI Available', icon: <Activity className="w-4 h-4" /> },
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: {
    y: 0,
    opacity: 1
  }
}

export default function Landing() {
  const [contactForm, setContactForm] = useState({ name: '', email: '', phone: '', message: '' })
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleContactSubmit = async (e) => {
    e.preventDefault()
    setIsSubmitting(true)
    try {
      await api.post('/api/contact', contactForm)
      toast.success('Message sent! I will get back to you soon.')
      setContactForm({ name: '', email: '', phone: '', message: '' })
    } catch (err) {
      toast.error('Failed to send message. Please try again later.')
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="min-h-screen selection:bg-indigo-500/30">
      {/* Navbar */}
      <nav className="fixed top-0 inset-x-0 z-50 border-b border-white/5 backdrop-blur-xl bg-slate-950/50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-3"
          >
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-[0_0_20px_rgba(99,102,241,0.3)]">
              <Rocket className="w-6 h-6 text-white" />
            </div>
            <span className="font-display font-bold text-white text-xl tracking-tight">
              CareerForge <span className="gradient-text">AI</span>
            </span>
          </motion.div>
          
          <motion.div 
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="flex items-center gap-4"
          >
            <Link to="/login" className="btn-ghost hidden sm:inline-flex">Sign In</Link>
            <Link to="/register" className="btn-primary py-2.5">
              Get Started
              <ArrowRight className="w-4 h-4" />
            </Link>
          </motion.div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-40 pb-24 px-6 overflow-hidden">
        {/* Animated Background Elements */}
        <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full -z-10 overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-500/10 blur-[120px] rounded-full animate-pulse" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-500/10 blur-[120px] rounded-full animate-pulse" style={{ animationDelay: '1s' }} />
        </div>

        <div className="max-w-5xl mx-auto text-center relative">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-300 text-sm font-medium mb-8">
              <Star className="w-4 h-4 fill-indigo-400" />
              Trusted by 50,000+ Students Pan India
            </div>
            <h1 className="text-6xl md:text-8xl font-bold text-white leading-[1.1] mb-8 tracking-tight">
              Your Career, <br />
              <span className="gradient-text">Redefined</span> by AI
            </h1>
            <p className="text-xl text-slate-400 max-w-2xl mx-auto mb-12 leading-relaxed">
              Unlock your potential with personalized guidance, data-driven college predictions, 
              and AI-powered resume optimization. Built specifically for the Indian education landscape.
            </p>
            
            <div className="flex flex-col sm:flex-row gap-5 justify-center items-center">
              <Link to="/register" className="btn-primary text-lg px-10 py-4 w-full sm:w-auto group">
                Forge Your Future
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Link>
              <Link to="/login" className="btn-secondary text-lg px-10 py-4 w-full sm:w-auto">
                Explore Modules
              </Link>
            </div>
          </motion.div>

          {/* Stats Grid */}
          <motion.div 
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-24"
          >
            {STATS.map((s, i) => (
              <motion.div 
                key={s.label}
                variants={itemVariants}
                className="glass-card p-6 text-center group hover:border-indigo-500/30 transition-colors"
              >
                <div className="w-10 h-10 rounded-lg bg-slate-800 flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform">
                  {s.icon}
                </div>
                <div className="text-3xl font-bold text-white mb-1">{s.value}</div>
                <div className="text-sm text-slate-500 font-medium">{s.label}</div>
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-32 px-6 relative">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-20">
            <motion.h2 
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              className="text-4xl md:text-5xl font-bold text-white mb-6"
            >
              Unified Intelligence for <br />
              <span className="gradient-text">Every Student Need</span>
            </motion.h2>
            <p className="text-slate-400 text-lg max-w-2xl mx-auto">
              Four cutting-edge AI modules designed to navigate the complexities 
              of Indian college admissions and career planning.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            {FEATURES.map((f, i) => (
              <motion.div
                key={f.title}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                viewport={{ once: true }}
                className="glass-card p-8 hover:translate-y-[-8px] transition-all duration-300 group"
              >
                <div className={`w-14 h-14 rounded-2xl bg-slate-900 border border-white/5 flex items-center justify-center mb-6 group-hover:border-${f.color}-500/50 transition-colors shadow-lg`}>
                  {f.icon}
                </div>
                <h3 className="text-xl font-bold text-white mb-4">{f.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed mb-6">
                  {f.desc}
                </p>
                <Link to="/register" className="text-indigo-400 text-sm font-semibold flex items-center gap-2 hover:text-indigo-300 transition-colors group/link">
                  Learn More 
                  <ArrowRight className="w-4 h-4 group-hover/link:translate-x-1 transition-transform" />
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-6">
        <motion.div 
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          className="max-w-5xl mx-auto relative rounded-[2rem] overflow-hidden p-12 md:p-20 text-center"
        >
          {/* CTA Background */}
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/20 to-purple-600/20 -z-10" />
          <div className="absolute inset-0 backdrop-blur-3xl -z-20" />
          <div className="absolute inset-0 border border-white/10 rounded-[2rem] -z-10" />

          <h2 className="text-4xl md:text-5xl font-bold text-white mb-8">
            Stop Guessing, <br />
            <span className="gradient-text">Start Building.</span>
          </h2>
          <p className="text-xl text-slate-300 mb-12 max-w-2xl mx-auto leading-relaxed">
            Join thousands of students who have already secured their dream colleges 
            and career paths with CareerForge AI.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link to="/register" className="btn-primary text-lg px-12 py-4">
              Get Started for Free
            </Link>
            <p className="text-slate-500 text-sm">No credit card required · Free credits daily</p>
          </div>
        </motion.div>
      </section>
      {/* Contact Section */}
      <section className="py-32 px-6 relative overflow-hidden">
        <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="text-4xl md:text-5xl font-bold text-white mb-6">
              For Career Help, <br />
              <span className="gradient-text">Contact Me</span>
            </h2>
            <p className="text-slate-400 text-lg mb-8 max-w-md">
              Have questions about your career path or need guidance on college admissions? 
              I'm here to help you forge your future. Send me a message!
            </p>
            
            <div className="space-y-6">
              <div className="flex items-center gap-4 group">
                <div className="w-12 h-12 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform">
                  <Mail className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Email Me At</p>
                  <p className="text-white font-medium">kadariuday2233@gmail.com</p>
                </div>
              </div>
              <div className="flex items-center gap-4 group">
                <div className="w-12 h-12 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 group-hover:scale-110 transition-transform">
                  <MessageSquare className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-widest">Connect</p>
                  <p className="text-white font-medium">LinkedIn Messenger</p>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            className="glass-card p-8 md:p-10 border-white/5 relative"
          >
            <form className="space-y-6" onSubmit={handleContactSubmit}>
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Your Name</label>
                <div className="relative group">
                  <input 
                    type="text" 
                    required 
                    value={contactForm.name}
                    onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                    className="input-field pl-12" 
                    placeholder="John Doe" 
                  />
                  <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Email Address</label>
                <div className="relative group">
                  <input 
                    type="email" 
                    required 
                    value={contactForm.email}
                    onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                    className="input-field pl-12" 
                    placeholder="john@example.com" 
                  />
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Phone Number</label>
                <div className="relative group">
                  <input 
                    type="tel" 
                    required
                    value={contactForm.phone}
                    onChange={(e) => setContactForm({ ...contactForm, phone: e.target.value })}
                    className="input-field pl-12" 
                    placeholder="+91 98765 43210" 
                  />
                  <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Message</label>
                <textarea 
                  required 
                  rows={4} 
                  value={contactForm.message}
                  onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                  className="input-field py-4 resize-none" 
                  placeholder="How can we work together?"
                ></textarea>
              </div>

              <button 
                type="submit" 
                disabled={isSubmitting}
                className="btn-primary w-full py-4 flex items-center justify-center gap-2 group text-sm font-bold tracking-widest uppercase disabled:opacity-50"
              >
                {isSubmitting ? (
                  <span className="flex items-center gap-2">
                    <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    Sending...
                  </span>
                ) : (
                  <>
                    Send Message
                    <Send className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                  </>
                )}
              </button>
            </form>
          </motion.div>
        </div>
      </section>

      <footer className="border-t border-white/5 py-12 px-6">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-center gap-8">
          <div className="flex flex-col md:flex-row items-center gap-8">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center">
                <Rocket className="w-5 h-5 text-indigo-400" />
              </div>
              <span className="font-bold text-white">CareerForge AI</span>
            </div>
            <div className="flex items-center gap-2 text-sm text-slate-500">
               <span className="w-1 h-1 rounded-full bg-indigo-500" />
               Maintained by <span className="text-slate-300 font-semibold">Kadari Uday</span>
            </div>
          </div>

          <div className="flex items-center gap-8 text-sm">
            <a 
              href="https://www.linkedin.com/in/kadariuday" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-2 text-slate-500 hover:text-indigo-400 transition-colors group"
            >
              <svg className="w-4 h-4 fill-current group-hover:scale-110 transition-transform" viewBox="0 0 24 24">
                <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
              </svg>
              <span>LinkedIn</span>
            </a>
            <span className="text-slate-800">|</span>
            <p className="text-slate-600">
              © 2026 CareerForge AI. Built for Indian students. 🇮🇳
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

