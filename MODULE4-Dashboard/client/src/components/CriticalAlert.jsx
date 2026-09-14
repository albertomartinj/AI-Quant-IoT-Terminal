import React from 'react';

/**
 * Component: CriticalAlert
 * Purpose: A high-visibility banner that breaks the normal reading flow.
 *          Implements the HCI rule of Immediate Scanning for critical alerts.
 */
const CriticalAlert = ({ severity, action, asset }) => {
  if (severity !== 'CRITICAL') return null;

  return (
    <div className="mb-8 w-full bg-alertRed text-white rounded-lg p-6 shadow-[0_0_20px_rgba(239,68,68,0.4)] animate-pulse border-2 border-red-300">
      <div className="flex items-center">
        {/* Warning Icon */}
        <svg className="w-10 h-10 mr-4 flex-shrink-0 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        
        <div>
          <h2 className="text-xl font-bold tracking-wider uppercase mb-1">
            System Alert: {severity}
          </h2>
          <p className="text-lg font-medium text-red-50">
            {asset} SIGNAL FIRED: <span className="font-black bg-white text-alertRed px-2 py-0.5 rounded ml-1">{action}</span>
          </p>
        </div>
      </div>
    </div>
  );
};

export default CriticalAlert;
