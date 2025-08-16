import React from "react";

function WeatherCard({ city, temperature, humidity, icon }) {
  if (!city) return null;

  return (
    <div className="weather-card">
      <h2>{city}</h2>
      {icon && <img src={icon} alt="Weather Icon" className="weather-icon" />}
      <p>Temperature: {temperature}°C</p>
      <p>Humidity: {humidity}%</p>
    </div>
  );
}

export default WeatherCard;
