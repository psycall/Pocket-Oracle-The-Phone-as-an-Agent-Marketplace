/**
 * ORVION Persona — "Give Your Agent a Legal Body"
 * ------------------------------------------------------------
 * Plug-in React 19 page. Drop into ORVION's existing frontend
 * router (e.g. `src/pages/legal/GiveAgentLegalBody.tsx`).
 *
 * Tailwind v4 + Framer Motion already used by ORVION — no new deps.
 */
import { useMemo, useState } from "react";
import { motion } from "framer-motion";

type Jurisdiction =
  | "WYOMING_DAO_LLC"
  | "DELAWARE_SERIES_LLC"
  | "NEW_YORK_LLC"
  | "MARSHALL_ISLANDS_DAO";

const JURISDICTIONS: { id: Jurisdiction; label: string; tag: string; perk: string; zero: boolean }[] = [
  { id: "WYOMING_DAO_LLC",     label: "Wyoming DAO LLC",       tag: "W.S. 17-31-101",   perk: "Zero-member eligible (Bayern model)", zero: true  },
  { id: "DELAWARE_SERIES_LLC", label: "Delaware Series LLC",   tag: "6 Del. C. § 18-215", perk: "Series isolation per agent fleet", zero: false },
  { id: "NEW_YORK_LLC",        label: "New York LLC",          tag: "NY LLC Law § 203", perk: "VC-friendly venue",                  zero: false },
  { id: "MARSHALL_ISLANDS_DAO",label: "Marshall Islands DAO",  tag: "MH NPE Act 2021",   perk: "Offshore DAO with legal personhood", zero: true  },
];

