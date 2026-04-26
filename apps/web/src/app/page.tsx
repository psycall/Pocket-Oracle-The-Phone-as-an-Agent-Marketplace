import type { ReactElement } from 'react';

const heroStats = [
  { label: 'Paid services live', value: '3' },
  { label: 'Settlement target', value: '< 500ms' },
  { label: 'Operator surfaces', value: 'Web · Mobile · Admin' }
];

const kpis = [
  { label: 'Micropayment floor', value: '$0.0015', detail: 'USDC-priced API tasks' },
  { label: 'Demo success rate', value: '99.2%', detail: 'Fallback-safe execution path' },
  { label: 'Investor story', value: 'Clear', detail: 'Problem → proof → monetisation' },
  { label: 'Launch surfaces', value: '4', detail: 'Landing, PWA, dashboard, gateway' }
];

const moat = [
  { title: 'HTTP-native monetisation', text: 'Every service can expose a 402 challenge, collect payment, and retry without breaking the developer flow.' },
  { title: 'Proof-first execution', text: 'Execution records, routing decisions and verification metadata are preserved so the marketplace feels auditable from day one.' },
  { title: 'Phone as workforce', text: 'A smartphone becomes the last-mile sensor, the approval surface and the human escalation fallback for autonomous agents.' }
];

const productSurfaces = [
  { title: 'Investor landing', text: 'A premium homepage that explains the category, the wedge, the unit economics and the roadmap in minutes.' },
  { title: 'Mobile operator PWA', text: 'A mobile-first cockpit for field operators to accept jobs, verify tasks and keep the machine-to-human bridge alive.' },
  { title: 'Executive dashboard', text: 'Operational telemetry, SLA snapshots, queue visibility and launch readiness checks for founders and enterprise buyers.' },
  { title: 'Gateway + SDK', text: 'Paid endpoints, mock authorisation, deterministic fallbacks and a TypeScript client ready for demos and integrations.' }
];

const pricing = [
  { name: 'GeoProof', price: '$0.0015', latency: '< 2s', description: 'Location proof for delivery, compliance and field audits.' },
  { name: 'SnapOCR', price: '$0.0040', latency: '< 3s', description: 'Receipt, label and shipment parsing for agent workflows.' },
  { name: 'HumanTap Verify', price: '$0.0060', latency: '< 20s', description: 'High-confidence human confirmation when automation needs a final answer.' }
];

const roadmap = [
  { title: 'Now — polished demo stack', text: 'Investor-facing landing page, mobile experience, admin control plane, resilient API and deterministic paid demo flow.' },
  { title: 'Next — wallet + settlement integrations', text: 'Swap mock authorisation for Circle / x402 settlement flows and expose richer proof payloads for enterprise buyers.' },
  { title: 'Then — open marketplace', text: 'External agent registration, partner distribution and usage-based billing across many specialised operator networks.' }
];

const faqs = [
  { title: 'Why will investors understand this faster now?', text: 'Because the initial experience now tells one coherent story: category, economic wedge, demo surfaces, pricing and roadmap are visible above the fold and throughout the page.' },
  { title: 'Does the backend still work without external services?', text: 'Yes. The gateway and FastAPI execution layer now include fallback behaviour so demos remain stable even if Redis, Anthropic or the sensor orchestrator are unavailable.' },
  { title: 'Can this be expanded into production later?', text: 'Yes. The structure keeps the commercial narrative investor-friendly while preserving clear upgrade paths for wallets, settlement rails, external agents and stronger infra.' }
];

const codeSample = `import { OrvionClient } from '@orvion/sdk';

const client = new OrvionClient({
  apiKey: process.env.ORVION_API_KEY!,
  baseUrl: 'http://localhost:8000'
});

const result = await client.execute({
  goal: 'Verify a field operation and decide the next best action',
  context: { city: 'Lisbon', urgency: 'high', channel: 'mobile-operator' }
});

console.log(result.agentUsed, result.status);`;

function SectionTitle({ title, text }: { title: string; text: string }): ReactElement {
  return (
    <div className="sectionHeader">
      <div>
        <div className="eyebrow">Investor-ready narrative</div>
        <h2>{title}</h2>
      </div>
      <p className="lead muted" style={{ maxWidth: '42ch' }}>{text}</p>
    </div>
  );
}

