import React from "react";

function HistoryList({ history }) {
  if (!history || history.length === 0) return <p>No recent searches</p>;

  return (
    <div className="history-list">
      <h3>Recent Searches</h3>
      <ul>
        {history.map((entry, index) => (
          <li key={index}>
            {entry.city} – {entry.temperature}°C – {entry.description}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default HistoryList;
