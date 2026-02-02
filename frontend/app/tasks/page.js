"use client";

import Navbar from "../../components/Navbar";
import { useEmails } from "../../context/EmailContext";

export default function Tasks() {

  const { emails, loading } = useEmails();

  if (loading) {
    return <p className="text-green-400 p-6">Loading tasks...</p>;
  }

  // Get only emails that created tasks
const tasks = emails.filter(
  e => e.actions.task_created && e.category !== "spam"
);

  return (
    <div className="min-h-screen bg-black text-green-400 p-6">

      <Navbar />

      <h1 className="text-2xl font-bold mb-4">Tasks</h1>

      <ul className="bg-gray-900 p-4 rounded-xl border border-green-600">

        {tasks.length === 0 && (
          <p className="text-gray-400">No tasks</p>
        )}

        {tasks.map((mail, i) => (
          <li key={i} className="mb-4">

            <p className="text-green-300 font-semibold">
              • {mail.actions.task_created}
            </p>

            <p className="text-gray-400 text-sm">
              From email: {mail.subject}
            </p>

          </li>
        ))}

      </ul>

    </div>
  );
}
