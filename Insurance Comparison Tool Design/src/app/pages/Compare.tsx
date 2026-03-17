import React from 'react';
import { useLocation, useNavigate } from 'react-router';
import { Button } from '../components/Button';
import { MOCK_POLICIES, formatCurrency } from '../store';
import { ArrowLeft, CheckCircle2, XCircle } from 'lucide-react';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

export const Compare = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const selectedIds: string[] = location.state?.selectedIds || [];
  
  if (selectedIds.length === 0) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 text-center font-['Inter']">
        <h2 className="text-2xl font-bold text-[#212529] mb-4">No policies selected for comparison</h2>
        <Button variant="primary" onClick={() => navigate('/shortlist')}>Go Back to Shortlist</Button>
      </div>
    );
  }

  const policiesToCompare = MOCK_POLICIES.filter(p => selectedIds.includes(p.id));

  // Determine the best value for each row to highlight
  const maxCover = Math.max(...policiesToCompare.map(p => p.coverAmount));
  const minPremium = Math.min(...policiesToCompare.map(p => p.priceMonthly));
  const maxCSR = Math.max(...policiesToCompare.map(p => p.claimSettlementRatio));

  const isBest = (val: number, bestVal: number, type: 'min' | 'max') => {
    return type === 'max' ? val === bestVal : val === bestVal;
  };

  return (
    <div className="min-h-screen bg-[#F8F9FA] text-[#212529] font-['Inter'] pb-32">
      <div className="max-w-7xl mx-auto p-6 md:p-12">
        <header className="mb-10 flex items-center">
          <Button variant="ghost" className="self-start -ml-4" onClick={() => navigate('/shortlist')}>
            <ArrowLeft className="w-5 h-5 mr-2" />
            Back to Shortlist
          </Button>
          <div className="ml-auto">
            <h1 className="text-2xl md:text-3xl font-extrabold tracking-tight text-[#212529]">
              Side-by-side comparison
            </h1>
          </div>
        </header>

        <div className="overflow-x-auto bg-white rounded-[24px] border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)]">
          <div className="min-w-[800px] w-full">
            
            {/* Header Row (Logos & Names) */}
            <div className="grid grid-cols-4 border-b-2 border-gray-100 bg-[#EBF5FF]/30 sticky top-0 z-10">
              <div className="p-6 flex items-end pb-4 font-bold text-sm text-[#868E96] uppercase tracking-wider">
                Compare Features
              </div>
              {policiesToCompare.map((policy) => (
                <div key={policy.id} className="p-6 flex flex-col items-center text-center pb-6 border-l border-gray-100 relative">
                  <div className="w-16 h-16 rounded-full overflow-hidden bg-white shadow-sm border border-gray-100 mb-4 flex-shrink-0">
                    <ImageWithFallback src={policy.insurerLogo} alt={policy.insurerName} className="w-full h-full object-cover" />
                  </div>
                  <h3 className="font-bold text-[#212529] text-xl leading-tight">{policy.planName}</h3>
                  <p className="text-sm text-[#868E96] mt-1">{policy.insurerName}</p>
                </div>
              ))}
              {/* Padding columns if less than 3 selected */}
              {Array.from({ length: 3 - policiesToCompare.length }).map((_, i) => (
                <div key={i} className="p-6 border-l border-gray-50"></div>
              ))}
            </div>

            {/* Row: Cover Amount */}
            <div className="grid grid-cols-4 border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
              <div className="p-6 font-medium text-[#212529] flex items-center">
                Cover Amount
              </div>
              {policiesToCompare.map((policy) => (
                <div key={policy.id} className={`p-6 border-l border-gray-50 flex items-center justify-center text-lg font-bold
                  ${isBest(policy.coverAmount, maxCover, 'max') ? 'bg-[#EBF5FF] text-[#007BFF]' : 'text-[#212529]'}
                `}>
                  {formatCurrency(policy.coverAmount)}
                </div>
              ))}
            </div>

            {/* Row: Monthly Premium */}
            <div className="grid grid-cols-4 border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
              <div className="p-6 font-medium text-[#212529] flex items-center">
                Monthly Premium
              </div>
              {policiesToCompare.map((policy) => (
                <div key={policy.id} className={`p-6 border-l border-gray-50 flex items-center justify-center text-lg font-bold
                  ${isBest(policy.priceMonthly, minPremium, 'min') ? 'bg-[#EBF5FF] text-[#007BFF]' : 'text-[#212529]'}
                `}>
                  {formatCurrency(policy.priceMonthly)}/mo
                </div>
              ))}
            </div>

            {/* Row: Room Rent Limit */}
            <div className="grid grid-cols-4 border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
              <div className="p-6 font-medium text-[#212529] flex items-center">
                Room Rent Limit
              </div>
              {policiesToCompare.map((policy) => {
                const isNoLimit = policy.roomRentLimit === 'No Limit';
                return (
                  <div key={policy.id} className={`p-6 border-l border-gray-50 flex flex-col items-center justify-center text-center
                    ${isNoLimit ? 'bg-[#EBF5FF]' : ''}
                  `}>
                    {isNoLimit ? (
                      <CheckCircle2 className="w-6 h-6 text-green-500 mb-1" />
                    ) : (
                      <span className="text-gray-400 mb-1">—</span>
                    )}
                    <span className={`text-sm ${isNoLimit ? 'font-bold text-[#007BFF]' : 'text-[#212529]'}`}>
                      {policy.roomRentLimit}
                    </span>
                  </div>
                );
              })}
            </div>

            {/* Row: Claim Settlement Ratio */}
            <div className="grid grid-cols-4 border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
              <div className="p-6 font-medium text-[#212529] flex items-center">
                Claim Settlement Ratio
              </div>
              {policiesToCompare.map((policy) => (
                <div key={policy.id} className={`p-6 border-l border-gray-50 flex items-center justify-center text-lg font-bold
                  ${isBest(policy.claimSettlementRatio, maxCSR, 'max') ? 'bg-[#EBF5FF] text-[#007BFF]' : 'text-[#212529]'}
                `}>
                  {policy.claimSettlementRatio}%
                </div>
              ))}
            </div>
            
            {/* Row: Copay */}
            <div className="grid grid-cols-4 border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
              <div className="p-6 font-medium text-[#212529] flex items-center">
                No Copayment
              </div>
              {policiesToCompare.map((policy) => {
                const hasNoCopay = policy.features.some(f => f.toLowerCase().includes('no copay') || f.toLowerCase().includes('no sub-limit'));
                return (
                  <div key={policy.id} className={`p-6 border-l border-gray-50 flex items-center justify-center
                     ${hasNoCopay ? 'bg-[#EBF5FF]' : ''}
                  `}>
                    {hasNoCopay ? (
                      <CheckCircle2 className="w-8 h-8 text-green-500" />
                    ) : (
                      <XCircle className="w-8 h-8 text-red-400" />
                    )}
                  </div>
                );
              })}
            </div>

          </div>
        </div>
      </div>

      {/* Sticky Bottom Actions */}
      <div className="fixed bottom-0 left-0 right-0 p-6 bg-white border-t border-gray-100 shadow-[0_-10px_40px_rgba(0,0,0,0.05)] z-50">
        <div className="max-w-7xl mx-auto overflow-x-auto">
          <div className="min-w-[800px] w-full grid grid-cols-4">
            {/* Empty first column for alignment */}
            <div></div>
            {/* Action buttons matching policy columns */}
            {policiesToCompare.map((policy) => (
              <div key={policy.id} className="px-6 flex items-center justify-center">
                <Button 
                  variant="primary" 
                  fullWidth
                  className="py-3 shadow-md font-bold text-base whitespace-nowrap"
                  onClick={() => alert(`Proceeding with ${policy.planName} by ${policy.insurerName}`)}
                >
                  Finalize {policy.insurerName}
                </Button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
