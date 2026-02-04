"use client";

import { useEffect, useState } from "react";
import Navbar from "../../components/Navbar";

export default function DailySummary() {

  const [summary, setSummary] = useState("Loading...");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/summary/daily")
      .then(res => res.json())
      .then(data => {
        setSummary(data.summary);   // ✅ VERY IMPORTANT
        setLoading(false);
      })
      .catch(err => {
        console.error(err);
        setSummary("Failed to load summary");
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <p className="text-green-400 p-6">Generating summary...</p>;
  }

  return (
    <div className="min-h-screen bg-black text-green-400 p-6">
      <Navbar />
      <h1 className="text-2xl font-bold mb-4">Daily Summary</h1>

      <div className="bg-gray-900 p-4 rounded-xl border border-green-600 whitespace-pre-wrap">
        {summary}
      </div>
    </div>
  );
}
