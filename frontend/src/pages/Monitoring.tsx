import React, { useEffect, useState } from 'react';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

type SensorRow = {
  timestamp: string;
  temp: number;
  humidity: number;
  co2: number;
};

const fallbackData: SensorRow[] = [
  { timestamp: '2025-10-03T10:00', temp: 22.1, humidity: 48, co2: 420 },
  { timestamp: '2025-10-03T10:05', temp: 22.3, humidity: 47, co2: 425 },
  { timestamp: '2025-10-03T10:10', temp: 22.2, humidity: 49, co2: 430 },
];

const Monitoring: React.FC = () => {
  const [data, setData] = useState<SensorRow[]>(fallbackData);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch('/api/ingest/')
      .then(res => res.ok ? res.json() : Promise.reject(res))
      .then(json => {
        if (Array.isArray(json)) setData(json);
      })
      .catch(() => setError('Could not fetch real sensor data, showing mock data.'));
  }, []);

  return (
    <div className="p-8 max-w-3xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Monitoring</h2>
      <p className="mb-4">View real-time and historical HVAC sensor data here.</p>
      {error && <div className="mb-4 text-red-600">{error}</div>}
      <div className="bg-white p-4 rounded shadow mb-6">
        <div className="font-semibold mb-2">Sensor Data (last {data.length} samples):</div>
        <table className="w-full text-left border">
          <thead>
            <tr className="bg-gray-100">
              <th className="p-2">Timestamp</th>
              <th className="p-2">Temperature (°C)</th>
              <th className="p-2">Humidity (%)</th>
              <th className="p-2">CO₂ (ppm)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, i) => (
              <tr key={i} className="border-t">
                <td className="p-2">{row.timestamp}</td>
                <td className="p-2">{row.temp}</td>
                <td className="p-2">{row.humidity}</td>
                <td className="p-2">{row.co2}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="bg-white p-4 rounded shadow">
        <div className="font-semibold mb-2">Temperature Over Time</div>
        <Line
          data={{
            labels: data.map(row => row.timestamp),
            datasets: [
              {
                label: 'Temperature (°C)',
                data: data.map(row => row.temp),
                borderColor: 'rgb(37, 99, 235)',
                backgroundColor: 'rgba(37, 99, 235, 0.2)',
                tension: 0.3,
              },
            ],
          }}
          options={{
            responsive: true,
            plugins: {
              legend: { display: true, position: 'top' },
              title: { display: false },
            },
            scales: {
              x: { title: { display: true, text: 'Timestamp' } },
              y: { title: { display: true, text: 'Temperature (°C)' } },
            },
          }}
        />
      </div>
    </div>
  );
};

export default Monitoring;
