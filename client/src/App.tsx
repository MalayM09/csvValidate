import React, { useState } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { CheckCircle, XCircle, Search, Sheet, Mail, User, AlertCircle, Loader2 } from 'lucide-react';
import { Button } from './components/Button';
import { Input } from './components/Input';
import { Select } from './components/Select';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const API_BASE = 'http://localhost:8000';

interface SheetInfo {
  sheet_name: string;
  columns: string[];
  row_count: number;
}

interface ValidationResult {
  valid: boolean;
  column_name: string;
  column_value: string;
  name: string | null;
  email: string | null;
  is_name_present: boolean;
  is_email_present: boolean;
}

function App() {
  const [sheetId, setSheetId] = useState('');
  const [sheetInfo, setSheetInfo] = useState<SheetInfo | null>(null);
  const [lookupColumn, setLookupColumn] = useState('POL_ID');
  const [lookupValue, setLookupValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [validating, setValidating] = useState(false);
  const [result, setResult] = useState<ValidationResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const fetchSheetInfo = async () => {
    if (!sheetId) return;
    setLoading(true);
    setError(null);
    setSheetInfo(null);
    try {
      const resp = await axios.get(`${API_BASE}/api/sheet-info`, {
        params: { sheet_id: sheetId }
      });
      setSheetInfo(resp.data);
      if (resp.data.columns.includes('POL_ID')) {
        setLookupColumn('POL_ID');
      } else if (resp.data.columns.length > 0) {
        setLookupColumn(resp.data.columns[0]);
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch sheet info. Check your Sheet ID and credentials.');
    } finally {
      setLoading(false);
    }
  };

  const handleValidate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!sheetId || !lookupValue) return;

    setValidating(true);
    setError(null);
    setResult(null);
    try {
      const resp = await axios.post(`${API_BASE}/api/validate`, {
        sheet_id: sheetId,
        column_name: lookupColumn,
        column_value: lookupValue
      });
      setResult(resp.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Validation failed');
    } finally {
      setValidating(false);
    }
  };

  return (
    <div className="min-h-screen bg-white text-[#212529] font-['Inter'] flex items-center justify-center p-6 md:p-12 lg:p-20 overflow-x-hidden">
      <div className="max-w-7xl w-full mx-auto grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">

        {/* Left Column: Content */}
        <motion.div
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="flex flex-col space-y-8"
        >
          <div className="inline-flex items-center space-x-2 px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-xs font-bold tracking-wide uppercase">
            <CheckCircle className="w-3 h-3" />
            <span>Smart Validator</span>
          </div>

          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight text-[#212529] leading-[1.05]">
            Validate policy data <br />
            <span className="text-blue-600">in seconds.</span>
          </h1>

          <p className="text-[#868E96] text-xl leading-relaxed max-w-lg">
            Connect your Google Sheet and instantly verify if critical fields like names and emails are present for any policy record.
          </p>

          <div className="flex items-center space-x-6 pt-4">
            <div className="flex -space-x-3">
              {[1, 2, 3].map((i) => (
                <div key={i} className="w-12 h-12 rounded-full border-4 border-white bg-gray-100 flex items-center justify-center overflow-hidden">
                  <img src={`https://i.pravatar.cc/150?u=${i + 10}`} alt="User" />
                </div>
              ))}
            </div>
            <p className="text-sm text-gray-500 font-medium">
              Trusted by 500+ <br /> support teams
            </p>
          </div>

          <div className="relative h-48 w-full max-w-md rounded-3xl overflow-hidden bg-gradient-to-br from-blue-50 to-indigo-50 flex items-center justify-center border border-blue-100/50">
            <div className="absolute inset-0 opacity-20 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')]"></div>
            <Sheet className="w-20 h-20 text-blue-200/50" />
          </div>
        </motion.div>

        {/* Right Column: Form */}
        <motion.div
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="relative"
        >
          <div className="absolute -top-20 -right-20 w-64 h-64 bg-blue-100 rounded-full blur-3xl opacity-50 z-0"></div>

          <div className="bg-white rounded-[32px] shadow-[0_20px_50px_rgba(0,0,0,0.08)] border border-gray-100 p-8 md:p-10 w-full max-w-lg mx-auto relative z-10 backdrop-blur-sm bg-white/95">
            <h2 className="text-2xl font-bold mb-8 text-[#212529] flex items-center">
              Entry Verification
            </h2>

            <form onSubmit={handleValidate} className="space-y-6">
              <div className="flex space-x-3 items-end">
                <Input
                  label="Google Sheet ID"
                  placeholder="Paste Sheet ID here..."
                  value={sheetId}
                  onChange={(e) => setSheetId(e.target.value)}
                  className="flex-1"
                />
                <Button
                  type="button"
                  onClick={fetchSheetInfo}
                  variant="outline"
                  disabled={loading || !sheetId}
                  className="mb-0.5"
                >
                  {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : "Connect"}
                </Button>
              </div>

              <AnimatePresence>
                {sheetInfo && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }}
                    animate={{ opacity: 1, height: 'auto' }}
                    exit={{ opacity: 0, height: 0 }}
                    className="space-y-6 overflow-hidden"
                  >
                    <div className="grid grid-cols-2 gap-4">
                      <Select
                        label="Lookup Column"
                        value={lookupColumn}
                        onChange={(e) => setLookupColumn(e.target.value)}
                        options={sheetInfo.columns.map(c => ({ label: c, value: c }))}
                      />
                      <Input
                        label="Value to Find"
                        placeholder="e.g. 32662.3"
                        value={lookupValue}
                        onChange={(e) => setLookupValue(e.target.value)}
                      />
                    </div>

                    <Button
                      type="submit"
                      variant="primary"
                      fullWidth
                      disabled={validating || !lookupValue}
                      className="py-4 text-base font-bold"
                    >
                      {validating ? <Loader2 className="w-5 h-5 animate-spin mr-2" /> : <Search className="w-5 h-5 mr-2" />}
                      Check Entry
                    </Button>
                  </motion.div>
                )}
              </AnimatePresence>

              {!sheetInfo && !loading && !error && (
                <div className="py-12 border-2 border-dashed border-gray-100 rounded-2xl flex flex-col items-center justify-center text-gray-400">
                  <Sheet className="w-10 h-10 mb-2 opacity-20" />
                  <p className="text-sm font-medium">Connect a sheet to start</p>
                </div>
              )}

              {error && (
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="p-4 bg-red-50 text-red-600 rounded-2xl text-sm flex items-start space-x-3 border border-red-100"
                >
                  <AlertCircle className="w-5 h-5 shrink-0" />
                  <span>{error}</span>
                </motion.div>
              )}
            </form>

            <AnimatePresence>
              {result && (
                <motion.div
                  initial={{ opacity: 0, scale: 0.95, y: 20 }}
                  animate={{ opacity: 1, scale: 1, y: 0 }}
                  className={cn(
                    "mt-10 p-6 rounded-3xl border transition-all duration-300",
                    result.valid ? "bg-green-50 border-green-100" : "bg-red-50 border-red-100"
                  )}
                >
                  <div className="flex items-center justify-between mb-6">
                    <h3 className={cn("text-lg font-bold", result.valid ? "text-green-700" : "text-red-700")}>
                      {result.valid ? "Valid Record" : "Incomplete Record"}
                    </h3>
                    {result.valid ?
                      <CheckCircle className="w-8 h-8 text-green-500" /> :
                      <XCircle className="w-8 h-8 text-red-500" />
                    }
                  </div>

                  <div className="space-y-4">
                    <div className="bg-white/60 backdrop-blur-sm p-4 rounded-2xl flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <User className="w-5 h-5 text-gray-400" />
                        <span className="text-sm font-medium text-gray-700">Name present?</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-bold text-gray-900">{result.name || "None"}</span>
                        {result.is_name_present ?
                          <CheckCircle className="w-4 h-4 text-green-500" /> :
                          <XCircle className="w-4 h-4 text-red-500" />
                        }
                      </div>
                    </div>

                    <div className="bg-white/60 backdrop-blur-sm p-4 rounded-2xl flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <Mail className="w-5 h-5 text-gray-400" />
                        <span className="text-sm font-medium text-gray-700">Email present?</span>
                      </div>
                      <div className="flex items-center space-x-2">
                        <span className="text-sm font-bold text-gray-900 truncate max-w-[150px]">{result.email || "None"}</span>
                        {result.is_email_present ?
                          <CheckCircle className="w-4 h-4 text-green-500" /> :
                          <XCircle className="w-4 h-4 text-red-500" />
                        }
                      </div>
                    </div>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </motion.div>
      </div>
    </div>
  );
}

export default App;
