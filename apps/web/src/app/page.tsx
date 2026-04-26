"use client"

import { useState, useRef } from "react"

// ── Types ─────────────────────────────────────────────────────

interface StreamEvent {
  type: string
  task_id?: string
  message?: string
  agent?: string
  routing?: Record<string, unknown>
  data?: Record<string, unknown>
  duration_ms?: number
}

interface ExecutionLog {
  id: string
  type: string
  message: string
  timestamp: number
  data?: unknown
}

// ── Main Dashboard ─────────────────────────────────────────────

export default function Dashboard() {
  const [goal, setGoal] = useState("")
  const [apiKey, setApiKey] = useState("")
  const [token, setToken] = useState("")
  const [logs, setLogs] = useState<ExecutionLog[]>([])
  const [isRunning, setIsRunning] = useState(false)
  const [result, setResult] = useState<Record<string, unknown> | null>(null)
  const abortRef = useRef<AbortController | null>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"

  // ── Auth ────────────────────────────────────────────────────
  const authenticate = async () => {
    const res = await fetch(`${API_URL}/node/token`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: apiKey }),
    })
    if (!res.ok) throw new Error("Auth failed — check your API key")
    const data = await res.json()
    setToken(data.access_token)
    return data.access_token
  }

  // ── Execution ────────────────────────────────────────────────
  const execute = async () => {
    if (!goal.trim()) return
    setIsRunning(true)
    setLogs([])
    setResult(null)

    const addLog = (event: StreamEvent) => {
      const messages: Record<string, string> = {
        started: `⚡ Task started — ID: ${event.task_id}`,
        routing: `🧭 ${event.message ?? "Analyzing goal..."}`,
        routed: `✅ Routed to agent: ${event.agent?.toUpperCase()}`,
        executing: `🤖 ${event.message ?? "Executing..."}`,
        result: `📦 Result received`,
        complete: `✓ Done in ${event.duration_ms}ms`,
      }
      setLogs(prev => [
        ...prev,
        {
          id: `${Date.now()}-${Math.random()}`,
          type: event.type,
          message: messages[event.type] ?? event.type,
          timestamp: Date.now(),
          data: event.data ?? event.routing,
        },
      ])
      if (event.type === "result" && event.data) {
        setResult(event.data as Record<string, unknown>)
      }
    }

    try {
      const activeToken = token || (await authenticate())
      abortRef.current = new AbortController()

      const res = await fetch(`${API_URL}/agent/execute/stream`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${activeToken}`,
        },
        body: JSON.stringify({ goal, context: {} }),
        signal: abortRef.current.signal,
      })

      if (!res.body) throw new Error("No stream body")
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ""

      while (true) {
        const { done, value } = await reader.read()
        if (done) break
        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split("\n")
        buffer = lines.pop() ?? ""
        for (const line of lines) {
          if (line.startsWith("data: ")) {
            try {
              const event = JSON.parse(line.slice(6)) as StreamEvent
              addLog(event)
            } catch { /* skip */ }
          }
        }
      }
    } catch (err: unknown) {
      if ((err as Error).name !== "AbortError") {
        setLogs(prev => [...prev, {
          id: `err-${Date.now()}`, type: "error",
          message: `❌ Error: ${(err as Error).message}`,
          timestamp: Date.now(),
        }])
      }
    } finally {
      setIsRunning(false)
    }
  }

  // ── UI ──────────────────────────────────────────────────────
  return (
    <div className="dashboard">
      <header className="header">
        <div className="node-badge">
          <span className="pulse" />
          <span>ORVION NODE</span>
        </div>
        <h1>Execution Dashboard</h1>
        <p>Goal → Engine → Result</p>
      </header>

      <main className="main">
        {/* Config */}
        <section className="card">
          <label className="label">API KEY</label>
          <input
            className="input"
            type="password"
            placeholder="Your Orvion API key"
            value={apiKey}
            onChange={e => setApiKey(e.target.value)}
          />
          {token && <p className="token-ok">✓ Authenticated</p>}
        </section>

        {/* Goal input */}
        <section className="card">
          <label className="label">GOAL</label>
          <textarea
            className="textarea"
            placeholder="e.g. Analyze crypto trends and find the best opportunity right now"
            value={goal}
            onChange={e => setGoal(e.target.value)}
            rows={3}
          />
          <button
            className={`btn ${isRunning ? "btn-stop" : "btn-run"}`}
            onClick={isRunning ? () => abortRef.current?.abort() : execute}
          >
            {isRunning ? "⏹ STOP" : "▶ EXECUTE"}
          </button>
        </section>

        {/* Live logs */}
        {logs.length > 0 && (
          <section className="card">
            <label className="label">EXECUTION STREAM</label>
            <div className="logs">
              {logs.map(log => (
                <div key={log.id} className={`log-line log-${log.type}`}>
                  <span className="log-time">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                  <span>{log.message}</span>
                </div>
              ))}
              {isRunning && <div className="log-line log-running">◌ running...</div>}
            </div>
          </section>
        )}

        {/* Result */}
        {result && (
          <section className="card result-card">
            <label className="label">RESULT</label>
            <pre className="result-json">{JSON.stringify(result, null, 2)}</pre>
          </section>
        )}
      </main>

      <style jsx>{`
        * { box-sizing: border-box; margin: 0; padding: 0; }
        .dashboard { background: #060a0f; min-height: 100vh; color: #c8d8e8; font-family: 'Courier New', monospace; }
        .header { background: #0d1520; border-bottom: 1px solid rgba(0,212,170,0.2); padding: 24px 32px; }
        .node-badge { display: flex; align-items: center; gap: 8px; color: #00d4aa; font-size: 11px; letter-spacing: 3px; margin-bottom: 8px; }
        .pulse { width: 8px; height: 8px; border-radius: 50%; background: #00d4aa; box-shadow: 0 0 10px #00d4aa; animation: pulse 2s infinite; }
        @keyframes pulse { 0%,100%{opacity:1}50%{opacity:0.3} }
        h1 { font-size: 28px; color: #fff; letter-spacing: 1px; }
        p { color: #5a7a8a; font-size: 13px; margin-top: 4px; }
        .main { max-width: 800px; margin: 0 auto; padding: 32px 24px; display: flex; flex-direction: column; gap: 16px; }
        .card { background: #0d1520; border: 1px solid rgba(0,212,170,0.15); border-radius: 12px; padding: 20px; }
        .label { display: block; color: #00d4aa; font-size: 10px; letter-spacing: 3px; margin-bottom: 10px; }
        .input, .textarea { width: 100%; background: #060a0f; border: 1px solid rgba(255,255,255,0.1); border-radius: 8px; color: #c8d8e8; font-family: monospace; font-size: 13px; padding: 10px 14px; outline: none; resize: vertical; }
        .input:focus, .textarea:focus { border-color: rgba(0,212,170,0.4); }
        .token-ok { color: #00d4aa; font-size: 11px; margin-top: 6px; }
        .btn { width: 100%; margin-top: 12px; padding: 12px; border: none; border-radius: 8px; font-family: monospace; font-size: 13px; letter-spacing: 2px; cursor: pointer; font-weight: bold; transition: all 0.2s; }
        .btn-run { background: #00d4aa; color: #000; }
        .btn-run:hover { background: #00f0c0; }
        .btn-stop { background: rgba(255,59,59,0.2); border: 1px solid rgba(255,59,59,0.4); color: #ff3b3b; }
        .logs { display: flex; flex-direction: column; gap: 6px; max-height: 300px; overflow-y: auto; }
        .log-line { display: flex; gap: 12px; font-size: 12px; padding: 6px 10px; border-radius: 6px; background: rgba(0,0,0,0.3); }
        .log-time { color: #3a5a6a; flex-shrink: 0; }
        .log-started, .log-complete { color: #00d4aa; }
        .log-routing, .log-routed { color: #aad4ff; }
        .log-executing { color: #f0c040; }
        .log-result { color: #c8d8e8; }
        .log-error { color: #ff3b3b; }
        .log-running { color: #3a5a6a; animation: pulse 1s infinite; }
        .result-card { border-color: rgba(0,212,170,0.3); }
        .result-json { font-size: 12px; line-height: 1.6; color: #00d4aa; overflow-x: auto; white-space: pre-wrap; word-break: break-word; max-height: 400px; overflow-y: auto; }
      `}</style>
    </div>
  )
}
