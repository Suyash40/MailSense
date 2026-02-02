export default function Alerts({ emails }) {

  const urgent = emails.filter(e => e.actions.alert);

  return (
    <div className="bg-gray-900 border border-red-600 rounded-xl p-4">
      <h2 className="text-xl font-bold mb-2 text-red-400">
        🚨 Urgent Alerts
      </h2>

      {urgent.length === 0 && (
        <p className="text-gray-400">No urgent alerts</p>
      )}

      <ul className="text-gray-200">
        {urgent.map((mail, idx) => (
          <li key={idx} className="mb-1">
            • {mail.subject}
          </li>
        ))}
      </ul>
    </div>
  );
}
