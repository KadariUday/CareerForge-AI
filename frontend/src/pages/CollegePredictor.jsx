import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { collegeAPI } from '../api/axios'
import toast from 'react-hot-toast'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  ReferenceLine,
  Cell
} from 'recharts'
import {
  School,
  Search,
  MapPin,
  CreditCard,
  Award,
  GraduationCap,
  ChevronRight,
  TrendingUp,
  Filter,
  CheckCircle2,
  AlertCircle,
  Activity,
  ArrowRight
} from 'lucide-react'

const EXAMS = ['NEET', 'JEE_MAINS', 'JEE_ADVANCED', 'EAMCET', 'EAMCET_BIPC', 'KCET', 'MHT_CET', 'COMEDK']
const CATEGORIES = ['General', 'OBC', 'SC', 'ST', 'EWS', 'PWD']
const STATES = [
  'Andhra Pradesh', 'Bihar', 'Delhi', 'Gujarat', 'Karnataka',
  'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Puducherry', 'Punjab',
  'Rajasthan', 'Tamil Nadu', 'Telangana', 'Uttar Pradesh', 'Uttarakhand',
  'All India'
]

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
}

const itemVariants = {
  hidden: { y: 20, opacity: 0 },
  visible: { y: 0, opacity: 1 }
}

