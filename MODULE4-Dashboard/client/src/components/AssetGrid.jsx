import React from 'react';
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  Tooltip, 
  ResponsiveContainer, 
  ReferenceLine 
} from 'recharts';

/**
 * Component: AssetGrid
 * Purpose: Displays asset metrics and a minimalist historical performance chart.
 *          Implements negative space and eliminates unnecessary grid lines to reduce cognitive load.
 */
const AssetGrid = ({ data }) => {
  if (!data) return null;

  const {
    asset,
    current_price,
    entry_price,
    stop_loss_threshold
  } = data;

  // Calculate actual percentage drop and absolute stop-loss price
  const dropPercentage = (((entry_price - current_price) / entry_price) * 100).toFixed(2);
  const isDropping = current_price < entry_price;
  const stopLossPrice = entry_price * (1 - (stop_loss_threshold / 100));

  // Simulate a brief history to visualize the drop crossing the stop-loss
  const chartData = [
    { time: '09:00', price: entry_price },
    { time: '10:00', price: entry_price - (entry_price - current_price) * 0.2 },
    { time: '11:00', price: entry_price - (entry_price - current_price) * 0.5 },
    { time: '12:00', price: entry_price - (entry_price - current_price) * 0.8 },
    { time: '13:00', price: stopLossPrice + 1 }, // Approaching threshold
    { time: 'Now', price: current_price },       // Crossed threshold
  ];

  // Determine line color based on whether we crossed the stop loss
  const hasCrossedStopLoss = current_price <= stopLossPrice;
  const chartLineColor = hasCrossedStopLoss ? '#ef4444' : '#22c55e'; // alertRed vs bullishGreen

  return (
    <div className="bg-darkSurface rounded-xl p-6 shadow-lg border border-gray-800 flex flex-col h-full">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-xl font-semibold text-gray-200">Asset Tracking</h2>
        <span className="px-3 py-1 bg-gray-800 text-white rounded font-mono font-bold">{asset}</span>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        {/* Entry Price */}
        <div className="p-4 bg-gray-900 rounded-lg">
          <p className="text-sm text-gray-400 mb-1">Entry Price</p>
          <p className="text-2xl font-bold text-white">${entry_price.toFixed(2)}</p>
        </div>

        {/* Current Price */}
        <div className="p-4 bg-gray-900 rounded-lg border-l-4" style={{ borderColor: chartLineColor }}>
          <p className="text-sm text-gray-400 mb-1">Current Price</p>
          <p className={`text-2xl font-bold ${hasCrossedStopLoss ? 'text-alertRed' : 'text-bullishGreen'}`}>
            ${current_price.toFixed(2)}
          </p>
        </div>
      </div>

      {/* Recharts Minimalist Graph Area */}
      <div className="flex-grow w-full h-48 mt-4">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            {/* Minimalist Axes: Hidden lines, only essential text */}
            <XAxis dataKey="time" stroke="#475569" tick={{ fill: '#64748b', fontSize: 12 }} tickLine={false} axisLine={false} />
            <YAxis domain={['auto', 'auto']} stroke="#475569" tick={{ fill: '#64748b', fontSize: 12 }} tickLine={false} axisLine={false} />
            
            {/* Clean Tooltip for interactive probing without clutter */}
            <Tooltip 
              contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '8px' }}
              itemStyle={{ color: '#f8fafc' }}
            />
            
            {/* Critical Stop-Loss Reference Line (Dashed, High Contrast Red) */}
            <ReferenceLine 
              y={stopLossPrice} 
              stroke="#ef4444" 
              strokeDasharray="3 3" 
              label={{ position: 'top', value: 'STOP-LOSS', fill: '#ef4444', fontSize: 10, fontWeight: 'bold' }} 
            />
            
            {/* Main Price Line */}
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke={chartLineColor} 
              strokeWidth={3} 
              dot={{ r: 4, fill: '#0f172a', strokeWidth: 2 }} 
              activeDot={{ r: 6 }} 
              isAnimationActive={true}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Stop Loss Analysis Summary */}
      <div className="mt-4 pt-4 border-t border-gray-700 flex justify-between items-end">
        <p className="text-sm text-gray-400">Current Drop vs Limit</p>
        <p className={`text-lg font-mono font-bold ${hasCrossedStopLoss ? 'text-alertRed' : 'text-gray-300'}`}>
          {isDropping ? `-${dropPercentage}%` : '0.00%'} / {stop_loss_threshold}%
        </p>
      </div>
    </div>
  );
};

export default AssetGrid;
