import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import {
  CheckCircle, XCircle, Upload, Search, ShieldCheck,
  AlertCircle, Loader2, Activity, ChevronRight, Building2,
  ArrowLeft
} from 'lucide-react';
import { Button } from './components/Button';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const API_BASE = ''; // Relative to the same domain on Vercel

interface VerificationDetail {
  status: 'match' | 'mismatch';
  expected?: string;
  actual?: string;
}

interface VerificationResult {
  primary_key: string;
  found: boolean;
  is_valid: boolean;
  error?: string;
  details?: Record<string, VerificationDetail>;
}

const COMPANIES = [
  { id: 'max_life', name: 'Max Life Insurance', icon: 'M', color: 'bg-blue-600', active: true },
  { id: 'tata', name: 'Tata Life Insurance', icon: 'T', color: 'bg-teal-600', active: true },
  { id: 'hdfc', name: 'HDFC Life', icon: 'H', color: 'bg-red-600', active: true },
  { id: 'icici', name: 'ICICI Prudential', icon: 'I', color: 'bg-orange-600', active: true },
  { id: 'bajaj', name: 'Bajaj Allianz', icon: 'B', color: 'bg-yellow-600', active: true },
];

function App() {
  const [selectedCompany, setSelectedCompany] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<VerificationResult[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setResults(null);
    }
  };

  const startVerification = async () => {
    if (!file || !selectedCompany) return;
    setLoading(true);
    setError(null);
    setResults(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      formData.append('company', selectedCompany);
      const resp = await axios.post(`${API_BASE}/api/verify-golden`, formData);
      setResults(resp.data.results);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Verification failed. Please check your CSV format.');
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setResults(null);
    setError(null);
    setSelectedCompany(null);
  };

  // Browser back button support
  React.useEffect(() => {
    const handlePopState = () => {
      if (selectedCompany) {
        setSelectedCompany(null);
      }
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, [selectedCompany]);

  const handleSelectCompany = (id: string) => {
    window.history.pushState({ company: id }, '');
    setSelectedCompany(id);
  };

  // --- Landing Page View ---
  if (!selectedCompany) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 font-['Inter']">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="max-w-4xl w-full"
        >
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs font-semibold tracking-wide uppercase mb-6">
            <ShieldCheck className="w-4 h-4" />
            <span>Term Renewals</span>
          </div>
          <h1 className="text-5xl font-semibold text-slate-900 mb-4 tracking-tight">Select Company</h1>
          <p className="text-slate-500 text-lg font-medium">Choose an insurance provider to begin the Golden Record verification</p>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {COMPANIES.map((company) => (
              <motion.button
                key={company.id}
                whileHover={company.active ? { y: -5, scale: 1.02 } : {}}
                whileTap={company.active ? { scale: 0.98 } : {}}
                onClick={() => company.active && handleSelectCompany(company.id)}
                className={cn(
                  "relative p-8 rounded-[32px] border-2 transition-all text-left overflow-hidden",
                  company.active
                    ? "bg-white border-white shadow-[0_20px_40px_rgba(0,0,0,0.04)] hover:shadow-xl hover:border-blue-100"
                    : "bg-slate-100 border-slate-200 opacity-60 cursor-not-allowed"
                )}
              >
                {!company.active && (
                  <div className="absolute top-4 right-4 bg-slate-200 text-slate-500 px-2 py-0.5 rounded text-[10px] font-bold uppercase">
                    Soon
                  </div>
                )}
                <div className={cn("w-14 h-14 rounded-2xl flex items-center justify-center text-white text-2xl font-semibold mb-6 shadow-lg", company.color)}>
                  {company.icon}
                </div>
                <h3 className="text-xl font-semibold text-slate-900 mb-2">{company.name}</h3>
                <p className="text-slate-400 text-sm leading-relaxed font-medium">
                  {company.active ? "" : "Integration pending implementation."}
                </p>
                {company.active && (
                  <div className="mt-6 flex items-center text-blue-600 font-semibold text-sm">
                    Enter Portal <ChevronRight className="w-4 h-4 ml-1" />
                  </div>
                )}
              </motion.button>
            ))}
          </div>

          <div className="mt-16 pt-8 border-t border-slate-200 flex items-center justify-between text-slate-400">
            <div className="flex items-center space-x-2">
              <Activity className="w-5 h-5" />
              <span className="text-sm font-medium">System status: All systems operational</span>
            </div>
            <p className="text-xs font-bold uppercase tracking-widest">© 2026 Golden Audit v2.0</p>
          </div>
        </motion.div>
      </div>
    );
  }

  // --- Main Verification Portal ---
  return (
    <div className="min-h-screen bg-slate-50 text-[#1E293B] font-['Inter'] flex items-center justify-center p-6 md:p-12 overflow-x-hidden">
      <div className="max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">

        {/* Left Column: Branding */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col space-y-8 lg:sticky lg:top-24"
        >
          <button
            onClick={reset}
            className="inline-flex items-center space-x-2 text-slate-400 hover:text-blue-600 font-bold transition-colors group mb-4"
          >
            <ArrowLeft className="w-4 h-4 group-hover:-translate-x-1 transition-transform" />
            <span>Select Another Company</span>
          </button>

          <div className="inline-flex items-center space-x-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs font-bold tracking-wide uppercase self-start">
            <Building2 className="w-4 h-4" />
            <span>{COMPANIES.find(c => c.id === selectedCompany)?.name} Portal</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-black tracking-tight text-slate-900 leading-[1.1]">
            Record <br />
            <span className="text-blue-600">Verification.</span>
          </h1>

          <p className="text-slate-500 text-xl leading-relaxed max-w-lg">
            Ensure your policy data strictly adheres to the authoritative golden entries.
          </p>

          <div className="flex flex-col space-y-4 pt-4">
            <div className="flex items-center space-x-3 text-slate-700">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-semibold text-sm">1</div>
              <span className="font-semibold text-lg">Upload your company CSV</span>
            </div>
            <div className="flex items-center space-x-3 text-slate-700">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-semibold text-sm">2</div>
              <span className="font-semibold text-lg">Verify against Golden Set</span>
            </div>
            <div className="flex items-center space-x-3 text-slate-700">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-semibold text-sm">3</div>
              <span className="font-semibold text-lg">Correct and proceed</span>
            </div>
          </div>
        </motion.div>

        {/* Right Column: Portal */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          className="w-full"
        >
          <div className="bg-white rounded-[40px] shadow-[0_32px_64px_-16px_rgba(0,0,0,0.12)] border border-slate-200 p-8 md:p-12 relative overflow-hidden">
            <div className="absolute top-0 right-0 p-8 opacity-5">
              <Activity className="w-32 h-32 text-blue-600" />
            </div>

            <div className="relative z-10">
              <h2 className="text-3xl font-semibold mb-2">Internal Verification Check</h2>
              <p className="text-slate-400 mb-10 font-medium">Checking integrity for {COMPANIES.find(c => c.id === selectedCompany)?.name}</p>

              {!results && (
                <div className="space-y-8">
                  <div className="relative border-4 border-dashed border-slate-100 rounded-[32px] p-16 flex flex-col items-center justify-center hover:border-blue-400 hover:bg-blue-50/50 transition-all cursor-pointer group bg-slate-50/50">
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleFileChange}
                      className="absolute inset-0 opacity-0 cursor-pointer z-20"
                    />
                    <div className="w-20 h-20 bg-white rounded-3xl shadow-xl flex items-center justify-center text-blue-600 mb-6 group-hover:scale-110 transition-transform pointer-events-none relative z-10">
                      <Upload className="w-10 h-10" />
                    </div>
                    <p className="text-xl font-semibold text-slate-900 pointer-events-none relative z-10 text-center">
                      {file ? file.name : `Drop ${COMPANIES.find(c => c.id === selectedCompany)?.name} CSV`}
                    </p>
                    <p className="text-sm text-slate-400 mt-2 font-medium pointer-events-none relative z-10">Maximum file size: 10MB</p>
                  </div>

                  <Button
                    onClick={startVerification}
                    fullWidth
                    disabled={!file || loading}
                    className="py-6 text-lg font-semibold bg-blue-600 hover:bg-blue-700 shadow-xl shadow-blue-200 rounded-2xl"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-6 h-6 animate-spin mr-3" />
                        Analyzing Records...
                      </>
                    ) : (
                      "Check"
                    )}
                  </Button>
                </div>
              )}

              {results && (
                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
                  <div className={cn(
                    "flex items-center justify-between p-6 rounded-3xl shadow-lg transition-all duration-500",
                    results.every(r => r.found && r.is_valid) ? "bg-green-600 text-white" : "bg-red-600 text-white"
                  )}>
                    <div>
                      <p className={cn(
                        "text-xs font-semibold uppercase tracking-widest mb-1",
                        results.every(r => r.found && r.is_valid) ? "text-green-100" : "text-red-100"
                      )}>Status Report</p>
                      <h3 className="text-xl font-semibold">
                        {results.every(r => r.found && r.is_valid) ? "Approved: All Records Match" : "Fatal Warning: Data Mismatch"}
                      </h3>
                    </div>
                    <Button onClick={() => setResults(null)} variant="ghost" className="text-white hover:bg-white/10 border-white/20">Clean Slate</Button>
                  </div>

                  <div className="space-y-4 max-h-[600px] overflow-y-auto pr-2">
                    {results.map((r, idx) => (
                      <div key={idx} className="group border border-slate-100 rounded-3xl p-6 hover:shadow-md transition-shadow bg-slate-50/50">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center space-x-4">
                            <div className={cn(
                              "w-12 h-12 rounded-2xl flex items-center justify-center shadow-sm",
                              !r.found ? "bg-amber-100 text-amber-600" : (r.is_valid ? "bg-green-100 text-green-600" : "bg-red-100 text-red-600")
                            )}>
                              {!r.found ? <Search className="w-6 h-6" /> : (r.is_valid ? <CheckCircle className="w-6 h-6" /> : <XCircle className="w-6 h-6" />)}
                            </div>
                            <div>
                              <h4 className="font-semibold text-slate-900">{r.primary_key}</h4>
                              <p className="text-xs text-slate-500 font-medium">
                                {r.is_valid ? "Correct data - Proceed" : (r.found ? "Data Incorrect" : "Record missing from CSV")}
                              </p>
                            </div>
                          </div>
                        </div>

                        {!r.is_valid && r.found && (
                          <div className="mt-4 p-3 bg-red-50 border border-red-100 rounded-xl flex items-center space-x-2 text-red-700">
                            <AlertCircle className="w-4 h-4 shrink-0" />
                            <span className="text-xs font-semibold">Critical data discrepancy found. Please review the highlighted fields below.</span>
                          </div>
                        )}

                        {!r.is_valid && r.details && (
                          <div className="mt-6 pt-6 border-t border-slate-200 grid grid-cols-1 md:grid-cols-2 gap-4">
                            {Object.entries(r.details).map(([key, val]) => (
                              val.status === 'mismatch' && (
                                <div key={key} className="flex flex-col space-y-2 p-3 bg-white rounded-xl border border-red-100 shadow-sm font-medium">
                                  <span className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">{key}</span>
                                  <div className="flex items-center justify-between">
                                    <div className="flex flex-col">
                                      <span className="text-[10px] text-gray-400 font-semibold">Golden Record</span>
                                      <span className="text-xs font-medium text-slate-900">{val.expected || "(Empty)"}</span>
                                    </div>
                                    <div className="flex flex-col items-end">
                                      <span className="text-[10px] text-red-500 font-semibold">Uploaded CSV</span>
                                      <span className="text-xs font-semibold text-red-600">{val.actual || "(Empty)"}</span>
                                    </div>
                                  </div>
                                </div>
                              )
                            ))}
                          </div>
                        )}
                        {r.error && (
                          <p className="mt-4 text-xs font-semibold text-amber-600 flex items-center">
                            <AlertCircle className="w-4 h-4 mr-1" /> {r.error}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )
              }

              {error && (
                <div className="mt-8 p-5 bg-red-50 text-red-700 rounded-[24px] text-sm flex items-start space-x-3 border border-red-100 border-l-4">
                  <AlertCircle className="w-6 h-6 shrink-0" />
                  <span className="font-medium leading-relaxed">{error}</span>
                </div>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default App;
