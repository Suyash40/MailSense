export default function TaskList({ emails }) {

  const tasks = emails
    .filter(e => e.actions.task_created)
    .map(e => e.actions.task_created);

  return (
    <div className="bg-gray-900 border border-green-600 rounded-xl p-4">
      <h2 className="text-xl font-bold mb-2 text-green-400">
        📋 Tasks
      </h2>

      {tasks.length === 0 && (
        <p className="text-gray-400">No tasks</p>
      )}

      <ul className="list-disc ml-5 text-gray-200">
        {tasks.map((task, idx) => (
          <li key={idx} className="mb-1">
            {task}
          </li>
        ))}
      </ul>
    </div>
  );
}
