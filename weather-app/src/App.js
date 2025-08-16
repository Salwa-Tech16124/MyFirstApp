import './App.css';
import React, { useState } from "react";
import SearchBar from "./components/SearchBar.jsx";
import WeatherCard from "./components/WeatherCard.jsx";
import HistoryList from "./components/HistoryList.jsx";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

function App() {
  const [weather, setWeather] = useState(null);
  const [history, setHistory] = useState([]);

  const fetchWeather = async (city) => {
    try {
      // Fetch weather data
      const response = await fetch(`${BACKEND_URL}/weather/${city}`);
      const data = await response.json();

      if (data.error) {
        alert(data.error);
        return;
      }

      setWeather(data);

      // Fetch updated history
      const historyRes = await fetch(`${BACKEND_URL}/history`);
      const historyData = await historyRes.json();
      setHistory(historyData);

    } catch (error) {
      console.error("Error fetching weather:", error);
    }
  };

  return (
    <div className="app-container">
      <h1>Weather App</h1>
      <SearchBar onSearch={fetchWeather} />
      {weather && <WeatherCard weather={weather} />}
      <HistoryList history={history} />
    </div>
  );
}

export default App;
