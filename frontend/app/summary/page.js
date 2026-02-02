"use client";

import Navbar from "../../components/Navbar";
import { useEmails } from "../../context/EmailContext";

export default function Summary() {

  const { emails, loading } = useEmails();

  if (loading) {
    return <p className="text-green-400 p-6">Loading summary...</p>;
  }

  const urgent = emails.filter(e => e.category === "urgent").length;
  const spam = emails.filter(e => e.category === "spam").length;
  const normal = emails.filter(e => e.category === "normal").length;

  return (
    <div className="min-h-screen bg-black text-green-400 p-6">

      <Navbar />

      <h1 className="text-2xl font-bold mb-4">Daily Summary</h1>

      <div className="bg-gray-900 p-6 rounded-xl border border-green-600 space-y-2">

        <p>Total Emails: {emails.length}</p>
        <p>Urgent: {urgent}</p>
        <p>Normal: {normal}</p>
        <p>Spam: {spam}</p>

      </div>

    </div>
  );
}
