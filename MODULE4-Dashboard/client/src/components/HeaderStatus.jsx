import React from 'react';

/**
 * Component: HeaderStatus
 * Purpose: Displays the overall system status and the timestamp of the last data update.
 */
const HeaderStatus = ({ lastUpdate }) => {
  return (
    <header className="flex justify-between items-center py-6 border-b border-gray-700 mb-8">
      <div>
        <h1 className="text-3xl font-bold tracking-tight text-white">Quant Terminal</h1>
        <p className="text-gray-400 mt-1">Module 4: Secure Data Visualization</p>
      </div>
      
      <div className="flex flex-col items-end">
        <div className="flex items-center space-x-2">
          {/* Pulsing green dot indicates active connection */}
          <span className="relative flex h-3 w-3">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-bullishGreen opacity-75"></span>
            <span className="relative inline-flex rounded-full h-3 w-3 bg-bullishGreen"></span>
          </span>
          <span className="text-sm font-medium text-gray-300">System Online</span>
        </div>
        {lastUpdate && (
          <span className="text-xs text-gray-500 mt-1">Last Sync: {new Date(lastUpdate).toLocaleTimeString()}</span>
        )}
      </div>
    </header>
  );
};

export default HeaderStatus;
