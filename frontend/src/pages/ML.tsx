import { useState } from 'react';

export default function ML() {
  const [status, setStatus] = useState<any>(null);
  
  const fetchStatus = async () => {
    const r = await fetch('/api/ml/status');
    setStatus(await r.json());
  };
  
  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Machine Learning</h1>
      <button onClick={fetchStatus} className="bg-blue-500 text-white px-4 py-2 rounded">
        Check Status
      </button>
      {status && (
        <pre className="mt-4 p-4 bg-gray-100 rounded">{JSON.stringify(status, null, 2)}</pre>
      )}
    </div>
  );
}
