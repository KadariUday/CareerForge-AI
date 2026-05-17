import { useState, useEffect } from 'react'
import Sidebar from './Sidebar'
import { motion, AnimatePresence } from 'framer-motion'
import { useLocation } from 'react-router-dom'
import { Menu, X, Mail, MessageSquare, Send, User, Phone } from 'lucide-react'
import api from '../api/axios'
import toast from 'react-hot-toast'

export default function Layout({ children }) {
  const location = useLocation()
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  // Contact Form State
  const [contactForm, setContactForm] = useState({ name: '', email: '', phone: '', message: '' })
  const [isSubmitting, setIsSubmitting] = useState(false)

  // Close sidebar on route change
  useEffect(() => {
    setMobileMenuOpen(false)
  }, [location])

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

  const scrollToContact = () => {
    const contactSection = document.getElementById('contact-me-section')
    if (contactSection) {
      contactSection.scrollIntoView({ behavior: 'smooth' })
    }
  }

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 overflow-x-hidden">
      {/* Mobile Sidebar Overlay */}
      <AnimatePresence>
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setMobileMenuOpen(false)}
            className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-40 lg:hidden"
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <div className={`fixed inset-y-0 left-0 z-50 transform ${mobileMenuOpen ? 'translate-x-0' : '-translate-x-full'} lg:translate-x-0 transition-transform duration-300 ease-in-out`}>
        <Sidebar onClose={() => setMobileMenuOpen(false)} />
      </div>

      {/* Main Content Area */}
      <main className="flex-1 lg:ml-64 min-h-screen relative flex flex-col w-full">
        {/* Mobile Header */}
        <header className="lg:hidden h-16 flex items-center justify-between px-6 border-b border-white/5 bg-slate-950/50 backdrop-blur-xl sticky top-0 z-30">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center">
              <span className="font-bold text-white">C</span>
            </div>
            <span className="font-bold text-white tracking-tight">CareerForge</span>
          </div>
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-2 rounded-lg bg-white/5 text-slate-400 hover:text-white transition-colors"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </header>

        {/* Decorative background blob */}
        <div className="fixed top-0 right-0 w-[500px] h-[500px] bg-indigo-600/5 blur-[120px] rounded-full pointer-events-none -z-10" />
        
        {/* Page Content */}
        <div className="flex-1 w-full max-w-7xl mx-auto px-4 sm:px-8 py-6 sm:py-10">
          <AnimatePresence mode="wait">
            <motion.div
              key={location.pathname}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.3, ease: 'easeOut' }}
              className="w-full mb-16"
            >
              {children}
            </motion.div>
          </AnimatePresence>

          {/* Statically Fixed Contact Form Section */}
          <div 
            id="contact-me-section"
            className="w-full mt-16 pt-16 border-t border-white/5 relative overflow-hidden"
          >
            {/* Soft background glow */}
            <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[350px] h-[350px] bg-indigo-500/5 blur-[100px] rounded-full pointer-events-none -z-10" />
            
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
              {/* Left Side: Info */}
              <div className="lg:col-span-5 space-y-6">
                <div>
                  <h3 className="text-3xl md:text-4xl font-bold text-white mb-4">
                    For Career Help, <br />
                    <span className="gradient-text font-display">Contact Me</span>
                  </h3>
                  <p className="text-slate-400 text-sm leading-relaxed max-w-md">
                    Have questions about your career path or need guidance on college admissions? 
                    I'm here to help you forge your future. Send me a message!
                  </p>
                </div>

                <div className="space-y-4 pt-2">
                  <div className="flex items-center gap-4 group">
                    <div className="w-11 h-11 rounded-xl bg-indigo-500/10 border border-indigo-500/20 flex items-center justify-center text-indigo-400 group-hover:scale-110 transition-transform">
                      <Mail className="w-4.5 h-4.5" />
                    </div>
                    <div>
                      <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Email Me At</p>
                      <p className="text-white text-sm font-medium">kadariuday2233@gmail.com</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 group">
                    <div className="w-11 h-11 rounded-xl bg-purple-500/10 border border-purple-500/20 flex items-center justify-center text-purple-400 group-hover:scale-110 transition-transform">
                      <MessageSquare className="w-4.5 h-4.5" />
                    </div>
                    <div>
                      <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Connect</p>
                      <a
                        href="https://www.linkedin.com/in/kadariuday"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-indigo-400 hover:text-indigo-300 text-sm font-semibold transition-colors"
                      >
                        LinkedIn Messenger
                      </a>
                    </div>
                  </div>
                </div>
              </div>

              {/* Right Side: Form Card */}
              <div className="lg:col-span-7">
                <div className="glass-card p-8 md:p-10 border-white/5 relative">
                  <form className="space-y-6" onSubmit={handleContactSubmit}>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                      <div className="space-y-2">
                        <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Your Name</label>
                        <div className="relative group">
                          <input 
                            type="text" 
                            required 
                            value={contactForm.name}
                            onChange={(e) => setContactForm({ ...contactForm, name: e.target.value })}
                            className="input-field pl-11 bg-slate-900 border-white/5 py-3.5 text-sm" 
                            placeholder="John Doe" 
                          />
                          <User className="absolute left-4 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
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
                            className="input-field pl-11 bg-slate-900 border-white/5 py-3.5 text-sm" 
                            placeholder="john@example.com" 
                          />
                          <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
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
                            className="input-field pl-11 bg-slate-900 border-white/5 py-3.5 text-sm" 
                            placeholder="+91 98765 43210" 
                          />
                          <Phone className="absolute left-4 top-1/2 -translate-y-1/2 w-4.5 h-4.5 text-slate-500 group-focus-within:text-indigo-400 transition-colors" />
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs font-bold text-slate-500 uppercase tracking-widest ml-1">Message</label>
                      <textarea 
                        required 
                        rows={4} 
                        value={contactForm.message}
                        onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                        className="input-field py-4 px-4 resize-none text-sm bg-slate-900 border-white/5" 
                        placeholder="How can I help you?"
                      ></textarea>
                    </div>

                    <button 
                      type="submit" 
                      disabled={isSubmitting}
                      className="btn-primary w-full py-4 flex items-center justify-center gap-2 group text-sm font-bold tracking-widest uppercase disabled:opacity-50 shadow-lg"
                    >
                      {isSubmitting ? (
                        <span className="flex items-center gap-2">
                          <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                          Sending...
                        </span>
                      ) : (
                        <>
                          Send Message
                          <Send className="w-4 h-4 group-hover:translate-x-0.5 transition-transform" />
                        </>
                      )}
                    </button>
                  </form>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Global Footer */}
        <footer className="py-8 px-8 border-t border-white/5 flex flex-col sm:flex-row items-center justify-between gap-4 text-slate-500 text-sm">
          <div className="flex items-center gap-2">
            <span className="w-1 h-1 rounded-full bg-indigo-500" />
            Maintained by <span className="text-slate-300 font-semibold">Kadari Uday</span>
          </div>
          <div className="flex items-center gap-4">
            <button 
              onClick={scrollToContact}
              className="flex items-center gap-2 hover:text-indigo-400 transition-colors group text-sm font-normal text-slate-500 focus:outline-none"
            >
              <MessageSquare className="w-4 h-4 group-hover:scale-110 transition-transform text-slate-500 group-hover:text-indigo-400" />
              <span>Contact Me</span>
            </button>
            <span className="opacity-20">|</span>
            <p>© 2026 CareerForge AI</p>
          </div>
        </footer>
      </main>
    </div>
  )
}
