"use client"

import Link from "next/link";
import Navbar from "../components/Navbar";
import { useEmails } from "../context/EmailContext";

export default function Home() {

  const { emails, loading } = useEmails();

  if (loading) {
    return <p className="text-green-400 p-6">Loading...</p>;
  }

  const countByCategory = (cat) =>
    emails.filter(e => e.category === cat).length;

  return (
    <div className="min-h-screen bg-black text-green-400 p-6">

      <h1 className="text-3xl font-bold mb-6">MailSense AI</h1>

      <Navbar />

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

        <Link href="/inbox?category=urgent">
          <div className="bg-gray-900 p-6 rounded-xl border border-red-600 cursor-pointer">
            <p className="text-red-400">Urgent</p>
            <p className="text-3xl">{countByCategory("urgent")}</p>
          </div>
        </Link>

        <Link href="/inbox?category=normal">
          <div className="bg-gray-900 p-6 rounded-xl border border-green-600 cursor-pointer">
            <p>Normal</p>
            <p className="text-3xl">{countByCategory("normal")}</p>
          </div>
        </Link>

        <Link href="/inbox?category=spam">
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-600 cursor-pointer">
            <p className="text-gray-400">Spam</p>
            <p className="text-3xl">{countByCategory("spam")}</p>
          </div>
        </Link>

        <div className="bg-gray-900 p-6 rounded-xl border border-green-600">
          <p>Total</p>
          <p className="text-3xl">{emails.length}</p>
        </div>

      </div>

    </div>
  );
}
