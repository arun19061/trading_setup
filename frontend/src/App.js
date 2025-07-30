import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line } from 'react-chartjs-2';

function App() {
  const [symbol, setSymbol] = useState('RELIANCE.NS');
  const [data, setData] = useState(null);
  const [portfolio, setPortfolio] = useState(null);
  const [logs, setLogs] = useState([]);

  const fetchData = async () => {
    const res = await axios.get(`http://localhost:8000/strategy/${symbol}`);
    setData(res.data);
  };

  const fetchPortfolio = async () => {
    const res = await axios.get(`http://localhost:8000/portfolio`);
    setPortfolio(res.data);
  };

  const fetchLogs = async () => {
    const res = await axios.get(`http://localhost:8000/logs`);
    setLogs(res.data);
  };

  useEffect(() => {
    fetchData();
    fetchPortfolio();
    fetchLogs();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>Trading Dashboard</h2>
      <input value={symbol} onChange={(e) => setSymbol(e.target.value)} />
      <button onClick={fetchData}>Run Strategy</button>
      {data && (
        <Line data={{
          labels: data.dates,
          datasets: [
            { label: "Close", data: data.close, borderColor: "blue" },
            { label: "SMA20", data: data.sma20, borderColor: "green" },
            { label: "SMA50", data: data.sma50, borderColor: "red" }
          ]
        }} />
      )}
      {portfolio && (
        <div>
          <h4>Portfolio</h4>
          <p>Cash: ₹{portfolio.cash.toFixed(2)}</p>
          <p>In Position: {portfolio.in_position ? "Yes" : "No"}</p>
          <p>Quantity: {portfolio.position.toFixed(2)}</p>
        </div>
      )}
      <h4>Trade Logs</h4>
      <ul>
        {logs.map((log, i) => (
          <li key={i}>{log.timestamp} - {log.action} @ ₹{log.price}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
