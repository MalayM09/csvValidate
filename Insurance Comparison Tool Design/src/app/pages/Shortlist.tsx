import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { Button } from '../components/Button';
import { PolicyCard } from '../components/PolicyCard';
import { MOCK_POLICIES } from '../store';
import { ArrowLeft } from 'lucide-react';

export const Shortlist = () => {
  const navigate = useNavigate();
  const [selectedPolicies, setSelectedPolicies] = useState<string[]>([]);

  const toggleSelect = (id: string) => {
    setSelectedPolicies(prev => {
      if (prev.includes(id)) {
        return prev.filter(p => p !== id);
      }
      if (prev.length >= 3) {
        // limit to 3 for comparison
        return prev;
      }
      return [...prev, id];
    });
  };

  const handleCompare = () => {
    if (selectedPolicies.length > 0) {
      navigate('/compare', { state: { selectedIds: selectedPolicies } });
    }
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] text-[#212529] font-['Inter'] pb-32">
      <div className="max-w-6xl w-full mx-auto p-6 md:p-12">
        
        <header className="mb-12 flex flex-col md:flex-row md:items-center gap-6">
          <Button variant="ghost" className="self-start -ml-4" onClick={() => navigate('/')}>
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Form
          </Button>
          <div className="md:ml-auto md:text-right">
            <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight text-[#212529]">
              Here are your top matches.
            </h1>
            <p className="text-[#868E96] mt-2">Select up to 3 to compare side-by-side.</p>
          </div>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {MOCK_POLICIES.map(policy => (
            <PolicyCard
              key={policy.id}
              policy={policy}
              showCheckbox={true}
              isSelected={selectedPolicies.includes(policy.id)}
              onToggleSelect={toggleSelect}
            />
          ))}
        </div>
      </div>

      {/* Sticky Bottom Bar */}
      <div 
        className={`fixed bottom-0 left-0 right-0 p-6 bg-white border-t border-gray-100 shadow-[0_-10px_40px_rgba(0,0,0,0.05)] transform transition-transform duration-300 z-50 ${
          selectedPolicies.length > 0 ? 'translate-y-0' : 'translate-y-full'
        }`}
      >
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div>
            <span className="font-semibold text-lg text-[#212529]">{selectedPolicies.length}</span>
            <span className="text-[#868E96] ml-2">selected for comparison</span>
          </div>
          <Button 
            variant="secondary" 
            onClick={handleCompare}
            disabled={selectedPolicies.length === 0}
            className="px-8 py-3.5 text-base font-bold shadow-md"
          >
            Compare Selected ({selectedPolicies.length})
          </Button>
        </div>
      </div>
    </div>
  );
};