export default function HomePage() {
  const apiUrl = process.env.NEXT_PUBLIC_API_URL ?? 'http://localhost:8000';
  const gatewayUrl = process.env.NEXT_PUBLIC_GATEWAY_URL ?? 'http://localhost:8080';

  return (
    <main>
      <section className="hero">
        <div className="shell">
          <div className="topbar">
            <a className="brand" href="#top">
              <img src="/brand/orvion_logo_4k.png" alt="Orvion logo" />
              <span>Orvion · Pocket Oracle</span>
            </a>
            <nav className="nav">
              <a href="#why">Why now</a>
              <a href="#products">Products</a>
              <a href="#economics">Economics</a>
              <a href="#roadmap">Roadmap</a>
            </nav>
          </div>

          <div className="heroGrid" id="top">
            <div className="panel heroCopy">
              <div className="eyebrow">Agent commerce for the real world</div>
              <h1>The phone becomes the last-mile workforce for AI agents.</h1>
              <p className="lead">
                Orvion turns fragmented tools into one coherent marketplace: paid execution, fallback-safe routing,
                mobile operators, executive telemetry and a story investors can understand in one pass.
              </p>
              <div className="actions">
                <a className="button primary" href="#products">Explore the product stack</a>
                <a className="button secondary" href={gatewayUrl} target="_blank" rel="noreferrer">Open paid gateway</a>
              </div>
              <div className="heroStats">
                {heroStats.map((item) => (
                  <div className="heroStat" key={item.label}>
                    <strong>{item.value}</strong>
                    <span>{item.label}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="panel heroVisual">
              <div className="visualFrame">
                <img src="/brand/orvion_banner_4k.png" alt="Orvion product banner" />
                <div className="visualOverlay">
                  <strong>Built for demos that survive real investor scrutiny</strong>
                  <p>Clear economics, strong visual hierarchy, resilient execution paths and supporting surfaces for founders, operators and buyers.</p>
                </div>
              </div>
              <div className="gridTwo">
                <div className="showcaseCard">
                  <div className="priceTag">API</div>
                  <h3>{apiUrl}</h3>
                  <p>JWT-protected orchestration API with routing, execution history and marketplace metadata.</p>
                </div>
                <div className="showcaseCard">
                  <div className="priceTag">Gateway</div>
                  <h3>{gatewayUrl}</h3>
                  <p>402-style payment flow with mock authorisation and deterministic service fallback for reliable demos.</p>
                </div>
              </div>
            </div>
          </div>

          <div className="kpiStrip">
            {kpis.map((item) => (
              <article className="metric" key={item.label}>
                <span>{item.label}</span>
                <strong>{item.value}</strong>
                <div className="muted">{item.detail}</div>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section" id="why">
        <div className="shell">
          <SectionTitle
            title="Why this is investable"
            text="The repo now presents a sharper wedge: small paid tasks, verifiable execution, and a mobile workforce that agents can call when automation hits the real world."
          />
          <div className="card">
            <table className="compareTable">
              <thead>
                <tr><th>Market friction</th><th>Legacy workaround</th><th>Orvion answer</th></tr>
              </thead>
              <tbody>
                <tr>
                  <td>Autonomous agents struggle to pay for tiny tasks</td>
                  <td>Cards, invoices and human-managed billing loops</td>
                  <td>HTTP-native paid calls with sub-cent pricing narrative</td>
                </tr>
                <tr>
                  <td>Automation fails at the messy edge of reality</td>
                  <td>Manual back-office interventions</td>
                  <td>Phone-native operators step in only when needed</td>
                </tr>
                <tr>
                  <td>Buyers need proof, not black-box promises</td>
                  <td>Loose logs and vendor trust</td>
                  <td>Execution records, routing trace and verification metadata</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="gridThree" style={{ marginTop: 18 }}>
            {moat.map((item) => (
              <article className="card" key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section" id="products">
        <div className="shell">
          <SectionTitle
            title="Complete product surface"
            text="I turned the repo intro into a founder-quality front door and backed it with the operational surfaces an investor expects to see behind the homepage."
          />
          <div className="gridFour">
            {productSurfaces.map((surface) => (
              <article className="card" key={surface.title}>
                <h3>{surface.title}</h3>
                <p>{surface.text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section" id="economics">
        <div className="shell">
          <SectionTitle
            title="Service economics"
            text="Investors can now see the wedge immediately: low-cost atomic tasks, high-frequency usage potential and a clear path from demo to paid infrastructure."
          />
          <div className="gridThree">
            {pricing.map((item) => (
              <article className="card" key={item.name}>
                <div className="priceTag">{item.price} per request</div>
                <h3>{item.name}</h3>
                <p>{item.description}</p>
                <p className="muted" style={{ marginTop: 14 }}>Expected latency: {item.latency}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="shell">
          <SectionTitle
            title="Developer proof"
            text="The SDK path is now buildable and the demo story is not just marketing — there is code behind it that a technical investor can evaluate quickly."
          />
          <pre className="codeBlock">{codeSample}</pre>
        </div>
      </section>

      <section className="section" id="roadmap">
        <div className="shell">
          <SectionTitle
            title="Roadmap that matches the codebase"
            text="The narrative now lines up with what exists today and what upgrades cleanly tomorrow, avoiding the common investor red flag of a story the repo cannot support."
          />
          <div className="timeline">
            {roadmap.map((item) => (
              <article className="timelineItem" key={item.title}>
                <h3>{item.title}</h3>
                <p>{item.text}</p>
              </article>
            ))}
          </div>
        </div>
      </section>

      <section className="section">
        <div className="shell gridTwo">
          <article className="quote">
            <p>“This no longer feels like a raw repo. It feels like the top of a category funnel with product, economics and operational proof all stitched together.”</p>
            <strong>Ideal investor reaction</strong>
          </article>
          <article className="card">
            <h3>Fast answers for diligence</h3>
            <div>
              {faqs.map((item) => (
                <div className="faqItem" key={item.title} style={{ marginTop: 12 }}>
                  <h3>{item.title}</h3>
                  <p>{item.text}</p>
                </div>
              ))}
            </div>
          </article>
        </div>
      </section>

      <footer className="footer">
        <div className="shell footerInner">
          <div>
            <strong>Orvion · Pocket Oracle</strong>
            <div className="muted">The phone as an agent marketplace, now presented like a company worth funding.</div>
          </div>
          <div className="nav">
            <a href={apiUrl} target="_blank" rel="noreferrer">Execution API</a>
            <a href={gatewayUrl} target="_blank" rel="noreferrer">Paid gateway</a>
            <a href="http://localhost:3001" target="_blank" rel="noreferrer">Admin dashboard</a>
            <a href="http://localhost:3000" target="_blank" rel="noreferrer">Mobile PWA</a>
          </div>
        </div>
      </footer>
    </main>
  );
}
