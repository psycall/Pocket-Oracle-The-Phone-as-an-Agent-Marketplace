const services = [
  { title: 'GeoProof', price: '$0.0015', description: 'Prova rápida de localização com contexto de campo.' },
  { title: 'SnapOCR', price: '$0.0040', description: 'Leitura curta de texto para recibos, placas e etiquetas.' },
  { title: 'HumanTap Verify', price: '$0.0060', description: 'Confirmação humana rápida para agentes que precisam de certeza operacional.' }
];

export default function Page() {
  return (
    <main className="page">
      <section className="hero">
        <p className="eyebrow">Pocket Oracle</p>
        <h1>The phone as an agent marketplace.</h1>
        <p className="lead">
          Uma experiência mobile-first para transformar smartphones em interfaces de trabalho e monetização para agentes autônomos.
        </p>
      </section>

      <section className="grid">
        {services.map((service) => (
          <article className="card" key={service.title}>
            <div className="price">{service.price}</div>
            <h2>{service.title}</h2>
            <p>{service.description}</p>
            <button>Run paid task</button>
          </article>
        ))}
      </section>

      <section className="panel">
        <h2>Use cases</h2>
        <p>
          Delivery verification, field audit, proof-of-presence, short OCR flows and local human confirmation for machine-to-machine commerce.
        </p>
      </section>
    </main>
  );
}
