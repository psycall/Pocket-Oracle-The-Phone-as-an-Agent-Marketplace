import { useState, useRef, useEffect } from 'react';
import { useAccount } from 'wagmi';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}

export function ChatAgent() {
  const { address } = useAccount();
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: 'assistant', 
      content: '👋 Olá! Conecte sua wallet e me diga o que fazer. Ex: "Faça um swap de 100 USDC para ETH na Arbitrum"',
      timestamp: new Date().toLocaleTimeString()
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const recognition = useRef<any>(null);
  const chatWindowRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

  const sendCommand = async () => {
    if (!input.trim() || !address) return;
    
    const userMessage: Message = { 
      role: 'user', 
      content: input,
      timestamp: new Date().toLocaleTimeString()
    };
    
    const historyToSend = messages.map(m => ({ role: m.role, content: m.content }));
    
    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/agent/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          command: currentInput, 
          wallet_address: address,
          history: historyToSend
        })
      });
      
      const data = await res.json();
      const assistantMessage: Message = {
        role: 'assistant',
        content: data.response || 'Erro ao processar comando',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage: Message = {
        role: 'assistant',
        content: '❌ Erro de conexão com o agente. Verifique se o backend está rodando.',
        timestamp: new Date().toLocaleTimeString()
      };
      setMessages(prev => [...prev, errorMessage]);
    }
    setLoading(false);
  };

  const startVoiceInput = () => {
    const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Voz não suportada no seu navegador.");
      return;
    }

    recognition.current = new SpeechRecognition();
    recognition.current.lang = 'pt-BR';
    recognition.current.continuous = false;
    recognition.current.interimResults = false;

    recognition.current.onstart = () => setIsListening(true);
    recognition.current.onend = () => setIsListening(false);

    recognition.current.onresult = (event: any) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      setTimeout(() => sendCommand(), 500);
    };

    recognition.current.onerror = (event: any) => {
      console.error('Erro de voz:', event.error);
      setIsListening(false);
    };

    recognition.current.start();
  };

  const stopVoiceInput = () => {
    if (recognition.current) {
      recognition.current.stop();
      setIsListening(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white p-6">
      <style>{`
        .glass-effect {
          background: rgba(15, 23, 42, 0.8);
          backdrop-filter: blur(10px);
          border: 1px solid rgba(148, 163, 184, 0.1);
        }
        .glow-text {
          background: linear-gradient(135deg, #00d9ff, #ffd60a);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
        .pulse-glow {
          box-shadow: 0 0 20px rgba(0, 217, 255, 0.5);
        }
      `}</style>

      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-5xl font-black glow-text mb-2">ORVION Agentic</h1>
          <p className="text-slate-400 text-sm">Agente autônomo de finanças descentralizadas</p>
        </div>

        {/* Chat Container */}
        <div className="glass-effect rounded-3xl h-[75vh] flex flex-col overflow-hidden shadow-2xl">
          {/* Messages */}
          <div 
            ref={chatWindowRef}
            className="flex-1 p-8 overflow-y-auto space-y-6"
          >
            {messages.map((msg, i) => (
              <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-5 rounded-2xl transition-all ${
                  msg.role === 'user' 
                    ? 'bg-gradient-to-r from-blue-600 to-blue-500 shadow-lg' 
                    : 'bg-slate-800 border border-slate-700'
                }`}>
                  <p className="text-base leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                  <p className="text-xs mt-2 opacity-60">{msg.timestamp}</p>
                </div>
              </div>
            ))}
            {loading && (
              <div className="flex justify-start">
                <div className="bg-slate-800 border border-slate-700 p-5 rounded-2xl">
                  <p className="text-emerald-400 animate-pulse">🤖 Agente pensando...</p>
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <div className="p-6 border-t border-slate-700 flex gap-3 bg-slate-900/50">
            <button 
              onClick={isListening ? stopVoiceInput : startVoiceInput}
              disabled={!address}
              className={`px-6 py-3 rounded-2xl text-2xl transition font-bold ${
                isListening
                  ? 'bg-red-600 hover:bg-red-500 pulse-glow'
                  : 'bg-slate-800 hover:bg-slate-700 disabled:opacity-50'
              }`}
            >
              {isListening ? '⏹️' : '🎤'}
            </button>
            <input
              value={input}
              onChange={e => setInput(e.target.value)}
              onKeyDown={e => e.key === 'Enter' && !loading && sendCommand()}
              placeholder={address ? "Digite ou fale seu comando..." : "Conecte sua wallet primeiro..."}
              disabled={!address}
              className="flex-1 bg-slate-800 border border-slate-700 rounded-2xl px-6 py-4 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 text-lg disabled:opacity-50 transition"
            />
            <button 
              onClick={sendCommand}
              disabled={loading || !address || !input.trim()}
              className="bg-gradient-to-r from-emerald-600 to-emerald-500 hover:from-emerald-500 hover:to-emerald-400 px-10 rounded-2xl font-bold disabled:opacity-50 transition shadow-lg hover:shadow-emerald-500/50"
            >
              Enviar
            </button>
          </div>
        </div>

        {/* Status Footer */}
        <div className="mt-6 text-center text-slate-400 text-sm">
          {address ? (
            <p>✅ Wallet conectada: <span className="text-emerald-400 font-mono">{address.slice(0, 6)}...{address.slice(-4)}</span></p>
          ) : (
            <p>⚠️ Conecte sua wallet para começar</p>
          )}
        </div>
      </div>
    </div>
  );
}
