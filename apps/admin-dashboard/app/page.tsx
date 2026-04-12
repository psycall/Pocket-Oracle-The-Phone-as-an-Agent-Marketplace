const metrics = [
  { label: 'Paid requests', value: '150' },
  { label: 'Average response time', value: '1.2s' },
  { label: 'Settlement mode', value: 'Mock / Circle-ready' },
  { label: 'Available services', value: '3' }
];

const jobs = [
  { id: 'JOB-401', service: 'GeoProof', status: 'Completed', operator: 'device-sp-01' },
  { id: 'JOB-402', service: 'SnapOCR', status: 'Completed', operator: 'device-rj-03' },
  { id: 'JOB-403', service: 'HumanTap Verify', status: 'Queued', operator: 'device-bh-02' }
];

export default function Page() {
  return (
    <main className="page">
      <header className="hero">
        <div>
          <p className="eyebrow">Executive control plane</p>
          <h1>Pocket Oracle Dashboard</h1>
          <p className="lead">Visão operacional para métricas de requests pagos, status de execução e readiness de submissão.</p>
        </div>
      </header>

      <section className="metrics">
        {metrics.map((metric) => (
          <article className="metricCard" key={metric.label}>
            <span>{metric.label}</span>
            <strong>{metric.value}</strong>
          </article>
        ))}
      </section>

      <section className="tableCard">
        <h2>Latest jobs</h2>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Service</th>
              <th>Status</th>
              <th>Operator</th>
            </tr>
          </thead>
          <tbody>
            {jobs.map((job) => (
              <tr key={job.id}>
                <td>{job.id}</td>
                <td>{job.service}</td>
                <td>{job.status}</td>
                <td>{job.operator}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
