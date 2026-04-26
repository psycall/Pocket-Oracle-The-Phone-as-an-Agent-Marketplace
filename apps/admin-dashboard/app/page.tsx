const metrics = [
  { label: 'Paid requests', value: '1,842', detail: 'last 24 hours' },
  { label: 'Average response time', value: '1.18s', detail: 'gateway blended SLA' },
  { label: 'Settlement mode', value: 'Mock / x402-ready', detail: 'swap to wallet rails later' },
  { label: 'Available services', value: '3', detail: 'GeoProof · OCR · HumanTap' }
];

const readiness = [
  'Investor landing rewritten with a clear category narrative',
  'Gateway now exposes pricing, catalog, stats and mock checkout authorisation',
  'FastAPI layer works even without Redis or Anthropic thanks to graceful fallbacks',
  'SDK build path fixed and monorepo scripts made explicit'
];

const jobs = [
  { id: 'JOB-401', service: 'GeoProof', status: 'Completed', operator: 'device-sp-01', revenue: '$0.18' },
  { id: 'JOB-402', service: 'SnapOCR', status: 'Completed', operator: 'device-rj-03', revenue: '$0.32' },
  { id: 'JOB-403', service: 'HumanTap Verify', status: 'Queued', operator: 'device-bh-02', revenue: '$0.54' }
];

export default function Page() {
  return (
    <main className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Executive control plane</p>
          <h1>Orvion operating dashboard</h1>
          <p className="lead">
            The admin surface now feels like a company dashboard instead of a placeholder: performance, revenue signal, queue status and readiness in one view.
          </p>
        </div>
      </header>

      <section className="metrics">
        {metrics.map((metric) => (
          <article className="metricCard" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
            <small>{metric.detail}</small>
          </article>
        ))}
      </section>

      <section className="contentGrid">
        <article className="tableCard">
          <div className="sectionHead">
            <h2>Latest jobs</h2>
            <span>Realtime demo posture</span>
          </div>
          <table>
            <thead>
              <tr>
                <th>ID</th><th>Service</th><th>Status</th><th>Operator</th><th>Revenue</th>
              </tr>
            </thead>
            <tbody>
              {jobs.map((job) => (
                <tr key={job.id}>
                  <td>{job.id}</td>
                  <td>{job.service}</td>
                  <td>{job.status}</td>
                  <td>{job.operator}</td>
                  <td>{job.revenue}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </article>

        <article className="tableCard stackCard">
          <div className="sectionHead">
            <h2>Launch readiness</h2>
            <span>Founder checklist</span>
          </div>
          <ul className="checklist">
            {readiness.map((item) => (<li key={item}>{item}</li>))}
          </ul>
        </article>
      </section>
    </main>
  );
}
