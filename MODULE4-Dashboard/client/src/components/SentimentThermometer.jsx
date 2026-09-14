import React from 'react';

/**
 * Component: SentimentThermometer
 * Purpose: Visualizes the NLP sentiment using a stylized circular meter.
 *          High contrast colors dominate the interface when "PANIC" is triggered.
 */
const SentimentThermometer = ({ label }) => {
  const isPanic = label === 'PANIC';
  
  // Design configuration based on state
  const colorClass = isPanic ? 'text-alertRed' : 'text-bullishGreen';
  const shadowClass = isPanic ? 'shadow-[0_0_30px_rgba(239,68,68,0.3)]' : 'shadow-none';
  const strokeColor = isPanic ? '#ef4444' : '#22c55e';
  
  // Calculate SVG circle properties for the meter
  const radius = 60;
  const circumference = 2 * Math.PI * radius;
  // If PANIC, fill the meter to 90%, if not, maybe 75% for positive
  const fillPercentage = isPanic ? 90 : 75;
  const strokeDashoffset = circumference - (fillPercentage / 100) * circumference;

  return (
    <div className={`bg-darkSurface rounded-xl p-6 border ${isPanic ? 'border-red-900/50' : 'border-gray-800'} flex flex-col items-center justify-between h-full transition-all duration-500 ${shadowClass}`}>
      <div className="w-full text-center mb-4">
        <h2 className="text-xl font-semibold text-gray-200">AI Sentiment Engine</h2>
        <p className="text-sm text-gray-500 mt-1">Real-time NLP Market Analysis</p>
      </div>
      
      {/* Circular SVG Meter */}
      <div className="relative flex items-center justify-center mb-4">
        <svg className="transform -rotate-90 w-40 h-40">
          {/* Background Track */}
          <circle 
            cx="80" 
            cy="80" 
            r={radius} 
            stroke="currentColor" 
            strokeWidth="12" 
            fill="transparent"
            className="text-gray-800"
          />
          {/* Progress Indicator */}
          <circle 
            cx="80" 
            cy="80" 
            r={radius} 
            stroke={strokeColor} 
            strokeWidth="12" 
            fill="transparent"
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-1000 ease-in-out"
          />
        </svg>
        
        {/* Centered Label */}
        <div className="absolute flex flex-col items-center justify-center">
          <span className={`text-2xl font-black tracking-widest uppercase ${colorClass}`}>
            {label || 'WAIT'}
          </span>
        </div>
      </div>
      
      <div className="w-full text-center mt-2">
        <p className={`text-sm font-medium px-4 py-2 rounded bg-gray-900 inline-block ${isPanic ? 'text-red-400 border border-red-900/50' : 'text-gray-400'}`}>
          {isPanic ? 'Extreme bearish signals detected' : 'Market conditions stable'}
        </p>
      </div>
    </div>
  );
};

export default SentimentThermometer;
