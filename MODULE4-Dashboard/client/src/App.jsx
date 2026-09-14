import React, { useState, useEffect } from 'react';
import axios from 'axios';
import HeaderStatus from './components/HeaderStatus';
import CriticalAlert from './components/CriticalAlert';
import SentimentThermometer from './components/SentimentThermometer';
import AssetGrid from './components/AssetGrid';

function App() {
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  /**
   * Fetches the latest portfolio and NLP sentiment data from our Express API.
   */
  const fetchData = async () => {
    try {
      setLoading(true);
      // Ensure the Node API is running on localhost:3000
      const response = await axios.get('http://localhost:3000/api/portfolio/status');
      
      if (response.data && response.data.success) {
        setPortfolioData(response.data.data);
        setError(null);
      } else {
        setError("Invalid response format from API.");
      }
    } catch (err) {
      console.error("Error fetching data:", err);
      setError("Failed to connect to the backend server.");
    } finally {
      setLoading(false);
    }
  };

  // Fetch data on initial component mount
  useEffect(() => {
    fetchData();
    
    // Optional: Setup polling for real-time updates
    // const interval = setInterval(fetchData, 10000);
    // return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen p-4 sm:p-8">
      <div className="max-w-6xl mx-auto">
        
        {/* Top Header */}
        <HeaderStatus lastUpdate={portfolioData?.timestamp} />

        {/* Loading and Error States */}
        {loading && !portfolioData && (
          <p className="text-gray-400 text-center py-10 animate-pulse">Establishing secure connection to Quant Core...</p>
        )}
        
        {error && (
          <div className="bg-red-900 border border-alertRed text-white p-4 rounded text-center">
            {error}
          </div>
        )}

        {/* Main Dashboard Content */}
        {portfolioData && (
          <main>
            {/* HCI Rule: Break flow for critical alerts */}
            <CriticalAlert 
              severity={portfolioData.alert_severity} 
              action={portfolioData.action_signal}
              asset={portfolioData.asset}
            />

            {/* Core Data Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              {/* Asset Metrics (Takes up 2/3 width on desktop) */}
              <div className="md:col-span-2">
                <AssetGrid data={portfolioData} />
              </div>

              {/* Sentiment NLP Analysis (Takes up 1/3 width on desktop) */}
              <div className="md:col-span-1">
                <SentimentThermometer label={portfolioData.sentiment_label} />
              </div>

            </div>
          </main>
        )}

      </div>
    </div>
  );
}

export default App;
