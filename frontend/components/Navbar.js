import Link from "next/link";

export default function Navbar() {
  return (
    <div className="flex gap-6 mb-6 text-green-400 font-semibold">

      <Link href="/">Home</Link>
      <Link href="/inbox">Inbox</Link>
      <Link href="/tasks">Tasks</Link>
      <Link href="/summary">Daily Summary</Link>

    </div>
  );
}
