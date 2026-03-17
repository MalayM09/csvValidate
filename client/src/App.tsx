import React, { useState } from 'react';
import axios from 'axios';
import { motion } from 'framer-motion';
import { CheckCircle, XCircle, Upload, Search, ShieldCheck, AlertCircle, Loader2, FileText, Activity } from 'lucide-react';
import { Button } from './components/Button';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const API_BASE = 'http://localhost:8000';

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

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<VerificationResult[] | null>(null);
  const [summary, setSummary] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setResults(null);
    }
  };

  const startVerification = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResults(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const resp = await axios.post(`${API_BASE}/api/verify-golden`, formData);
      setResults(resp.data.results);
      setSummary(resp.data.summary);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Verification failed. Please check your CSV format.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 text-[#1E293B] font-['Inter'] flex items-center justify-center p-6 md:p-12 overflow-x-hidden">
      <div className="max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">

        {/* Left Column: Branding */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex flex-col space-y-8 lg:sticky lg:top-24"
        >
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 bg-blue-100 text-blue-700 rounded-full text-xs font-bold tracking-wide uppercase self-start">
            <ShieldCheck className="w-4 h-4" />
            <span>Golden Data Integrity</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-black tracking-tight text-slate-900 leading-[1.1]">
            Golden Record <br />
            <span className="text-blue-600">Verification.</span>
          </h1>

          <p className="text-slate-500 text-xl leading-relaxed max-w-lg">
            Ensure your policy data strictly adheres to the authoritative golden entries. Upload your CSV to perform a deep cross-check against the backend reference set.
          </p>

          <div className="flex flex-col space-y-4 pt-4">
            <div className="flex items-center space-x-3 text-slate-700">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm">1</div>
              <span className="font-medium text-lg">Upload your latest policy CSV</span>
            </div>
            <div className="flex items-center space-x-3 text-slate-700">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm">2</div>
              <span className="font-medium text-lg">Verify against 6 Golden Records</span>
            </div>
            <div className="flex items-center space-x-3 text-slate-700">
              <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-bold text-sm">3</div>
              <span className="font-medium text-lg">Instant mismatch reporting</span>
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
              <h2 className="text-3xl font-bold mb-2">Verification Portal</h2>
              <p className="text-slate-400 mb-10">Securely check your data integrity</p>

              {!results && (
                <div className="space-y-8">
                  <div className="relative border-4 border-dashed border-slate-100 rounded-[32px] p-16 flex flex-col items-center justify-center hover:border-blue-400 hover:bg-blue-50/50 transition-all cursor-pointer group bg-slate-50/50">
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleFileChange}
                      className="absolute inset-0 opacity-0 cursor-pointer"
                    />
                    <div className="w-20 h-20 bg-white rounded-3xl shadow-xl flex items-center justify-center text-blue-600 mb-6 group-hover:scale-110 transition-transform">
                      <Upload className="w-10 h-10" />
                    </div>
                    <p className="text-xl font-bold text-slate-900">
                      {file ? file.name : "Drop your CSV file"}
                    </p>
                    <p className="text-sm text-slate-400 mt-2">Maximum file size: 10MB</p>
                  </div>

                  <Button
                    onClick={startVerification}
                    fullWidth
                    disabled={!file || loading}
                    className="py-6 text-lg font-black bg-blue-600 hover:bg-blue-700 shadow-xl shadow-blue-200 rounded-2xl"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-6 h-6 animate-spin mr-3" />
                        Analyzing Records...
                      </>
                    ) : (
                      "Run Verification Check"
                    )}
                  </Button>
                </div>
              )}

              {results && (
                <div className="space-y-8 animate-in fade-in slide-in-from-bottom-4">
                  <div className="flex items-center justify-between bg-slate-900 text-white p-6 rounded-3xl shadow-lg">
                    <div>
                      <p className="text-slate-400 text-xs font-bold uppercase tracking-widest mb-1">Status Report</p>
                      <h3 className="text-xl font-bold">{summary}</h3>
                    </div>
                    <Button onClick={() => setResults(null)} variant="ghost" className="text-white hover:bg-white/10">New Check</Button>
                  </div>

                  <div className="space-y-4">
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
                              <h4 className="font-bold text-slate-900">{r.primary_key}</h4>
                              <p className="text-xs text-slate-500">
                                {r.is_valid ? "Correct data - Proceed" : (r.found ? "Incorrect data detected" : "Record missing from CSV")}
                              </p>
                            </div>
                          </div>
                        </div>

                        {!r.is_valid && r.details && (
                          <div className="mt-6 pt-6 border-t border-slate-200 grid grid-cols-1 gap-4">
                            {Object.entries(r.details).map(([key, val]) => (
                              val.status === 'mismatch' && (
                                <div key={key} className="flex flex-col space-y-2 p-3 bg-white rounded-xl border border-red-50">
                                  <span className="text-[10px] font-black uppercase tracking-wider text-slate-400">{key}</span>
                                  <div className="flex items-center justify-between">
                                    <div className="flex flex-col">
                                      <span className="text-[10px] text-red-400 font-bold">Expected</span>
                                      <span className="text-xs font-medium text-slate-900">{val.expected || "(Empty)"}</span>
                                    </div>
                                    <div className="flex flex-col items-end">
                                      <span className="text-[10px] text-blue-400 font-bold">Actual</span>
                                      <span className="text-xs font-black text-red-600">{val.actual || "(Empty)"}</span>
                                    </div>
                                  </div>
                                </div>
                              )
                            ))}
                          </div>
                        )}
                        {r.error && (
                          <p className="mt-4 text-xs font-bold text-amber-600 flex items-center">
                            <AlertCircle className="w-4 h-4 mr-1" /> {r.error}
                          </p>
                        )}
                      </div>
                    ))}
                  </div>
                </div>
              )}

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