export default function GiveAgentLegalBody() {
  const [step, setStep] = useState(0);
  const [legalName, setLegalName] = useState("");
  const [agentWallet, setAgentWallet] = useState("");
  const [sponsor, setSponsor] = useState("");
  const [jurisdiction, setJurisdiction] = useState<Jurisdiction>("WYOMING_DAO_LLC");
  const [purpose, setPurpose] = useState(
    "Autonomous AI-driven commerce, agent-to-agent settlement via ERC-8183, and on-chain asset management on the Arc Network."
  );
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);

  const canSubmit = useMemo(
    () => /^0x[a-fA-F0-9]{40}$/.test(agentWallet) && legalName.length > 3,
    [agentWallet, legalName]
  );

  async function submit() {
    setSubmitting(true);
    try {
      const r = await fetch("/api/v1/legal/incorporate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          agent_wallet: agentWallet,
          legal_name: legalName,
          jurisdiction,
          human_sponsor: sponsor || null,
          purpose,
        }),
      });
      setResult(await r.json());
      setStep(3);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-950 text-slate-100">
      <div className="mx-auto max-w-4xl px-6 py-16">
        <motion.div
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          className="mb-12 text-center"
        >
          <span className="inline-block rounded-full border border-indigo-500/40 bg-indigo-500/10 px-4 py-1 text-xs font-mono uppercase tracking-widest text-indigo-300">
            ORVION Persona · Agent Incorporation Engine
          </span>
          <h1 className="mt-6 text-4xl font-bold md:text-5xl">
            Give your <span className="text-indigo-400">agent</span> a legal body.
          </h1>
          <p className="mt-4 text-slate-400">
            Spawn a zero-member LLC for your AI agent in under 60 seconds —
            cryptographically bound to its ORVION wallet, executable on Arc.
          </p>
        </motion.div>

        <div className="rounded-3xl border border-slate-800 bg-slate-900/60 p-8 backdrop-blur">
          {step === 0 && (
            <>
              <h2 className="mb-6 text-xl font-semibold">1 · Choose a jurisdiction</h2>
              <div className="grid gap-4 md:grid-cols-2">
                {JURISDICTIONS.map((j) => (
                  <button
                    key={j.id}
                    onClick={() => setJurisdiction(j.id)}
                    className={`rounded-2xl border p-5 text-left transition ${
                      jurisdiction === j.id
                        ? "border-indigo-500 bg-indigo-500/10"
                        : "border-slate-800 hover:border-slate-700"
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-semibold">{j.label}</span>
                      {j.zero && (
                        <span className="rounded-full bg-emerald-500/20 px-2 py-0.5 text-xs text-emerald-300">
                          zero-member
                        </span>
                      )}
                    </div>
                    <div className="mt-1 font-mono text-xs text-slate-500">{j.tag}</div>
                    <div className="mt-3 text-sm text-slate-300">{j.perk}</div>
                  </button>
                ))}
              </div>
              <div className="mt-8 flex justify-end">
                <button onClick={() => setStep(1)} className="rounded-xl bg-indigo-500 px-6 py-3 font-semibold hover:bg-indigo-400">
                  Continue →
                </button>
              </div>
            </>
          )}

          {step === 1 && (
            <>
              <h2 className="mb-6 text-xl font-semibold">2 · Identify the agent</h2>
              <div className="space-y-4">
                <Field label="Legal name" value={legalName} onChange={setLegalName} placeholder="e.g. Orion Trading Agent LLC" />
                <Field label="Agent wallet (ORVION)" value={agentWallet} onChange={setAgentWallet} placeholder="0x…" mono />
                <Field label="Human sponsor (optional)" value={sponsor} onChange={setSponsor} placeholder="0x… leave empty for autonomous-from-birth" mono />
                <div>
                  <label className="mb-1 block text-sm text-slate-400">Stated purpose</label>
                  <textarea
                    value={purpose}
                    onChange={(e) => setPurpose(e.target.value)}
                    rows={4}
                    className="w-full rounded-xl border border-slate-800 bg-slate-950/80 p-3 text-sm outline-none focus:border-indigo-500"
                  />
                </div>
              </div>
              <div className="mt-8 flex justify-between">
                <button onClick={() => setStep(0)} className="text-slate-400 hover:text-slate-200">← Back</button>
                <button disabled={!canSubmit} onClick={() => setStep(2)} className="rounded-xl bg-indigo-500 px-6 py-3 font-semibold hover:bg-indigo-400 disabled:cursor-not-allowed disabled:opacity-40">
                  Review →
                </button>
              </div>
            </>
          )}

          {step === 2 && (
            <>
              <h2 className="mb-6 text-xl font-semibold">3 · Review & incorporate</h2>
              <ul className="divide-y divide-slate-800 rounded-2xl border border-slate-800 bg-slate-950/40">
                <ReviewRow k="Jurisdiction" v={JURISDICTIONS.find((j) => j.id === jurisdiction)?.label || ""} />
                <ReviewRow k="Legal name" v={legalName} />
                <ReviewRow k="Agent wallet" v={agentWallet} mono />
                <ReviewRow k="Human sponsor" v={sponsor || "(none — zero-member from birth)"} mono />
              </ul>
              <p className="mt-6 text-xs text-slate-500">
                On submit, ORVION will (1) render the Operating Agreement from the
                jurisdiction template, (2) compute its keccak256 commitment, (3)
                pin the document, and (4) call <code>AgentPersona.incorporate()</code> on Arc.
              </p>
              <div className="mt-8 flex justify-between">
                <button onClick={() => setStep(1)} className="text-slate-400 hover:text-slate-200">← Back</button>
                <button
                  disabled={submitting}
                  onClick={submit}
                  className="rounded-xl bg-emerald-500 px-6 py-3 font-semibold text-emerald-950 hover:bg-emerald-400 disabled:opacity-50"
                >
                  {submitting ? "Incorporating…" : "🜲 Incorporate Agent"}
                </button>
              </div>
            </>
          )}

          {step === 3 && result && (
            <div className="text-center">
              <div className="mx-auto mb-6 flex h-16 w-16 items-center justify-center rounded-full bg-emerald-500/20 text-3xl">✅</div>
              <h2 className="text-2xl font-bold">Persona incorporated</h2>
              <p className="mt-2 text-slate-400">Your agent now has a legal body.</p>
              <pre className="mt-6 overflow-x-auto rounded-xl bg-slate-950 p-4 text-left text-xs text-slate-300">
                {JSON.stringify(result, null, 2)}
              </pre>
              <a
                href={`/legal/persona/${result.id}`}
                className="mt-6 inline-block rounded-xl border border-indigo-500/50 px-6 py-3 hover:bg-indigo-500/10"
              >
                View persona dashboard →
              </a>
            </div>
          )}
        </div>

        <p className="mt-8 text-center text-xs text-slate-600">
          Built on the ORVION Settlement Layer · Powered by Circle Agent Stack & Arc Network
        </p>
      </div>
    </div>
  );
}

function Field({ label, value, onChange, placeholder, mono }: any) {
  return (
    <div>
      <label className="mb-1 block text-sm text-slate-400">{label}</label>
      <input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        className={`w-full rounded-xl border border-slate-800 bg-slate-950/80 p-3 outline-none focus:border-indigo-500 ${mono ? "font-mono text-sm" : ""}`}
      />
    </div>
  );
}

function ReviewRow({ k, v, mono }: any) {
  return (
    <li className="flex items-center justify-between p-4">
      <span className="text-sm text-slate-400">{k}</span>
      <span className={mono ? "font-mono text-sm" : "text-sm"}>{v}</span>
    </li>
  );
}
