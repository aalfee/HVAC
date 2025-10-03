import React, { useState } from 'react';

const Simulation: React.FC = () => {
  const [buildingId, setBuildingId] = useState('');
  const [startTime, setStartTime] = useState('');
  const [endTime, setEndTime] = useState('');
  const [parameters, setParameters] = useState('');
  const [result, setResult] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const response = await fetch('/api/simulate/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          building_id: buildingId,
          start_time: startTime,
          end_time: endTime,
          parameters: parameters ? JSON.parse(parameters) : {},
        }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || data.error || 'Simulation failed');
      setResult(JSON.stringify(data, null, 2));
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Simulation Control</h2>
      <form onSubmit={handleSubmit} className="space-y-4 bg-white p-6 rounded shadow">
        <div>
          <label htmlFor="buildingId" className="block font-semibold">Building ID</label>
          <input id="buildingId" type="text" className="w-full border p-2 rounded" value={buildingId} onChange={e => setBuildingId(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="startTime" className="block font-semibold">Start Time</label>
          <input id="startTime" type="datetime-local" className="w-full border p-2 rounded" value={startTime} onChange={e => setStartTime(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="endTime" className="block font-semibold">End Time</label>
          <input id="endTime" type="datetime-local" className="w-full border p-2 rounded" value={endTime} onChange={e => setEndTime(e.target.value)} required />
        </div>
        <div>
          <label htmlFor="parameters" className="block font-semibold">Parameters (JSON)</label>
          <textarea id="parameters" className="w-full border p-2 rounded" value={parameters} onChange={e => setParameters(e.target.value)} placeholder='{"temp": 22, "humidity": 50}' rows={2} />
        </div>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>
          {loading ? 'Running...' : 'Run Simulation'}
        </button>
      </form>
      {result && (
        <div className="mt-6 bg-green-50 border border-green-200 p-4 rounded">
          <div className="font-semibold mb-2">Result:</div>
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

export default Simulation;
