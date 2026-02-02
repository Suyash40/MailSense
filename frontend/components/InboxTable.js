export default function InboxTable({ emails }) {
  return (
    <div className="bg-gray-900 rounded-xl border border-green-600 p-4">

      <h2 className="text-2xl font-bold mb-3 text-green-400">
        📥 Inbox
      </h2>

      <table className="w-full text-left text-gray-200">

        <thead>
          <tr className="border-b border-gray-700 text-green-300">
            <th className="pb-2">Subject</th>
            <th className="pb-2">From</th>
            <th className="pb-2">Category</th>
          </tr>
        </thead>

        <tbody>
          {emails.map((mail, idx) => (
            <tr key={idx} className="border-b border-gray-800 hover:bg-gray-800 transition">

              <td className="py-2">
                {mail.subject}
              </td>

              <td className="text-gray-400">
                {mail.from}
              </td>

              <td>
                <span className={`px-3 py-1 rounded-full text-sm font-semibold text-black
                  ${
                    mail.category === "urgent"
                      ? "bg-red-500"
                      : mail.category === "spam"
                      ? "bg-gray-400"
                      : "bg-green-400"
                  }
                `}>
                  {mail.category}
                </span>
              </td>

            </tr>
          ))}
        </tbody>

      </table>
    </div>
  );
}
