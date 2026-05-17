import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { careerAPI } from '../api/axios'
import toast from 'react-hot-toast'
import { 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  Radar, 
  ResponsiveContainer, 
  Tooltip,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Cell
} from 'recharts'
import { 
  Target, 
  Plus, 
  X, 
  Brain, 
  Briefcase, 
  GraduationCap, 
  Lightbulb, 
  TrendingUp, 
  Building2, 
  ArrowRight,
  Sparkles,
  BookOpen,
  Layout,
  Users,
  Compass,
  Activity
} from 'lucide-react'

const PERSONALITY_TRAITS = ['analytical', 'creative', 'leadership', 'social', 'technical', 'entrepreneurial']
const INTEREST_SUGGESTIONS = ['coding', 'biology', 'design', 'finance', 'teaching', 'research', 'entrepreneurship', 'data science', 'marketing', 'law']

export default function CareerGuidance() {
  const [form, setForm] = useState({
    interests: [], skills: '', academic_scores: { math: '', physics: '', biology: '' },
    personality_traits: [], current_education: '', preferred_work_style: '',
  })
  const [customInterest, setCustomInterest] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const toggleInterest = (i) => setForm(f => ({
    ...f, interests: f.interests.includes(i) ? f.interests.filter(x => x !== i) : [...f.interests, i]
  }))
  const toggleTrait = (t) => setForm(f => ({
    ...f, personality_traits: f.personality_traits.includes(t) ? f.personality_traits.filter(x => x !== t) : [...f.personality_traits, t]
  }))
  const addCustomInterest = () => {
    if (customInterest.trim() && !form.interests.includes(customInterest.trim())) {
      setForm(f => ({ ...f, interests: [...f.interests, customInterest.trim()] }))
      setCustomInterest('')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.interests.length === 0) { toast.error('Please add at least one interest'); return }
    setLoading(true)
    try {
      const payload = {
        interests: form.interests,
        skills: form.skills.split(',').map(s => s.trim()).filter(Boolean),
        academic_scores: Object.fromEntries(
          Object.entries(form.academic_scores).filter(([,v]) => v !== '').map(([k,v]) => [k, parseFloat(v)])
        ),
        personality_traits: form.personality_traits,
        current_education: form.current_education || undefined,
        preferred_work_style: form.preferred_work_style || undefined,
      }
      const { data } = await careerAPI.analyze(payload)
      setResult(data)
      toast.success('Career analysis complete! 🚀')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-10">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
      >
        <h1 className="text-4xl font-bold text-white tracking-tight flex items-center gap-3">
          <Target className="w-10 h-10 text-indigo-400" />
          AI Career Guidance
        </h1>
        <p className="text-slate-400 mt-2 text-lg">Harness GPT-4 to map your academic strengths to industry demand.</p>
      </motion.div>

      {!result ? (
        <motion.form 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          onSubmit={handleSubmit} 
          className="space-y-8 pb-20"
        >
          {/* Interests & Skills */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="glass-card p-8 space-y-6">
              <div className="flex items-center gap-3 mb-2">
                <Compass className="w-5 h-5 text-indigo-400" />
                <h2 className="text-lg font-bold text-white uppercase tracking-widest text-sm">Passions & Interests</h2>
              </div>
              
              <div className="flex flex-wrap gap-2">
                {INTEREST_SUGGESTIONS.map(i => (
                  <button 
                    key={i} type="button" onClick={() => toggleInterest(i)}
                    className={`px-4 py-2 rounded-xl text-xs font-bold border transition-all duration-300 ${
                      form.interests.includes(i) 
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow-lg shadow-indigo-600/20' 
                      : 'border-white/5 text-slate-500 hover:text-slate-300 hover:bg-white/5'
                    }`}
                  >
                    {i.toUpperCase()}
                  </button>
                ))}
              </div>

              <div className="flex gap-3">
                <div className="relative flex-1">
                  <input 
                    value={customInterest} 
                    onChange={e => setCustomInterest(e.target.value)}
                    onKeyDown={e => e.key === 'Enter' && (e.preventDefault(), addCustomInterest())}
                    className="input-field pl-10" 
                    placeholder="Other interests..." 
                  />
                  <Plus className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
                </div>
                <button 
                  type="button" 
                  onClick={addCustomInterest} 
                  className="btn-secondary px-6 font-bold"
                >
                  Add
                </button>
              </div>

              <AnimatePresence>
                {form.interests.length > 0 && (
                  <motion.div 
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    className="flex flex-wrap gap-2 pt-4 border-t border-white/5"
                  >
                    {form.interests.map(i => (
                      <span 
                        key={i} 
                        className="badge badge-indigo flex items-center gap-2 pr-2 py-1.5 cursor-pointer group" 
                        onClick={() => toggleInterest(i)}
                      >
                        {i}
                        <X className="w-3 h-3 group-hover:text-white transition-colors" />
                      </span>
                    ))}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>

            <div className="glass-card p-8 space-y-6">
              <div className="flex items-center gap-3 mb-2">
                <Briefcase className="w-5 h-5 text-indigo-400" />
                <h2 className="text-lg font-bold text-white uppercase tracking-widest text-sm">Experience & Profile</h2>
              </div>
              
              <div className="space-y-4">
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Key Skills</label>
                  <input 
                    value={form.skills} 
                    onChange={e => setForm({...form, skills: e.target.value})}
                    className="input-field mt-2" 
                    placeholder="e.g. Python, Public Speaking, UI Design..." 
                  />
                </div>
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Current Education</label>
                  <input 
                    value={form.current_education} 
                    onChange={e => setForm({...form, current_education: e.target.value})}
                    className="input-field mt-2" 
                    placeholder="e.g. 12th Standard / B.Tech CSE" 
                  />
                </div>
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Preferred Environment</label>
                  <div className="grid grid-cols-3 gap-3 mt-2">
                    {['Remote', 'On-site', 'Hybrid'].map(style => (
                      <button
                        key={style}
                        type="button"
                        onClick={() => setForm({...form, preferred_work_style: style})}
                        className={`py-2.5 rounded-xl text-xs font-bold border transition-all duration-300 ${
                          form.preferred_work_style === style 
                          ? 'bg-white/10 text-white border-white/20' 
                          : 'border-white/5 text-slate-500 hover:text-slate-300'
                        }`}
                      >
                        {style}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Academic & Personality */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="glass-card p-8 space-y-6">
              <div className="flex items-center gap-3 mb-2">
                <GraduationCap className="w-5 h-5 text-indigo-400" />
                <h2 className="text-lg font-bold text-white uppercase tracking-widest text-sm">Academic Performance (Optional)</h2>
              </div>
              
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                {['math', 'physics', 'biology'].map(sub => (
                  <div key={sub} className="space-y-2">
                    <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">{sub}</label>
                    <input 
                      type="number" min="0" max="100"
                      value={form.academic_scores[sub]}
                      onChange={e => setForm({...form, academic_scores: {...form.academic_scores, [sub]: e.target.value}})}
                      className="input-field text-center" 
                      placeholder="%" 
                    />
                  </div>
                ))}
              </div>
              <p className="text-[10px] text-slate-500 uppercase tracking-widest text-center">Scores help AI assess technical suitability</p>
            </div>

            <div className="glass-card p-8 space-y-6">
              <div className="flex items-center gap-3 mb-2">
                <Brain className="w-5 h-5 text-indigo-400" />
                <h2 className="text-lg font-bold text-white uppercase tracking-widest text-sm">Personality Matrix</h2>
              </div>
              
              <div className="flex flex-wrap gap-2">
                {PERSONALITY_TRAITS.map(t => (
                  <button 
                    key={t} type="button" onClick={() => toggleTrait(t)}
                    className={`px-4 py-2 rounded-xl text-xs font-bold border uppercase tracking-widest transition-all duration-300 ${
                      form.personality_traits.includes(t) 
                      ? 'bg-purple-600 text-white border-purple-500 shadow-lg shadow-purple-600/20' 
                      : 'border-white/5 text-slate-500 hover:text-slate-300 hover:bg-white/5'
                    }`}
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button 
            type="submit" 
            disabled={loading} 
            className="btn-primary w-full py-5 text-lg group relative overflow-hidden"
          >
            {loading ? (
              <span className="flex items-center gap-3">
                <span className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                AI Analysis in progress...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                Analyze My Career Path
                <ArrowRight className="w-6 h-6 group-hover:translate-x-1 transition-transform" />
              </span>
            )}
          </button>
        </motion.form>
      ) : (
        <CareerResults 
          result={result} 
          form={form} 
          onReset={() => setResult(null)} 
        />
      )}
    </div>
  )
}

function CareerResults({ result, form, onReset }) {
  const [selected, setSelected] = useState(0)
  const path = result.career_paths[selected]

  const radarData = [
    { subject: 'Match', A: path.match_percentage },
    { subject: 'Demand', A: path.demand_level === 'Very High' ? 95 : path.demand_level === 'High' ? 75 : 55 },
    { subject: 'Growth', A: path.growth_rate === 'High' ? 85 : path.growth_rate === 'Medium' ? 65 : 45 },
    { subject: 'Salary', A: 80 },
    { subject: 'Skills', A: 70 },
  ]

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="space-y-8 pb-20"
    >
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-2xl font-bold text-white">Recommended Trajectories</h2>
          <p className="text-slate-400 mt-1">Top {result.career_paths.length} paths identified for your profile.</p>
        </div>
        <button 
          onClick={onReset} 
          className="btn-secondary py-2.5 text-xs font-bold uppercase tracking-widest border-white/10 hover:bg-white/5"
        >
          New Analysis
        </button>
      </div>

      {/* Summary Widget */}
      <div className="glass-card p-8 bg-gradient-to-r from-indigo-600/10 to-transparent border-l-4 border-l-indigo-500">
        <div className="flex items-start gap-6">
          <div className="w-12 h-12 rounded-2xl bg-indigo-500/20 flex items-center justify-center text-indigo-400 flex-shrink-0">
            <Lightbulb className="w-6 h-6" />
          </div>
          <div className="space-y-4">
            <p className="text-slate-200 text-lg leading-relaxed font-medium">{result.summary}</p>
            <div className="flex items-center gap-2 text-indigo-400 font-bold text-sm bg-indigo-500/10 w-fit px-4 py-2 rounded-xl">
              <Sparkles className="w-4 h-4" />
              Next Step: {result.immediate_action}
            </div>
          </div>
        </div>
      </div>

      {/* Career Selection Tabs */}
      <div className="flex gap-3 overflow-x-auto pb-2 no-scrollbar">
        {result.career_paths.map((p, i) => (
          <button 
            key={i} 
            onClick={() => setSelected(i)}
            className={`flex-shrink-0 px-6 py-4 rounded-2xl border transition-all duration-300 text-left min-w-[200px] ${
              i === selected 
              ? 'bg-indigo-600 border-indigo-500 shadow-xl shadow-indigo-600/20' 
              : 'glass-card hover:border-white/20'
            }`}
          >
            <div className={`text-xs font-bold uppercase tracking-widest mb-2 ${i === selected ? 'text-white/70' : 'text-slate-500'}`}>
              Match {p.match_percentage}%
            </div>
            <div className={`font-bold ${i === selected ? 'text-white' : 'text-slate-300'}`}>{p.title}</div>
          </button>
        ))}
      </div>

      {/* Detail View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 space-y-8">
          <div className="glass-card p-8">
            <div className="flex flex-col md:flex-row justify-between gap-6 mb-8">
              <div>
                <h3 className="text-3xl font-bold text-white mb-3">{path.title}</h3>
                <p className="text-slate-400 leading-relaxed text-lg">{path.description}</p>
              </div>
              <div className="text-center bg-white/5 rounded-3xl p-6 border border-white/5 min-w-[140px]">
                <div className="text-4xl font-black gradient-text">{path.match_percentage}%</div>
                <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-1">Compatibility</div>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              {[
                { label: 'Avg Salary', value: `₹${path.average_salary_lpa} LPA`, icon: <TrendingUp className="w-4 h-4 text-emerald-400" /> },
                { label: 'Job Demand', value: path.demand_level, icon: <Users className="w-4 h-4 text-blue-400" /> },
                { label: 'Timeline', value: `${path.timeline_months} Months`, icon: <Activity className="w-4 h-4 text-amber-400" /> },
              ].map(s => (
                <div key={s.label} className="p-4 rounded-2xl bg-white/5 border border-white/5 group hover:border-white/20 transition-all">
                  <div className="flex items-center gap-2 text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">
                    {s.icon}
                    {s.label}
                  </div>
                  <div className="text-lg font-bold text-white">{s.value}</div>
                </div>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="glass-card p-8 space-y-6">
              <h4 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                <Brain className="w-4 h-4 text-indigo-400" />
                Skills to Master
              </h4>
              <div className="flex flex-wrap gap-2">
                {path.skills_to_learn.map(s => (
                  <span key={s} className="badge badge-indigo">{s}</span>
                ))}
              </div>
            </div>

            <div className="glass-card p-8 space-y-6">
              <h4 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                <Building2 className="w-4 h-4 text-purple-400" />
                Top Hiring Partners
              </h4>
              <div className="flex flex-wrap gap-3">
                {path.top_companies.map(c => (
                  <span key={c} className="px-4 py-2 rounded-xl bg-white/5 border border-white/5 text-xs font-bold text-slate-300">
                    {c}
                  </span>
                ))}
              </div>
            </div>
          </div>

          <div className="glass-card p-8 space-y-6">
            <h4 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
              <BookOpen className="w-4 h-4 text-amber-400" />
              Learning Roadmap
            </h4>
            <div className="space-y-4">
              {path.recommended_courses.map((c, i) => (
                <div key={i} className="flex items-center gap-4 p-4 rounded-2xl bg-slate-900 border border-white/5 group hover:border-indigo-500/30 transition-all">
                  <div className="w-10 h-10 rounded-xl bg-white/5 flex items-center justify-center text-indigo-400 group-hover:bg-indigo-600 group-hover:text-white transition-all">
                    {i + 1}
                  </div>
                  <div className="flex-1 font-semibold text-slate-200">{c}</div>
                  <ArrowRight className="w-5 h-5 text-slate-600 group-hover:text-indigo-400" />
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="space-y-8">
          <div className="glass-card p-8 h-fit flex flex-col items-center">
            <h4 className="text-sm font-bold text-white uppercase tracking-widest mb-8">Role Suitability</h4>
            <div className="w-full h-[250px]">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="rgba(255,255,255,0.05)" />
                  <PolarAngleAxis dataKey="subject" tick={{ fill: '#64748b', fontSize: 10, fontWeight: 700 }} />
                  <Radar dataKey="A" stroke="#6366f1" fill="#6366f1" fillOpacity={0.4} />
                  <Tooltip 
                    contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
            <div className="mt-8 pt-8 border-t border-white/5 w-full text-center">
               <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2">Estimated Growth</div>
               <div className="text-2xl font-bold text-emerald-400">{path.growth_rate}</div>
            </div>
          </div>

          <div className="glass-card p-8 bg-gradient-to-b from-indigo-500/20 to-transparent">
             <h4 className="text-sm font-bold text-white uppercase tracking-widest mb-4">AI Prediction</h4>
             <p className="text-slate-300 text-sm leading-relaxed italic">
               "Based on your strong {form.academic_scores.math > 80 ? 'mathematical base' : 'profile'} 
               and interest in {form.interests[0]}, {path.title} offers the highest ROI on your skill set."
             </p>
          </div>
        </div>
      </div>
    </motion.div>
  )
}

