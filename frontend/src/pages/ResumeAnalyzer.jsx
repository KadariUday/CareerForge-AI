import { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { motion, AnimatePresence } from 'framer-motion'
import { resumeAPI } from '../api/axios'
import toast from 'react-hot-toast'
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts'
import {
  FileText,
  UploadCloud,
  CheckCircle2,
  AlertCircle,
  Search,
  Briefcase,
  Award,
  RefreshCcw,
  Activity,
  Sparkles,
  Globe,
  Link,
  Mail,
  ArrowRight,
  ShieldCheck,
  ChevronRight
} from 'lucide-react'

function ScoreGauge({ score, label, colorCls }) {
  const percentage = Math.min(100, Math.max(0, score))
  const circumference = 2 * Math.PI * 30
  const offset = circumference - (percentage / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-2 group">
      <div className="relative w-16 h-16">
        <svg className="w-full h-full -rotate-90" viewBox="0 0 72 72">
          <circle cx="36" cy="36" r="30" fill="none" stroke="rgba(255,255,255,0.03)" strokeWidth="6" />
          <motion.circle
            cx="36" cy="36" r="30" fill="none"
            stroke="currentColor" strokeWidth="6"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset: offset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            strokeLinecap="round"
            className={colorCls}
          />
        </svg>
        <span className="absolute inset-0 flex items-center justify-center text-sm font-bold text-white">
          {Math.round(score)}%
        </span>
      </div>
      <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest group-hover:text-slate-300 transition-colors">
        {label}
      </span>
    </div>
  )
}

export default function ResumeAnalyzer() {
  const [file, setFile] = useState(null)
  const [jobDesc, setJobDesc] = useState('')
  const [targetRole, setTargetRole] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const onDrop = useCallback((accepted) => {
    if (accepted[0]) {
      setFile(accepted[0])
      toast.success('Resume uploaded successfully!')
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'application/pdf': ['.pdf'] }, maxFiles: 1, maxSize: 10 * 1024 * 1024,
  })

  const handleAnalyze = async () => {
    if (!file) { toast.error('Please upload a PDF resume first'); return }
    setLoading(true)
    try {
      const fd = new FormData()
      fd.append('file', file)
      if (jobDesc) fd.append('job_description', jobDesc)
      if (targetRole) fd.append('target_role', targetRole)
      const { data } = await resumeAPI.analyze(fd)
      setResult(data)
      toast.success('Resume analysis complete! 📄')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Analysis failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const radarData = result ? [
    { subject: 'Format', A: result.ats_score.formatting },
    { subject: 'Keywords', A: result.ats_score.keywords },
    { subject: 'Experience', A: result.ats_score.experience },
    { subject: 'Education', A: result.ats_score.education },
    { subject: 'Skills', A: result.ats_score.skills },
  ] : []

  return (
    <div className="space-y-10">
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
      >
        <h1 className="text-4xl font-bold text-white tracking-tight flex items-center gap-3">
          <FileText className="w-10 h-10 text-indigo-400" />
          Resume Intelligence
        </h1>
        <p className="text-slate-400 mt-2 text-lg">AI-powered ATS scoring and professional feedback loop.</p>
      </motion.div>

      {!result ? (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-8 pb-20"
        >
          <div
            {...getRootProps()}
            className={`glass-card p-16 border-2 border-dashed text-center cursor-pointer transition-all duration-500 group relative overflow-hidden ${isDragActive
                ? 'border-indigo-500 bg-indigo-500/10 scale-[0.99]'
                : 'border-white/5 hover:border-indigo-500/40 hover:bg-white/5'
              }`}
          >
            <input {...getInputProps()} />
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />

            <AnimatePresence mode="wait">
              {file ? (
                <motion.div
                  key="file"
                  initial={{ opacity: 0, scale: 0.9 }}
                  animate={{ opacity: 1, scale: 1 }}
                  className="relative z-10"
                >
                  <div className="w-20 h-20 bg-indigo-500/10 rounded-3xl flex items-center justify-center text-indigo-400 mx-auto mb-6 border border-indigo-500/20">
                    <FileText className="w-10 h-10" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-1">{file.name}</h3>
                  <p className="text-slate-500 text-sm">{(file.size / 1024).toFixed(0)} KB · Click to replace</p>
                </motion.div>
              ) : (
                <motion.div
                  key="empty"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  className="relative z-10"
                >
                  <div className="w-20 h-20 bg-slate-900 rounded-3xl flex items-center justify-center text-slate-500 mx-auto mb-6 group-hover:text-indigo-400 group-hover:bg-indigo-500/10 transition-all duration-500">
                    <UploadCloud className="w-10 h-10" />
                  </div>
                  <h3 className="text-xl font-bold text-white mb-2">
                    {isDragActive ? 'Drop your resume' : 'Upload your Resume'}
                  </h3>
                  <p className="text-slate-500 text-sm max-w-xs mx-auto">
                    Drag and drop your PDF here, or click to browse. Max file size 10MB.
                  </p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div className="glass-card p-8 space-y-6">
              <div className="flex items-center gap-3">
                <Briefcase className="w-5 h-5 text-indigo-400" />
                <h2 className="text-lg font-bold text-white uppercase tracking-widest text-sm">Target Context</h2>
              </div>
              <div className="space-y-4">
                <div>
                  <label className="text-xs font-bold text-slate-500 uppercase tracking-wider ml-1">Target Role</label>
                  <input
                    value={targetRole} onChange={e => setTargetRole(e.target.value)}
                    className="input-field mt-2" placeholder="e.g. Senior Software Engineer"
                  />
                </div>
                <p className="text-[10px] text-slate-500 uppercase tracking-widest font-bold">Role context significantly improves AI accuracy</p>
              </div>
            </div>

            <div className="glass-card p-8 space-y-6">
              <div className="flex items-center gap-3">
                <Search className="w-5 h-5 text-indigo-400" />
                <h2 className="text-lg font-bold text-white uppercase tracking-widest text-sm">Job Description</h2>
              </div>
              <textarea
                value={jobDesc} onChange={e => setJobDesc(e.target.value)} rows={3}
                className="input-field resize-none"
                placeholder="Paste the target job description here..."
              />
            </div>
          </div>

          <button
            onClick={handleAnalyze}
            disabled={loading || !file}
            className="btn-primary w-full py-5 text-lg group relative overflow-hidden"
          >
            {loading ? (
              <span className="flex items-center gap-3">
                <span className="w-6 h-6 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Processing Resume Intelligence...
              </span>
            ) : (
              <span className="flex items-center gap-2">
                Launch Analysis
                <Activity className="w-6 h-6 group-hover:scale-125 group-hover:text-amber-400 transition-all" />
              </span>
            )}
          </button>
        </motion.div>
      ) : (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="space-y-10 pb-20"
        >
          {/* Header Actions */}
          <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="w-16 h-16 rounded-2xl bg-indigo-600 flex items-center justify-center text-white shadow-xl shadow-indigo-600/20">
                <div className="text-2xl font-black">{result.ats_score.overall}</div>
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">Score Analysis</h2>
                <div className="flex items-center gap-2 mt-1">
                  <span className={`px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-widest border ${result.source === 'ai'
                      ? 'bg-indigo-500/10 text-indigo-400 border-indigo-500/20'
                      : 'bg-slate-500/10 text-slate-400 border-slate-500/20'
                    }`}>
                    {result.source === 'ai' ? 'GPT-4 Powered' : 'Standard Logic'}
                  </span>
                  <span className="text-slate-500 text-xs tracking-tight">{result.word_count} Words Analyzed</span>
                </div>
              </div>
            </div>
            <button
              onClick={() => { setResult(null); setFile(null) }}
              className="btn-secondary py-3 px-6 flex items-center gap-2 text-xs font-bold uppercase tracking-widest border-white/10 hover:bg-white/5"
            >
              <RefreshCcw className="w-4 h-4" />
              Re-upload Resume
            </button>
          </div>

          {/* Top Row: Score & Radar */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div className="lg:col-span-2 glass-card p-8">
              <div className="flex items-center justify-between mb-10">
                <h3 className="text-lg font-bold text-white uppercase tracking-widest text-sm flex items-center gap-2">
                  <ShieldCheck className="w-5 h-5 text-indigo-400" />
                  ATS Optimization Matrix
                </h3>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-4 sm:gap-8">
                <ScoreGauge score={result.ats_score.formatting} label="Format" colorCls="text-indigo-400" />
                <ScoreGauge score={result.ats_score.keywords} label="Keywords" colorCls="text-emerald-400" />
                <ScoreGauge score={result.ats_score.experience} label="Impact" colorCls="text-amber-400" />
                <ScoreGauge score={result.ats_score.education} label="Academic" colorCls="text-purple-400" />
                <ScoreGauge score={result.ats_score.skills} label="Skills" colorCls="text-rose-400" />
              </div>
            </div>

            <div className="glass-card p-8 flex flex-col items-center justify-center">
              <h3 className="text-[10px] font-bold text-slate-500 uppercase tracking-[0.2em] mb-8">Skill Distribution</h3>
              <div className="w-full h-[200px]">
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
            </div>
          </div>

          {/* Middle Row: Strengths & Skills */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div className="glass-card p-8 space-y-6">
              <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                Detected Strengths
              </h3>
              <div className="space-y-3">
                {result.strengths.map((s, i) => (
                  <div key={i} className="flex items-start gap-3 p-4 rounded-2xl bg-emerald-500/5 border border-emerald-500/10 group hover:border-emerald-500/30 transition-all">
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-2 flex-shrink-0" />
                    <p className="text-emerald-100 text-sm leading-relaxed">{s}</p>
                  </div>
                ))}
              </div>
            </div>

            <div className="glass-card p-8 space-y-6">
              <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
                <Award className="w-5 h-5 text-indigo-400" />
                Technical Competencies
              </h3>
              <div className="flex flex-wrap gap-2">
                {result.detected_skills.map((s, i) => (
                  <span key={i} className="badge badge-indigo">
                    {s}
                  </span>
                ))}
              </div>
              <div className="pt-4 border-t border-white/5 grid grid-cols-3 gap-4">
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Contact</span>
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${result.has_contact_info ? 'text-emerald-400 bg-emerald-500/10' : 'text-slate-600 bg-white/5'}`}>
                    <Mail className="w-4 h-4" />
                  </div>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">LinkedIn</span>
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${result.has_linkedin ? 'text-blue-400 bg-blue-500/10' : 'text-slate-600 bg-white/5'}`}>
                    <Link className="w-4 h-4" />
                  </div>
                </div>
                <div className="flex flex-col gap-1">
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">GitHub</span>
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${result.has_github ? 'text-white bg-white/10' : 'text-slate-600 bg-white/5'}`}>
                    <Globe className="w-4 h-4" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Suggestions */}
          <div className="glass-card p-8 space-y-8">
            <h3 className="text-sm font-bold text-white uppercase tracking-widest flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-amber-400" />
              Optimization Roadmap
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {result.suggestions.map((s, i) => (
                <div
                  key={i}
                  className={`relative p-6 rounded-3xl border-l-4 transition-all duration-300 group hover:translate-x-1 ${s.category === 'Critical' ? 'border-l-rose-500 bg-rose-500/5' :
                      s.category === 'Important' ? 'border-l-amber-500 bg-amber-500/5' :
                        'border-l-indigo-500 bg-indigo-500/5'
                    }`}
                >
                  <div className="flex items-center gap-3 mb-3">
                    <span className={`text-[10px] font-black px-2 py-0.5 rounded-md uppercase tracking-[0.2em] ${s.category === 'Critical' ? 'bg-rose-500/20 text-rose-400' :
                        s.category === 'Important' ? 'bg-amber-500/20 text-amber-400' :
                          'bg-indigo-500/20 text-indigo-400'
                      }`}>
                      {s.category}
                    </span>
                    <h4 className="text-white font-bold text-sm leading-tight group-hover:text-indigo-300 transition-colors">{s.issue}</h4>
                  </div>
                  <p className="text-slate-400 text-sm leading-relaxed mb-4">{s.suggestion}</p>
                  <div className="flex items-center gap-2 text-[10px] font-bold text-indigo-400 uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity">
                    View Reference <ArrowRight className="w-3 h-3" />
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* AI Executive Summary */}
          {result.ai_review && (
            <div className="glass-card p-10 bg-gradient-to-br from-indigo-600/10 to-transparent border-t-2 border-t-indigo-500">
              <div className="flex flex-col md:flex-row gap-10">
                <div className="space-y-6 flex-1">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-full bg-indigo-500 flex items-center justify-center text-white">
                      <Activity className="w-5 h-5" />
                    </div>
                    <h3 className="text-xl font-bold text-white">Executive Review</h3>
                  </div>
                  <p className="text-slate-300 text-lg leading-relaxed italic">"{result.ai_review}"</p>
                </div>

                {result.improved_summary && (
                  <div className="w-full md:w-[350px]">
                    <div className="p-6 rounded-3xl bg-slate-950 border border-white/5 relative overflow-hidden group">
                      <div className="absolute top-0 right-0 p-3 opacity-10 group-hover:opacity-20 transition-opacity">
                        <Sparkles className="w-20 h-20" />
                      </div>
                      <h4 className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest mb-3">AI Content Strategy</h4>
                      <p className="text-slate-400 text-xs font-bold uppercase tracking-widest mb-2">Refined Summary Suggestion:</p>
                      <p className="text-slate-200 text-sm leading-relaxed italic font-medium relative z-10">
                        "{result.improved_summary}"
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </motion.div>
      )}
    </div>
  )
}

