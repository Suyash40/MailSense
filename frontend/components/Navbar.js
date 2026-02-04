import Link from "next/link";
import { useEmails } from "../context/EmailContext";

export default function Navbar() {

  const { logout } = useEmails();

  return (
    <div className="flex justify-between items-center mb-6">

      <div className="flex gap-6 text-green-400 font-semibold">
        <Link href="/">Home</Link>
        <Link href="/inbox">Inbox</Link>
        <Link href="/tasks">Tasks</Link>
        <Link href="/summary">Daily Summary</Link>
      </div>

      <button
        onClick={logout}
        className="bg-red-600 px-4 py-1 rounded text-black font-semibold"
      >
        Sign Out
      </button>

    </div>
  );
}
