import React from 'react';
import { Policy, formatCurrency } from '../store';
import { CheckCircle2 } from 'lucide-react';
import { Button } from './Button';
import { ImageWithFallback } from './figma/ImageWithFallback';

interface PolicyCardProps {
  policy: Policy;
  isSelected?: boolean;
  onToggleSelect?: (id: string) => void;
  showCheckbox?: boolean;
}

export const PolicyCard: React.FC<PolicyCardProps> = ({ 
  policy, 
  isSelected = false, 
  onToggleSelect,
  showCheckbox = false
}) => {
  return (
    <div className={`
      relative flex flex-col justify-between bg-white rounded-2xl p-6 border-2 transition-all duration-200
      hover:shadow-lg
      ${isSelected ? 'border-[#007BFF] bg-[#EBF5FF]/30 shadow-md' : 'border-transparent shadow-sm'}
    `}>
      {showCheckbox && (
        <div className="absolute top-4 right-4">
          <input
            type="checkbox"
            className="w-5 h-5 rounded border-gray-300 text-[#007BFF] focus:ring-[#007BFF] cursor-pointer"
            checked={isSelected}
            onChange={() => onToggleSelect && onToggleSelect(policy.id)}
          />
        </div>
      )}

      <div>
        <div className="flex items-center gap-4 mb-6">
          <div className="w-14 h-14 rounded-full overflow-hidden bg-gray-50 border border-gray-100 flex-shrink-0">
            <ImageWithFallback
              src={policy.insurerLogo}
              alt={policy.insurerName}
              className="w-full h-full object-cover"
            />
          </div>
          <div>
            <h3 className="font-bold text-[#212529] text-lg leading-tight">{policy.planName}</h3>
            <p className="text-sm text-[#868E96]">{policy.insurerName}</p>
          </div>
        </div>

        <ul className="space-y-3 mb-6">
          {policy.features.slice(0, 3).map((feature, i) => (
            <li key={i} className="flex items-start gap-2 text-sm text-[#212529]">
              <CheckCircle2 className="w-4 h-4 text-green-500 mt-0.5 flex-shrink-0" />
              <span>{feature}</span>
            </li>
          ))}
        </ul>
      </div>

      <div className="pt-5 border-t border-gray-100 flex items-end justify-between mt-auto">
        <div>
          <p className="text-xs text-[#868E96] font-medium mb-1">Monthly Premium</p>
          <div className="flex items-baseline gap-1">
            <span className="text-2xl font-bold text-[#212529]">{formatCurrency(policy.priceMonthly)}</span>
          </div>
        </div>
        
        {!showCheckbox && (
          <Button variant="primary" className="px-6 py-2">
            Select
          </Button>
        )}
      </div>
    </div>
  );
};
