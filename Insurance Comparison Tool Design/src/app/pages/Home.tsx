import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import { Button } from '../components/Button';
import { Input } from '../components/Input';
import { Select } from '../components/Select';
import { ImageWithFallback } from '../components/figma/ImageWithFallback';

import heroImage from 'figma:asset/3a3f80cb4ad9ca85e317d69fc33996444626e5fc.png';

export const Home = () => {
  const navigate = useNavigate();
  const [coverageType, setCoverageType] = useState('health');
  const [age, setAge] = useState('28');
  const [priority, setPriority] = useState('low-premium');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/shortlist');
  };

  return (
    <div className="min-h-screen bg-white text-[#212529] font-['Inter'] flex items-center justify-center p-6 md:p-12 lg:p-24">
      <div className="max-w-6xl w-full mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        
        {/* Left Column */}
        <div className="flex flex-col space-y-8 max-w-lg">
          <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold tracking-tight text-[#212529] leading-[1.1]">
            Find the right policy without the headache.
          </h1>
          <p className="text-[#868E96] text-lg leading-relaxed">
            We help you navigate hundreds of insurance plans. Tell us a bit about yourself, and get a personalized, jargon-free recommendation in seconds.
          </p>
          
          <div className="relative h-64 w-full rounded-3xl overflow-hidden bg-[#EBF5FF] flex items-center justify-center">
            {/* 3D Character Graphic Placeholder/Image */}
            <ImageWithFallback 
              src={heroImage}
              alt="Friendly 3D Mascot"
              className="absolute inset-0 w-full h-full object-cover opacity-90 mix-blend-multiply"
            />
          </div>
        </div>

        {/* Right Column */}
        <div className="bg-white rounded-[24px] shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-gray-100 p-8 md:p-10 w-full max-w-md mx-auto relative z-10">
          <h2 className="text-2xl font-bold mb-6 text-[#212529]">Let's build your shortlist</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <Select 
              label="Coverage Type" 
              value={coverageType}
              onChange={(e) => setCoverageType(e.target.value)}
              options={[
                { label: 'Health Insurance', value: 'health' },
                { label: 'Term Life Insurance', value: 'term' },
                { label: 'Car Insurance', value: 'car' },
              ]}
            />
            
            <Input 
              label="Age" 
              type="number"
              min="18"
              max="100"
              value={age}
              onChange={(e) => setAge(e.target.value)}
              placeholder="e.g. 28"
            />
            
            <Select 
              label="Key Priority" 
              value={priority}
              onChange={(e) => setPriority(e.target.value)}
              options={[
                { label: 'Low Monthly Premium', value: 'low-premium' },
                { label: 'High Cover Amount', value: 'high-coverage' },
                { label: 'Quick Claim Settlement', value: 'quick-claims' },
              ]}
            />
            
            <Button type="submit" variant="primary" fullWidth className="mt-8 py-4 text-base font-semibold">
              Show My Shortlist
            </Button>
          </form>
        </div>
      </div>
    </div>
  );
};
