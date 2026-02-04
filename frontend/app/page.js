"use client";

import Navbar from "../components/Navbar";
import { useEmails } from "../context/EmailContext";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function Home() {

  const { emails, loading, user } = useEmails();
  const router = useRouter();

  if (!user && typeof window !== "undefined") {
    router.replace("/login");
    return null;
  }


  if (loading) {
    return <p className="text-green-400 p-6">Loading...</p>;
  }

  const countByCategory = (cat) =>
    emails.filter(e => e.category === cat).length;

  return (
    <div className="min-h-screen bg-black text-green-400 p-6">

      <Navbar />

      <h1 className="text-3xl font-bold mb-6">Dashboard</h1>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">

        <Link href="/inbox?category=urgent">
          <div className="bg-gray-900 p-6 rounded-xl border border-red-600 cursor-pointer">
            Urgent: {countByCategory("urgent")}
          </div>
        </Link>

        <Link href="/inbox?category=normal">
          <div className="bg-gray-900 p-6 rounded-xl border border-green-600 cursor-pointer">
            Normal: {countByCategory("normal")}
          </div>
        </Link>

        <Link href="/inbox?category=spam">
          <div className="bg-gray-900 p-6 rounded-xl border border-gray-600 cursor-pointer">
            Spam: {countByCategory("spam")}
          </div>
        </Link>

        <Link href="/inbox?category=job">
          <div className="bg-gray-900 p-6 rounded-xl border border-yellow-500 cursor-pointer hover:bg-gray-800 transition">
            Jobs: {countByCategory("job")}
          </div>
        </Link>


        <div className="bg-gray-900 p-6 rounded-xl border border-green-600">
          Total: {emails.length}
        </div>

      </div>

    </div>
  );
}
