"use client";

import { useState } from "react";
import { useSearchParams } from "next/navigation";
import Navbar from "../../components/Navbar";
import { useEmails } from "../../context/EmailContext";

export default function Inbox() {

  const { emails, loading } = useEmails();
  const [selected, setSelected] = useState(null);
  const searchParams = useSearchParams();
  const categoryFilter = searchParams.get("category");
  const filteredEmails = categoryFilter
    ? emails.filter(e => e.category === categoryFilter)
    : emails;



  if (loading) {
    return <p className="text-green-400 p-6">Loading emails...</p>;
  }


  return (
    <div className="min-h-screen bg-black text-green-400 p-6">

      <Navbar />

      <h1 className="text-2xl font-bold mb-4">Inbox</h1>

      <div className="flex gap-6">

        {/* Email list */}
        <div className="w-1/3 bg-gray-900 p-4 rounded-xl border border-green-600">

          {filteredEmails.map((mail, i) => (
            <div
              key={i}
              onClick={() => setSelected(mail)}
              className="cursor-pointer py-2 border-b border-gray-700 hover:text-green-300"
            >
              • {mail.subject}
            </div>
          ))}


        </div>

        {/* Full email view */}
        <div className="flex-1 bg-gray-900 p-4 rounded-xl border border-green-600">

          {!selected && (
            <p className="text-gray-400">Click an email to open</p>
          )}

          {selected && (
            <>
              <h2 className="text-xl mb-2">{selected.subject}</h2>
              <p className="text-gray-400 mb-2">{selected.from}</p>
              <p className="text-gray-200 whitespace-pre-wrap">
                {selected.body}
              </p>
            </>
          )}

        </div>

      </div>

    </div>
  );
}
