const jobs = [
  { title: 'GeoProof verification', state: 'Ready now', payout: '$0.0015',
    detail: 'Confirm last-mile delivery coordinates and attach confidence score.' },
  { title: 'SnapOCR receipt read', state: 'Queue 02', payout: '$0.0040',
    detail: 'Capture the receipt, extract structured text and return it to the agent.' },
  { title: 'HumanTap escalation', state: 'Priority', payout: '$0.0060',
    detail: 'Approve or reject an edge-case answer when the autonomous flow needs certainty.' }
];

const stats = [
  { label: 'Today', value: '19 jobs' },
  { label: 'Acceptance', value: '94%' },
  { label: 'Response SLA', value: '12s' }
];

export default function Page() {
  return (
    <main className="page">
      <section className="phoneFrame">
        <header className="hero">
          <p className="eyebrow">Operator app</p>
          <h1>Pocket Oracle on mobile</h1>
          <p className="lead">
            A believable operator experience for demos: jobs, payouts, urgency and one-tap escalation in a phone-native UI.
          </p>
        </header>

        <section className="stats">
          {stats.map((item) => (
            <article className="statCard" key={item.label}>
              <span>{item.label}</span>
              <strong>{item.value}</strong>
            </article>
          ))}
        </section>

        <section className="queueCard">
          <div className="sectionHead">
            <h2>Live queue</h2>
            <span>3 services</span>
          </div>
          <div className="jobList">
            {jobs.map((job) => (
              <article className="jobCard" key={job.title}>
                <div className="jobTop">
                  <div>
                    <h3>{job.title}</h3>
                    <p>{job.detail}</p>
                  </div>
                  <span className="badge">{job.state}</span>
                </div>
                <div className="jobBottom">
                  <strong>{job.payout}</strong>
                  <button>Accept task</button>
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="panel">
          <h2>Why this matters</h2>
          <p>
            Investors can now see the last-mile piece of the thesis. The phone is not decoration — it is the operational bridge between automation and the physical world.
          </p>
        </section>

        <nav className="bottomNav">
          <a className="active">Queue</a>
          <a>Wallet</a>
          <a>Proofs</a>
          <a>Profile</a>
        </nav>
      </section>
    </main>
  );
}
