import React, { useState, useEffect } from "react";
import "./App.css";

const images = [
  "/images/CorvetteSting.jpg",
  "/images/Porsche911Carrera4.png",
  "/images/PorscheCayman.png"
];

function App() {
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % images.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="slideshow-container">
      {images.map((img, index) => (
        <img
          key={index}
          src={img}
          alt={`slide-${index}`}
          className={`slide ${index === currentIndex ? "active" : ""}`}
        />
      ))}
    </div>
  );
}

export default App;
