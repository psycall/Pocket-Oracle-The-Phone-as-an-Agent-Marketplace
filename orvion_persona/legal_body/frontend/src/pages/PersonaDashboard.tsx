/**
 * Persona dashboard — lists incorporated agents and exposes
 * sign / amend / dissociate actions.
 */
import { useEffect, useState } from "react";
import { motion } from "framer-motion";

type Persona = {
  id: number;
  on_chain_id?: number;
  agent_wallet: string;
  legal_name: string;
  jurisdiction: string;
  status: string;
  human_sponsor?: string | null;
  operating_agreement_hash?: string;
  incorporated_at?: string;
};

export default function PersonaDashboard() {
  const [items, setItems] = useState<Persona[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/v1/legal/personas")
      .then((r) => r.json())
      .then((d) => setItems(d.items || []))
      .finally(() => setLoading(false));
  }, []);

  async function dissociate(persona_id: number) {
    if (!confirm("Transition this persona to a zero-member configuration?")) return;
    await fetch("/api/v1/legal/dissociate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ persona_id, reason: "User-initiated transition to autonomy" }),
    });
    setItems((xs) =>
      xs.map((p) => (p.id === persona_id ? { ...p, human_sponsor: null } : p))
    );
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-6xl px-6 py-12">
        <h1 className="text-3xl font-bold">Legal Personas</h1>
        <p className="mt-2 text-slate-400">Agents currently incorporated through ORVION Persona.</p>

        {loading ? (
          <div className="mt-12 text-center text-slate-500">Loading…</div>
        ) : items.length === 0 ? (
          <div className="mt-12 rounded-2xl border border-dashed border-slate-800 p-12 text-center text-slate-500">
            No personas yet. <a href="/legal/incorporate" className="text-indigo-400 underline">Incorporate one</a>.
          </div>
        ) : (
          <div className="mt-8 grid gap-4 md:grid-cols-2">
            {items.map((p, i) => (
              <motion.div
                key={p.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.04 }}
                className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6"
              >
                <div className="flex items-center justify-between">
                  <h3 className="font-semibold">{p.legal_name}</h3>
                  <span className={`rounded-full px-2 py-0.5 text-xs ${statusColor(p.status)}`}>
                    {p.status}
                  </span>
                </div>
                <div className="mt-3 space-y-1 font-mono text-xs text-slate-400">
                  <div>Wallet&nbsp;&nbsp;: {p.agent_wallet}</div>
                  <div>Sponsor : {p.human_sponsor || "— (zero-member)"}</div>
                  <div>Jurisd. : {p.jurisdiction}</div>
                  <div>OA hash : {p.operating_agreement_hash?.slice(0, 14)}…</div>
                </div>
                <div className="mt-4 flex gap-2">
                  <a href={`/legal/persona/${p.id}`} className="rounded-lg border border-slate-700 px-3 py-1.5 text-xs hover:bg-slate-800">
                    Details
                  </a>
                  {p.human_sponsor && (
                    <button
                      onClick={() => dissociate(p.id)}
                      className="rounded-lg border border-amber-500/40 px-3 py-1.5 text-xs text-amber-300 hover:bg-amber-500/10"
                    >
                      Dissociate → zero-member
                    </button>
                  )}
                </div>
              </motion.div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

function statusColor(s: string) {
  switch (s) {
    case "INCORPORATED": return "bg-emerald-500/20 text-emerald-300";
    case "PENDING":      return "bg-amber-500/20 text-amber-300";
    case "SUSPENDED":    return "bg-orange-500/20 text-orange-300";
    case "DISSOLVED":    return "bg-rose-500/20 text-rose-300";
    default:             return "bg-slate-700/40 text-slate-300";
  }
}