export default function CollegePredictor() {
  const [form, setForm] = useState({ exam: 'NEET', rank: '', category: 'General', state: '', max_fees_lpa: '', preferred_branch: 'All' })
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState('safe')

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.rank || !form.state) {
      toast.error('Please enter your rank and home state')
      return
    }
    setLoading(true)
    try {
      const payload = {
        exam: form.exam, rank: parseInt(form.rank),
        category: form.category, state: form.state,
        max_fees_lpa: form.max_fees_lpa ? parseFloat(form.max_fees_lpa) : undefined,
        preferred_branch: form.preferred_branch
      }
      const { data } = await collegeAPI.predict(payload)
      setResult(data)
      setActiveTab(data.safe.length > 0 ? 'safe' : data.target.length > 0 ? 'target' : 'dream')
      toast.success(`Found ${data.total_found} matching colleges!`)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Prediction failed')
    } finally {
      setLoading(false)
    }
  }

  const colleges = result ? (activeTab === 'safe' ? result.safe : activeTab === 'target' ? result.target : result.dream) : []

  const chartData = result ? [
    ...result.safe.slice(0, 2).map(c => ({ name: c.college.name.split(' ')[0], cutoff: c.avg_cutoff, type: 'Safe', full: c.college.name })),
    ...result.target.slice(0, 2).map(c => ({ name: c.college.name.split(' ')[0], cutoff: c.avg_cutoff, type: 'Target', full: c.college.name })),
    ...result.dream.slice(0, 2).map(c => ({ name: c.college.name.split(' ')[0], cutoff: c.avg_cutoff, type: 'Dream', full: c.college.name })),
  ] : []

  const getClassificationColor = (type) => {
    switch (type) {
      case 'Safe': return '#10b981'
      case 'Target': return '#f59e0b'
      case 'Dream': return '#f43f5e'
      default: return '#6366f1'
    }
  }

  return (
    <div className="space-y-10">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
      >
        <h1 className="text-4xl font-bold text-white tracking-tight flex items-center gap-3">
          <School className="w-10 h-10 text-indigo-400" />
          College Predictor
        </h1>
        <p className="text-slate-400 mt-2 text-lg">Data-driven admission probability analysis for top Indian exams.</p>
      </motion.div>

      {/* Form Section */}
      <motion.form
        onSubmit={handleSubmit}
        className="glass-card p-8 border-indigo-500/10"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <div className="flex items-center gap-2 mb-8">
          <Filter className="w-5 h-5 text-indigo-400" />
          <h2 className="text-lg font-bold text-white uppercase tracking-widest text-sm">Prediction Filters</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Competitive Exam</label>
            <div className="relative group">
              <select
                value={form.exam}
                onChange={e => setForm({ ...form, exam: e.target.value })}
                className="input-field appearance-none pr-10"
              >
                {EXAMS.map(e => <option key={e} value={e}>{e.replace('_', ' ')}</option>)}
              </select>
              <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 rotate-90 pointer-events-none group-hover:text-indigo-400 transition-colors" />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Preferred Discipline</label>
            <div className="relative group">
              <select
                value={form.preferred_branch}
                onChange={e => setForm({ ...form, preferred_branch: e.target.value })}
                className="input-field appearance-none pr-10"
              >
                {form.exam === 'EAMCET_BIPC' ? (
                  <>
                    <option value="All">Core BIPC (Agri/Pharm/Vet)</option>
                    <option value="Agriculture">Agriculture</option>
                    <option value="Pharmacy">Pharmacy / Pharm.D</option>
                    <option value="Veterinary">Veterinary</option>
                    <option value="Horticulture">Horticulture</option>
                  </>
                ) : (
                  <>
                    <option value="All">All Disciplines</option>
                    <option value="Agriculture">Agriculture</option>
                    <option value="Pharmacy">Pharmacy / Pharm.D</option>
                    <option value="Medical">Medical / Paramedical</option>
                    <option value="Computer">Computer Science / IT</option>
                    <option value="Mechanical">Mechanical Engineering</option>
                    <option value="Civil">Civil Engineering</option>
                    <option value="Electronics">Electronics / ECE / EEE</option>
                  </>
                )}
              </select>
              <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 rotate-90 pointer-events-none group-hover:text-indigo-400 transition-colors" />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Your All India Rank</label>
            <div className="relative">
              <input
                type="number" min="1" required
                value={form.rank}
                onChange={e => setForm({ ...form, rank: e.target.value })}
                className="input-field pl-10"
                placeholder="e.g. 25000"
              />
              <TrendingUp className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Category Quota</label>
            <div className="relative group">
              <select
                value={form.category}
                onChange={e => setForm({ ...form, category: e.target.value })}
                className="input-field appearance-none pr-10"
              >
                {CATEGORIES.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
              <ChevronRight className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 rotate-90 pointer-events-none group-hover:text-indigo-400 transition-colors" />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Home State</label>
            <div className="relative group">
              <select
                value={form.state}
                onChange={e => setForm({ ...form, state: e.target.value })}
                className="input-field appearance-none pr-10"
                required
              >
                <option value="">Select Home State</option>
                {STATES.map(s => <option key={s} value={s}>{s}</option>)}
              </select>
              <MapPin className="absolute right-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500 pointer-events-none group-hover:text-indigo-400 transition-colors" />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Max Annual Fees (LPA) (Optional)</label>
            <div className="relative">
              <input
                type="number" min="0" step="0.1"
                value={form.max_fees_lpa}
                onChange={e => setForm({ ...form, max_fees_lpa: e.target.value })}
                className="input-field pl-10"
                placeholder="e.g. 5.0"
              />
              <CreditCard className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-500" />
            </div>
          </div>

          <div className="flex items-end">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary w-full py-3.5 group flex items-center justify-center gap-2"
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <span className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Analyzing Data...
                </span>
              ) : (
                <>
                  <Search className="w-5 h-5 group-hover:scale-110 transition-transform" />
                  Run Prediction
                </>
              )}
            </button>
          </div>
        </div>
      </motion.form>

      {/* Results Section */}
      <AnimatePresence>
        {result && (
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            className="space-y-10 pb-20"
          >
            {/* Summary Cards */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
              {[
                { label: 'Safe Bets', count: result.safe.length, icon: <CheckCircle2 className="w-5 h-5" />, color: 'emerald' },
                { label: 'Target Match', count: result.target.length, icon: <Activity className="w-5 h-5" />, color: 'amber' },
                { label: 'Dream Colleges', count: result.dream.length, icon: <AlertCircle className="w-5 h-5" />, color: 'rose' },
              ].map(s => (
                <div key={s.label} className="glass-card p-6 flex items-center justify-between group">
                  <div>
                    <div className={`text-4xl font-bold text-${s.color}-400 mb-1`}>{s.count}</div>
                    <div className="flex items-center gap-2 text-slate-500 font-bold uppercase tracking-widest text-[10px]">
                      {s.icon}
                      {s.label}
                    </div>
                  </div>
                  <div className={`w-12 h-12 rounded-xl bg-${s.color}-500/10 flex items-center justify-center text-${s.color}-400 border border-${s.color}-500/20 group-hover:scale-110 transition-transform`}>
                    <School className="w-6 h-6" />
                  </div>
                </div>
              ))}
            </div>

            {/* Visualization and Tabs Container */}
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Left Side: Visualization */}
              <div className="lg:col-span-1 space-y-6">
                <div className="glass-card p-6 h-full min-h-[300px] flex flex-col">
                  <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                    <TrendingUp className="w-5 h-5 text-indigo-400" />
                    Rank Analysis
                  </h3>

                  <div className="flex-1 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={chartData} layout="vertical" margin={{ left: -20, right: 20 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={false} />
                        <XAxis type="number" hide />
                        <YAxis dataKey="name" type="category" tick={{ fill: '#94a3b8', fontSize: 10, fontWeight: 600 }} width={80} />
                        <Tooltip
                          cursor={{ fill: 'rgba(255,255,255,0.02)' }}
                          contentStyle={{ background: '#0f172a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                          labelStyle={{ color: '#fff', fontWeight: 'bold', marginBottom: '4px' }}
                        />
                        <ReferenceLine x={parseInt(form.rank)} stroke="#6366f1" strokeDasharray="5 5" label={{ position: 'top', value: 'My Rank', fill: '#818cf8', fontSize: 10, fontWeight: 'bold' }} />
                        <Bar dataKey="cutoff" radius={[0, 4, 4, 0]} barSize={20}>
                          {chartData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={getClassificationColor(entry.type)} fillOpacity={0.6} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>

                  <p className="text-[10px] text-slate-500 text-center mt-4 uppercase tracking-[0.2em] font-bold">
                    Relative cutoff proximity map
                  </p>
                </div>
              </div>

              {/* Right Side: Tabbed Results */}
              <div className="lg:col-span-2 space-y-6">
                <div className="flex p-1 rounded-2xl bg-slate-900/50 border border-white/5 backdrop-blur-sm self-start">
                  {['safe', 'target', 'dream'].map(tab => (
                    <button
                      key={tab}
                      onClick={() => setActiveTab(tab)}
                      className={`flex items-center gap-2 px-6 py-3 rounded-xl text-xs font-bold uppercase tracking-widest transition-all duration-300 ${activeTab === tab
                          ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/20'
                          : 'text-slate-500 hover:text-slate-300'
                        }`}
                    >
                      <div className={`w-2 h-2 rounded-full ${tab === 'safe' ? 'bg-emerald-500' : tab === 'target' ? 'bg-amber-500' : 'bg-rose-500'
                        }`} />
                      {tab}
                      <span className="ml-1 opacity-50">({result[tab].length})</span>
                    </button>
                  ))}
                </div>

                <motion.div
                  layout
                  className="grid grid-cols-1 gap-4"
                >
                  {colleges.length === 0 ? (
                    <div className="glass-card p-12 text-center">
                      <School className="w-12 h-12 text-slate-700 mx-auto mb-4" />
                      <h4 className="text-slate-400 font-bold">No results found</h4>
                      <p className="text-slate-600 text-sm">Try broadening your search or adjusting your max fees.</p>
                    </div>
                  ) : colleges.map((pred, i) => (
                    <motion.div
                      key={pred.college.college_id + i}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: i * 0.05 }}
                      className="glass-card group hover:border-white/20 transition-all duration-300"
                    >
                      <div className="p-6">
                        <div className="flex flex-col md:flex-row justify-between gap-6">
                          <div className="space-y-4">
                            <div className="flex items-center gap-3">
                              <div className={`px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border ${activeTab === 'safe' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                                  activeTab === 'target' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                                    'bg-rose-500/10 text-rose-400 border-rose-500/20'
                                }`}>
                                {pred.admission_chance_percent}% Probability
                              </div>
                              <div className="flex items-center gap-1 text-slate-500 text-[10px] font-bold uppercase tracking-widest">
                                <Award className="w-3 h-3" />
                                {pred.college.college_type}
                              </div>
                            </div>

                            <div>
                              <h3 className="text-xl font-bold text-white group-hover:text-indigo-400 transition-colors leading-tight">
                                {pred.college.name}
                              </h3>
                              <div className="flex items-center gap-4 mt-2">
                                <span className="flex items-center gap-1 text-xs text-slate-400">
                                  <MapPin className="w-3 h-3" />
                                  {pred.college.location}, {pred.college.state}
                                </span>
                                <span className="flex items-center gap-1 text-xs text-slate-400">
                                  <GraduationCap className="w-3 h-3" />
                                  {pred.college.branch}
                                </span>
                              </div>
                            </div>
                          </div>

                          <div className="flex flex-col md:items-end justify-between gap-4">
                            <div className="text-left md:text-right">
                              <div className="text-slate-500 text-[10px] font-bold uppercase tracking-[0.2em] mb-1">3-Year Avg. Cutoff</div>
                              <div className="text-2xl font-bold text-white">#{pred.avg_cutoff.toLocaleString()}</div>
                              <div className={`text-[10px] font-bold mt-1 ${pred.rank_gap <= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                                {pred.rank_gap <= 0 ? `+${Math.abs(pred.rank_gap).toLocaleString()} above avg` : `-${Math.abs(pred.rank_gap).toLocaleString()} below avg`}
                              </div>
                            </div>

                            <div className="flex items-center gap-4">
                              <div className="text-right">
                                <div className="text-slate-500 text-[10px] font-bold uppercase tracking-widest">Fees / Year</div>
                                <div className="text-sm font-bold text-white">₹{pred.college.fees_lpa} LPA</div>
                              </div>
                              {pred.college.nirf_rank && (
                                <div className="text-right pl-4 border-l border-white/10">
                                  <div className="text-slate-500 text-[10px] font-bold uppercase tracking-widest">NIRF Rank</div>
                                  <div className="text-sm font-bold text-white">#{pred.college.nirf_rank}</div>
                                </div>
                              )}
                            </div>
                          </div>
                        </div>

                        {/* Interactive Footer */}
                        <div className="mt-6 pt-6 border-t border-white/5 flex items-center justify-between">
                          <div className="flex-1 max-w-[200px]">
                            <div className="h-1.5 w-full bg-white/5 rounded-full overflow-hidden">
                              <motion.div
                                initial={{ width: 0 }}
                                animate={{ width: `${pred.admission_chance_percent}%` }}
                                className={`h-full rounded-full bg-gradient-to-r ${activeTab === 'safe' ? 'from-emerald-500 to-emerald-400' :
                                    activeTab === 'target' ? 'from-amber-500 to-amber-400' :
                                      'from-rose-500 to-rose-400'
                                  }`}
                              />
                            </div>
                          </div>
                          <button className="flex items-center gap-2 text-[10px] font-bold text-indigo-400 uppercase tracking-widest hover:text-indigo-300 transition-colors group/btn">
                            View Prospectus
                            <ArrowRight className="w-3 h-3 group-hover/btn:translate-x-1 transition-transform" />
                          </button>
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </motion.div>
              </div>
            </div>

            {/* Disclaimer */}
            <motion.div
              variants={itemVariants}
              className="glass-card p-6 border-amber-500/10 bg-amber-500/5 flex items-start gap-4"
            >
              <AlertCircle className="w-6 h-6 text-amber-400 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-bold text-amber-400 uppercase tracking-wider">Prediction Disclaimer</h4>
                <p className="text-slate-400 text-xs mt-1 leading-relaxed">
                  Please note that this is purely an AI and data-driven analysis. It is just a prediction and students may still have chances in these colleges depending on dynamic counseling rounds, seat availability, and choice filling preferences.
                </p>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  )
}

