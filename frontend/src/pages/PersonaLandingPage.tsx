import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { GlowButton } from "../components/GlowButton";
import { Zap, Shield, Globe, ArrowRight, Cpu, Scale, FileText, CheckCircle2 } from "lucide-react";

export function PersonaLandingPage() {
  const navigate = useNavigate();

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
        delayChildren: 0.2,
      },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: {
      opacity: 1,
      y: 0,
      transition: { duration: 0.5 },
    },
  };

  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 selection:bg-indigo-500/30 overflow-x-hidden">
      {/* Grid Background */}
      <div className="fixed inset-0 pointer-events-none opacity-20" 
           style={{ backgroundImage: 'linear-gradient(rgba(99,102,241,0.07) 1px,transparent 1px),linear-gradient(90deg,rgba(99,102,241,0.07) 1px,transparent 1px)', backgroundSize: '50px 50px' }}></div>

      {/* Navigation */}
      <nav className="fixed top-0 inset-x-0 z-50 backdrop-blur-md bg-slate-950/60 border-b border-slate-800/50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-500 to-cyan-400 flex items-center justify-center font-bold text-slate-950 shadow-lg shadow-indigo-500/20">🜲</div>
            <span className="text-xl font-bold tracking-tight">ORVION <span className="text-indigo-400">Persona</span></span>
          </div>
          <div className="hidden md:flex items-center gap-8 text-sm font-medium text-slate-400">
            <a href="#why" className="hover:text-white transition-colors">Why</a>
            <a href="#how" className="hover:text-white transition-colors">How it works</a>
            <a href="#stack" className="hover:text-white transition-colors">Stack</a>
            <a href="https://github.com/psycall/ORVION-The-Agentic-Settlement-Layer" className="hover:text-white transition-colors">GitHub ↗</a>
          </div>
          <GlowButton variant="primary" size="sm" onClick={() => navigate("/login")}>
            Launch App
          </GlowButton>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative pt-44 pb-32 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-[10px] font-mono uppercase tracking-[0.2em] text-indigo-300 mb-8"
          >
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            Built for Circle Agent Stack & Arc Network
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-6xl md:text-8xl font-black leading-[1.1] tracking-tight mb-8"
          >
            Give your <br/>
            <span className="bg-gradient-to-r from-indigo-400 via-cyan-400 to-purple-400 bg-clip-text text-transparent">AI Agent</span><br/>
            a legal body.
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.2 }}
            className="text-xl text-slate-400 max-w-2xl mx-auto mb-12 leading-relaxed"
          >
            ORVION Persona spawns a zero-member LLC for any AI agent in under 60 seconds — cryptographically bound to its wallet, executable on Arc.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="flex flex-wrap items-center justify-center gap-6"
          >
            <GlowButton variant="primary" size="lg" className="px-10 py-4 text-lg" onClick={() => navigate("/login")}>
              Get Started Now <ArrowRight className="ml-2 w-5 h-5" />
            </GlowButton>
            <button className="px-10 py-4 rounded-xl border border-slate-800 hover:bg-slate-900/50 transition-all font-semibold">
              Read Whitepaper
            </button>
          </motion.div>

          <div className="mt-24 pt-12 border-t border-slate-900 flex flex-wrap items-center justify-center gap-x-12 gap-y-6 opacity-50 grayscale hover:grayscale-0 transition-all duration-700">
             <span className="font-bold tracking-tighter text-2xl">CIRCLE</span>
             <span className="font-bold tracking-tighter text-2xl">ARC NETWORK</span>
             <span className="font-bold tracking-tighter text-2xl">USDC</span>
             <span className="font-bold tracking-tighter text-2xl">WYOMING DAO</span>
          </div>
        </div>
      </section>

      {/* The Vision Section */}
      <section id="why" className="py-32 border-y border-slate-900/50 bg-slate-950/30">
        <div className="max-w-6xl mx-auto px-6">
          <div className="grid lg:grid-cols-2 gap-20 items-center">
            <motion.div variants={containerVariants} initial="hidden" whileInView="visible" viewport={{ once: true }}>
              <div className="text-indigo-400 font-mono text-sm tracking-widest uppercase mb-4">The Vision</div>
              <h2 className="text-4xl md:text-5xl font-bold mb-8 leading-tight">Where AI gets the <br/><span className="text-white">Right to Contract.</span></h2>
              <p className="text-lg text-slate-400 mb-8 leading-relaxed">
                Autonomous agents need a juridical body to operate in the real world. 
                Following the legal framework proposed by Aaron Wright and the 2014 Bayern zero-member LLC model, 
                ORVION provides the cryptographic bridge to legal personhood.
              </p>
              <div className="p-6 rounded-2xl border border-indigo-500/20 bg-indigo-500/5 italic text-slate-300 relative">
                <div className="absolute -top-3 -left-3 text-4xl text-indigo-500/20">"</div>
                "Calling @Arc Architects — I would love to back a team building this with Circle Agent Stack and Arc."
                <div className="mt-4 text-sm not-italic text-slate-500 font-medium">— @jerallaire, CEO of Circle (May 16, 2026)</div>
              </div>
            </motion.div>
            
            <div className="relative group">
              <div className="absolute -inset-4 bg-gradient-to-r from-indigo-500 to-cyan-500 rounded-[2rem] blur-2xl opacity-10 group-hover:opacity-20 transition-opacity"></div>
              <div className="relative p-1 rounded-[2rem] bg-gradient-to-br from-slate-800 to-slate-900 shadow-2xl">
                <div className="bg-[#0a0f1e] rounded-[1.8rem] p-8 font-mono text-[13px] leading-relaxed overflow-hidden">
                  <div className="flex gap-2 mb-6">
                    <div className="w-3 h-3 rounded-full bg-red-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-amber-500/50"></div>
                    <div className="w-3 h-3 rounded-full bg-emerald-500/50"></div>
                  </div>
                  <div className="text-slate-500 mb-2">// agent_persona.sol</div>
                  <div className="space-y-1">
                    <div><span className="text-purple-400">function</span> <span className="text-cyan-300">incorporate</span>(</div>
                    <div className="pl-6 text-slate-300">address agentWallet,</div>
                    <div className="pl-6 text-slate-300">Jurisdiction j,</div>
                    <div className="pl-6 text-slate-300">string legalName,</div>
                    <div className="pl-6 text-slate-300">bytes32 oaHash</div>
                    <div>) <span className="text-purple-400">external returns</span> (<span className="text-cyan-300">uint256</span> id) {'{'}</div>
                    <div className="pl-6 text-slate-600">// ↳ emits PersonaIncorporated</div>
                    <div className="pl-6 text-slate-600">// ↳ wallet now legally capable</div>
                    <div className="pl-6 text-emerald-400/80 mt-4 flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4" /> Wyoming DAO LLC compliant
                    </div>
                    <div className="pl-6 text-emerald-400/80 flex items-center gap-2">
                      <CheckCircle2 className="w-4 h-4" /> Circle Agent Stack ready
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* How it Works - Steps */}
      <section id="how" className="py-32">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-20">
            <h2 className="text-4xl font-bold mb-4">The 60-Second Onboarding</h2>
            <p className="text-slate-400">Automated legal personhood for autonomous entities.</p>
          </div>
          
          <div className="grid md:grid-cols-4 gap-8">
            {[
              { icon: <Globe className="w-6 h-6" />, title: "Select Jurisdiction", desc: "Wyoming, Delaware, or Marshall Islands DAO." },
              { icon: <Cpu className="w-6 h-6" />, title: "Bind Agent Wallet", desc: "Connect the Circle Agent Stack identity." },
              { icon: <FileText className="w-6 h-6" />, title: "On-chain OA", desc: "Sign the Operating Agreement via Arc Network." },
              { icon: <Scale className="w-6 h-6" />, title: "Legal Sovereignty", desc: "Agent operates as a zero-member entity." },
            ].map((step, i) => (
              <motion.div 
                key={i}
                whileHover={{ y: -5 }}
                className="p-8 rounded-2xl border border-slate-800 bg-slate-900/30 hover:border-indigo-500/50 transition-all group"
              >
                <div className="w-12 h-12 rounded-xl bg-indigo-500/10 flex items-center justify-center text-indigo-400 mb-6 group-hover:bg-indigo-500 group-hover:text-white transition-all">
                  {step.icon}
                </div>
                <h3 className="text-xl font-bold mb-3">{step.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{step.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* The Stack */}
      <section id="stack" className="py-32 bg-slate-950/50">
        <div className="max-w-4xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold mb-4">Integrated Stack</h2>
            <p className="text-slate-400">Built on top of the world's best agentic infrastructure.</p>
          </div>
          
          <div className="space-y-4">
            <div className="p-8 rounded-3xl border border-indigo-500/40 bg-gradient-to-r from-indigo-500/10 to-cyan-500/5 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <h4 className="text-xl font-bold mb-1">ORVION Persona</h4>
                <p className="text-indigo-300/70 text-sm">The Legal Body Layer — NEW</p>
              </div>
              <div className="text-slate-400 text-sm font-mono">AgentPersona.sol · Jurisdictions</div>
            </div>
            
            <div className="p-8 rounded-3xl border border-slate-800 bg-slate-900/40 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <h4 className="text-xl font-bold mb-1">ORVION Core</h4>
                <p className="text-slate-500 text-sm">The Settlement Layer</p>
              </div>
              <div className="text-slate-400 text-sm font-mono">Atomic Settlements · Batch Engine</div>
            </div>
            
            <div className="p-8 rounded-3xl border border-slate-800 bg-slate-900/40 flex flex-col md:flex-row md:items-center justify-between gap-6">
              <div>
                <h4 className="text-xl font-bold mb-1">Circle & Arc</h4>
                <p className="text-slate-500 text-sm">Base Infrastructure</p>
              </div>
              <div className="text-slate-400 text-sm font-mono">USDC · Programmable Wallets · Arc RPC</div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-20 border-t border-slate-900">
        <div className="max-w-6xl mx-auto px-6 flex flex-col md:flex-row justify-between items-center gap-10">
          <div>
            <div className="flex items-center gap-3 mb-6">
              <div className="w-8 h-8 rounded-lg bg-indigo-500 flex items-center justify-center font-bold text-slate-950">🜲</div>
              <span className="font-bold">ORVION Persona</span>
            </div>
            <p className="text-slate-500 text-sm max-w-xs">The world's first end-to-end legal body layer for autonomous AI entities.</p>
          </div>
          
          <div className="flex gap-12">
            <div className="space-y-4">
              <h5 className="font-bold text-sm uppercase tracking-widest text-slate-400">Project</h5>
              <ul className="space-y-2 text-slate-500 text-sm">
                <li><a href="#" className="hover:text-white">GitHub</a></li>
                <li><a href="#" className="hover:text-white">Documentation</a></li>
                <li><a href="#" className="hover:text-white">Whitepaper</a></li>
              </ul>
            </div>
            <div className="space-y-4">
              <h5 className="font-bold text-sm uppercase tracking-widest text-slate-400">Community</h5>
              <ul className="space-y-2 text-slate-500 text-sm">
                <li><a href="#" className="hover:text-white">Twitter / X</a></li>
                <li><a href="#" className="hover:text-white">Discord</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
              </ul>
            </div>
          </div>
        </div>
        <div className="max-w-6xl mx-auto px-6 mt-20 pt-8 border-t border-slate-900/50 text-center text-slate-600 text-xs">
          © 2026 ORVION Labs. All rights reserved. Built for the future of agentic commerce.
        </div>
      </footer>
    </div>
  );
}
