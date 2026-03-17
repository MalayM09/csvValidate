import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, XCircle, Upload, Search, Sheet, Mail, User, AlertCircle, Loader2, Table, RefreshCw } from 'lucide-react';
import { Button } from './components/Button';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const API_BASE = 'http://localhost:8000';

interface ValidationBatchResult {
  csv_row: Record<string, any>;
  sheet_row: Record<string, any> | null;
  matches: Record<string, boolean>;
  is_valid: boolean;
  name_present: boolean;
  email_present: boolean;
  error?: string;
}

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [samples, setSamples] = useState<Record<string, any>[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [validating, setValidating] = useState(false);
  const [results, setResults] = useState<ValidationBatchResult[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setError(null);
      setSamples(null);
      setResults(null);
    }
  };

  const uploadCSV = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const resp = await axios.post(`${API_BASE}/api/upload-csv`, formData);
      setSamples(resp.data.samples);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to process CSV');
    } finally {
      setLoading(false);
    }
  };

  const validateBatch = async () => {
    if (!samples) return;
    setValidating(true);
    setError(null);
    try {
      const resp = await axios.post(`${API_BASE}/api/validate-batch`, samples);
      setResults(resp.data.results);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Validation failed');
    } finally {
      setValidating(false);
    }
  };

  const reset = () => {
    setFile(null);
    setSamples(null);
    setResults(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-white text-[#212529] font-['Inter'] flex items-center justify-center p-6 md:p-12 lg:p-20 overflow-x-hidden">
      <div className="max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">

        {/* Left Column: Content */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex flex-col space-y-8 sticky top-20"
        >
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-orange-50 text-orange-600 rounded-full text-xs font-bold tracking-wide uppercase">
            <RefreshCw className="w-3 h-3" />
            <span>Batch Cross-Check</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-[#212529] leading-[1.05]">
            Compare CSV with <br />
            <span className="text-blue-600">Google Sheets.</span>
          </h1>

          <p className="text-[#868E96] text-xl leading-relaxed max-w-lg">
            Upload your CSV and we'll randomly sample 5-6 entries to cross-check against the Master Sheet in real-time.
          </p>

          <div className="p-6 bg-gray-50 rounded-3xl border border-gray-100 flex items-center space-x-4">
            <div className="w-12 h-12 bg-blue-100 rounded-2xl flex items-center justify-center text-blue-600">
              <Sheet className="w-6 h-6" />
            </div>
            <div>
              <p className="text-xs font-bold text-gray-400 uppercase tracking-wider">Target Sheet</p>
              <p className="text-sm font-bold text-gray-700">1bMd0xDug...RZnHI</p>
            </div>
          </div>
        </motion.div>

        {/* Right Column: Workflow */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          className="relative w-full"
        >
          <div className="bg-white rounded-[32px] shadow-[0_20px_50px_rgba(0,0,0,0.06)] border border-gray-100 p-8 md:p-10 w-full relative z-10">

            {/* Step 1: Upload */}
            {!samples && (
              <div className="space-y-8">
                <h2 className="text-2xl font-bold">Step 1: Upload CSV</h2>
                <div className="relative border-2 border-dashed border-gray-200 rounded-[24px] p-12 flex flex-col items-center justify-center hover:border-blue-400 transition-colors bg-gray-50/50">
                  <input
                    type="file"
                    accept=".csv"
                    onChange={handleFileChange}
                    className="absolute inset-0 opacity-0 cursor-pointer"
                  />
                  <Upload className="w-12 h-12 text-blue-500 mb-4" />
                  <p className="text-lg font-bold text-gray-700">
                    {file ? file.name : "Choose CSV File"}
                  </p>
                  <p className="text-sm text-gray-400 mt-1">or drag and drop here</p>
                </div>
                <Button
                  onClick={uploadCSV}
                  fullWidth
                  disabled={!file || loading}
                  className="py-4 text-base font-bold"
                >
                  {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : "Process & Sample Entries"}
                </Button>
              </div>
            )}

            {/* Step 2: Sampling */}
            {samples && !results && (
              <div className="space-y-8">
                <div className="flex items-center justify-between">
                  <h2 className="text-2xl font-bold">Step 2: Sampled Entries</h2>
                  <Button onClick={reset} variant="ghost" className="text-xs">Reset</Button>
                </div>
                <p className="text-sm text-gray-500">We've picked {samples.length} random entries. Ready to cross-check?</p>

                <div className="space-y-4">
                  {samples.map((s, idx) => (
                    <div key={idx} className="p-4 bg-gray-50 rounded-2xl border border-gray-100 flex items-center justify-between">
                      <div className="flex flex-col">
                        <span className="text-xs font-bold text-gray-400">POL_ID</span>
                        <span className="text-sm font-bold text-gray-800">{s.POL_ID || "N/A"}</span>
                      </div>
                      <div className="flex flex-col items-end">
                        <span className="text-xs font-bold text-gray-400">Name</span>
                        <span className="text-sm text-gray-600 truncate max-w-[150px]">{s.LIFE_ASSURED_NAME || "N/A"}</span>
                      </div>
                    </div>
                  ))}
                </div>

                <Button
                  onClick={validateBatch}
                  fullWidth
                  disabled={validating}
                  className="py-4 text-base font-bold bg-[#FF8255] hover:bg-orange-600"
                >
                  {validating ? <Loader2 className="w-5 h-5 animate-spin mr-2" /> : <Search className="w-5 h-5 mr-2" />}
                  Cross-Check with Sheet
                </Button>
              </div>
            )}

            {/* Step 3: Results */}
            {results && (
              <div className="space-y-8">
                <div className="flex items-center justify-between">
                  <h2 className="text-2xl font-bold">Cross-Check Report</h2>
                  <Button onClick={reset} variant="ghost" className="text-xs">Start New Upload</Button>
                </div>

                <div className="space-y-6 max-h-[600px] overflow-y-auto pr-2">
                  {results.map((r, idx) => (
                    <motion.div
                      key={idx}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.1 }}
                      className={cn(
                        "p-6 rounded-3xl border",
                        r.is_valid ? "bg-green-50 border-green-100" : "bg-red-50 border-red-100"
                      )}
                    >
                      <div className="flex items-center justify-between mb-4">
                        <div className="flex items-center space-x-2">
                          <span className="text-lg font-bold text-gray-800">POL-ID: {r.csv_row.POL_ID}</span>
                        </div>
                        {r.is_valid ? <CheckCircle className="text-green-500" /> : <XCircle className="text-red-500" />}
                      </div>

                      {r.error ? (
                        <p className="text-xs text-red-600 font-medium">Error: {r.error}</p>
                      ) : (
                        <div className="grid grid-cols-1 gap-3 text-xs">
                          <div className={cn("flex justify-between p-2 rounded-xl bg-white/60", !r.name_present && "text-red-600 font-bold")}>
                            <span>Name Presence</span>
                            <span>{r.name_present ? "✅ Present" : "❌ Missing"}</span>
                          </div>
                          <div className={cn("flex justify-between p-2 rounded-xl bg-white/60", !r.email_present && "text-red-600 font-bold")}>
                            <span>Email Presence</span>
                            <span>{r.email_present ? "✅ Present" : "❌ Missing"}</span>
                          </div>
                          <div className="flex justify-between p-2 rounded-xl bg-white/60">
                            <span>Data Match (CSV vs Sheet)</span>
                            <span className={cn("font-bold", r.is_valid ? "text-green-600" : "text-red-600")}>
                              {Object.values(r.matches).filter(m => !m).length === 0 ? "Full Match" : "Mismatch Found"}
                            </span>
                          </div>
                        </div>
                      )}
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            {error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="mt-6 p-4 bg-red-50 text-red-600 rounded-2xl text-sm flex items-start space-x-3 border border-red-100"
              >
                <AlertCircle className="w-5 h-5 shrink-0" />
                <span>{error}</span>
              </motion.div>
            )}

          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default App;
