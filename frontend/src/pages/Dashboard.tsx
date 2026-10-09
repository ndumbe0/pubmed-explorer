import { useState, useEffect } from 'react';

export default function Dashboard() {
  const [summary, setSummary] = useState<any>(null);

  useEffect(() => {
    fetch('/api/facets/summary')
      .then(r => r.json())
      .then(setSummary)
      .catch(() => {});
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-blue-100 p-4 rounded">
            <h2 className="text-xl font-semibold">Total Papers</h2>
            <p className="text-3xl">{summary.total}</p>
          </div>
        </div>
      )}
    </div>
  );
}
