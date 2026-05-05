import React from 'react';

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="max-w-7xl mx-auto px-4 py-20">
        <div className="text-center">
          <h1 className="text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500 mb-4">
            ORVION
          </h1>
          <p className="text-2xl text-gray-300 mb-8">
            The Agentic Settlement Layer
          </p>
          <p className="text-lg text-gray-400 mb-12 max-w-2xl mx-auto">
            Trustless payments for autonomous agents on Arc Network, powered by Circle USDC
          </p>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
            <div className="bg-slate-800 p-8 rounded-lg border border-cyan-500/20">
              <h3 className="text-xl font-bold text-cyan-400 mb-4">Instant Settlement</h3>
              <p className="text-gray-400">Real-time USDC payments on Arc Network</p>
            </div>
            <div className="bg-slate-800 p-8 rounded-lg border border-blue-500/20">
              <h3 className="text-xl font-bold text-blue-400 mb-4">Trustless Execution</h3>
              <p className="text-gray-400">Smart contracts ensure fairness and transparency</p>
            </div>
            <div className="bg-slate-800 p-8 rounded-lg border border-purple-500/20">
              <h3 className="text-xl font-bold text-purple-400 mb-4">Scalable</h3>
              <p className="text-gray-400">1000+ TPS for mass adoption</p>
            </div>
          </div>

          <div className="flex gap-4 justify-center">
            <a href="https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer" 
               className="px-8 py-3 bg-cyan-500 text-black font-bold rounded-lg hover:bg-cyan-400 transition">
              GitHub
            </a>
            <a href="/docs" 
               className="px-8 py-3 bg-slate-700 text-white font-bold rounded-lg hover:bg-slate-600 transition">
              Documentation
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
