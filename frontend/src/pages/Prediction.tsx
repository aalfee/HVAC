import React, { useState } from 'react';

const Prediction: React.FC = () => {
  const [sensorData, setSensorData] = useState('');
  const [timestamp, setTimestamp] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch('/api/predict/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          sensor_data: JSON.parse(sensorData),
          timestamp: timestamp,
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || data.error || 'Prediction failed');
      setResult(JSON.stringify(data, null, 2));
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Fault Prediction</h2>
      <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded shadow">
        <div>
          <label className="block font-semibold">Sensor Data (JSON array, shape [n_samples, 3])</label>
          <textarea className="w-full border p-2 rounded" value={sensorData} onChange={e => setSensorData(e.target.value)} placeholder='[[22.1, 48, 420], [22.3, 47, 425]]' rows={3} required />
        </div>
        <div>
          <label className="block font-semibold">Timestamp</label>
          <input type="datetime-local" className="w-full border p-2 rounded" value={timestamp} onChange={e => setTimestamp(e.target.value)} required />
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>
          {loading ? 'Predicting...' : 'Get Prediction'}
        </button>
      </form>
      {result && (
        <div className="mt-6 bg-green-50 border border-green-200 p-4 rounded">
          <div className="font-semibold mb-2">Prediction Result:</div>
          <pre className="text-sm whitespace-pre-wrap">{result}</pre>
        </div>
      )}
      {error && (
        <div className="mt-6 bg-red-50 border border-red-200 p-4 rounded text-red-700">
          Error: {error}
        </div>
      )}
    </div>
  );
};

export default Prediction;
