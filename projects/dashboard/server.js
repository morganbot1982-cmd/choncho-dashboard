const http = require('http');
const https = require('https');

const PORT = 3333;
const LEANTIME_API = 'http://localhost:8080/api/jsonrpc';
const LEANTIME_KEY = 'W2bKPo0rWZnVHKHiuq2Lhk6zp6CJnkWN'; // From leantime setup

let apiCallId = 1;

function leantimeRPC(method, params = {}) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      jsonrpc: '2.0',
      method,
      params,
      id: apiCallId++
    });

    const url = new URL(LEANTIME_API);
    const options = {
      hostname: url.hostname,
      port: url.port,
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': LEANTIME_KEY,
        'Content-Length': Buffer.byteLength(payload)
      }
    };

    const req = http.request(options, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          if (parsed.error) reject(new Error(parsed.error.message || 'API error'));
          else resolve(parsed.result);
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

async function fetchDashboardData() {
  try {
    // Fetch all projects
    const projectsResult = await leantimeRPC('leantime.rpc.Projects.Projects.getAll', {
      userId: 1,
      clientId: 1
    });
    
    const projects = projectsResult?.data || [];
    
    // Fetch all tasks
    const tasksResult = await leantimeRPC('leantime.rpc.Tickets.Tickets.getAll', {
      userId: 1,
      projectId: null // Get all tasks across projects
    });
    
    const allTasks = tasksResult?.data || [];
    
    // Group tasks by project
    const tasksByProject = {};
    for (const task of allTasks) {
      const pid = task.projectId || task.project;
      if (!tasksByProject[pid]) tasksByProject[pid] = [];
      tasksByProject[pid].push(task);
    }
    
    return { projects, tasksByProject, allTasks };
  } catch (error) {
    console.error('Leantime API error:', error.message);
    return { projects: [], tasksByProject: {}, allTasks: [], error: error.message };
  }
}

function getPriorityLabel(priority) {
  const map = { 1: 'Low', 2: 'Medium', 3: 'High', 4: 'Critical' };
  return map[priority] || 'Unknown';
}

function getStatusLabel(status) {
  const map = { 3: 'Open', 4: 'In Progress', 5: 'Done', 6: 'Blocked' };
  return map[status] || 'Unknown';
}

function getStatusClass(status) {
  if (status === 5) return 'active'; // Done
  if (status === 6) return 'waiting'; // Blocked
  if (status === 4) return 'active'; // In Progress
  return 'planning'; // Open
}

async function buildDashboard() {
  const { projects, tasksByProject, allTasks, error } = await fetchDashboardData();
  
  if (error) {
    return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Choncho Dashboard</title>
<meta http-equiv="refresh" content="30">
<style>
  body { font-family: sans-serif; padding: 40px; background: #0d1117; color: #e6edf3; }
  .error { background: #f85149; color: white; padding: 20px; border-radius: 8px; }
</style>
</head>
<body>
  <div class="error">
    <h2>⚠️ Leantime API Error</h2>
    <p>${error}</p>
    <p>Make sure Leantime is running at http://localhost:8080</p>
  </div>
</body>
</html>`;
  }

  // Build project cards
  let projectCards = '';
  
  for (const project of projects) {
    const tasks = tasksByProject[project.id] || [];
    const done = tasks.filter(t => t.status === 5).length;
    const open = tasks.filter(t => t.status === 3).length;
    const inProgress = tasks.filter(t => t.status === 4).length;
    const blocked = tasks.filter(t => t.status === 6).length;
    const total = tasks.length || 1;
    const pct = Math.round((done / total) * 100);
    
    const statusClass = blocked > 0 ? 'waiting' : inProgress > 0 ? 'active' : 'planning';
    const statusLabel = blocked > 0 ? 'Blocked' : inProgress > 0 ? 'In Progress' : open > 0 ? 'Open' : 'Done';
    
    let tasksHtml = '';
    const activeTasks = tasks.filter(t => t.status !== 5).slice(0, 8); // Show up to 8 active tasks
    
    for (const task of activeTasks) {
      const icon = task.status === 5 ? '✅' : 
                   task.status === 6 ? '🚧' : 
                   task.status === 4 ? '⏳' : '📋';
      const priorityBadge = task.priority >= 3 ? `<span style="color: #f85149; font-weight: bold;">[${getPriorityLabel(task.priority)}]</span>` : '';
      tasksHtml += `<div class="task-item"><span class="task-icon">${icon}</span><span>${task.headline} ${priorityBadge}</span></div>`;
    }
    
    if (tasks.length > activeTasks.length) {
      tasksHtml += `<div class="task-item"><span class="task-icon">•</span><span style="color: #8b949e;">...and ${tasks.length - activeTasks.length} more</span></div>`;
    }
    
    projectCards += `
      <div class="card project-card ${statusClass}">
        <div class="card-header">
          <h3>${project.name}</h3>
          <span class="status-badge ${statusClass}">${statusLabel}</span>
        </div>
        <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
        <div class="progress-label">${done} done · ${inProgress} in progress · ${open} open · ${blocked} blocked</div>
        <div class="task-list">${tasksHtml || '<div class="task-item" style="color: #8b949e;">No tasks yet</div>'}</div>
      </div>`;
  }
  
  // Blockers (tasks with status = blocked OR high priority open tasks)
  const blockers = allTasks.filter(t => t.status === 6 || (t.priority >= 3 && t.status !== 5));
  let blockersHtml = '<div class="card blockers-card"><h3>🚧 Blockers & Urgent</h3>';
  if (blockers.length > 0) {
    for (const task of blockers.slice(0, 10)) {
      const projectName = projects.find(p => p.id === task.projectId)?.name || 'Unknown';
      const priorityLabel = getPriorityLabel(task.priority);
      blockersHtml += `<div class="blocker-item"><strong>${projectName}:</strong> ${task.headline} <span style="color: #d29922;">[${priorityLabel}]</span></div>`;
    }
  } else {
    blockersHtml += '<div class="blocker-item clear">No blockers 🎉</div>';
  }
  blockersHtml += '</div>';
  
  // Next actions (high priority open tasks, sorted by priority)
  const nextActions = allTasks
    .filter(t => t.priority >= 3 && t.status !== 5 && t.status !== 6)
    .sort((a, b) => b.priority - a.priority)
    .slice(0, 10);
  
  let nextHtml = '<div class="card next-card"><h3>📋 Next Actions</h3>';
  if (nextActions.length > 0) {
    for (const task of nextActions) {
      const projectName = projects.find(p => p.id === task.projectId)?.name || 'Unknown';
      const priorityLabel = getPriorityLabel(task.priority);
      nextHtml += `<div class="next-item">${task.headline} <span style="color: #8b949e; font-size: 11px;">(${projectName} · ${priorityLabel})</span></div>`;
    }
  } else {
    nextHtml += '<div class="next-item">All clear! 🎉</div>';
  }
  nextHtml += '</div>';
  
  // Stats
  const totalTasks = allTasks.length;
  const doneTasks = allTasks.filter(t => t.status === 5).length;
  const openTasks = allTasks.filter(t => t.status === 3).length;
  const inProgressTasks = allTasks.filter(t => t.status === 4).length;
  const blockedTasks = allTasks.filter(t => t.status === 6).length;
  
  let statsHtml = '<div class="card stats-card"><h3>📊 Overview</h3>';
  statsHtml += `<div class="stats-grid">`;
  statsHtml += `<div class="stat-item"><div class="stat-label">Projects</div><div class="stat-value">${projects.length}</div></div>`;
  statsHtml += `<div class="stat-item"><div class="stat-label">Total Tasks</div><div class="stat-value">${totalTasks}</div></div>`;
  statsHtml += `<div class="stat-item"><div class="stat-label">Done</div><div class="stat-value" style="color: #3fb950;">${doneTasks}</div></div>`;
  statsHtml += `<div class="stat-item"><div class="stat-label">In Progress</div><div class="stat-value" style="color: #58a6ff;">${inProgressTasks}</div></div>`;
  statsHtml += `<div class="stat-item"><div class="stat-label">Open</div><div class="stat-value">${openTasks}</div></div>`;
  statsHtml += `<div class="stat-item"><div class="stat-label">Blocked</div><div class="stat-value" style="color: #f85149;">${blockedTasks}</div></div>`;
  statsHtml += `</div></div>`;

  const now = new Date().toLocaleString('en-AU', { timeZone: 'Australia/Brisbane' });

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Choncho Dashboard</title>
<meta http-equiv="refresh" content="30">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { 
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: #0d1117; color: #e6edf3; padding: 24px;
    max-width: 1400px; margin: 0 auto;
  }
  header { 
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 32px; padding-bottom: 16px; border-bottom: 1px solid #21262d;
  }
  header h1 { font-size: 24px; font-weight: 600; }
  header h1 span { margin-right: 8px; }
  .meta { color: #8b949e; font-size: 13px; }
  
  .grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px; }
  .grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; margin-bottom: 20px; }
  @media (max-width: 900px) { .grid, .grid-3 { grid-template-columns: 1fr; } }
  
  .card {
    background: #161b22; border: 1px solid #21262d; border-radius: 12px;
    padding: 20px; transition: border-color 0.2s;
  }
  .card:hover { border-color: #388bfd44; }
  .card h3 { font-size: 16px; font-weight: 600; margin-bottom: 12px; }
  
  .project-card { border-left: 3px solid #388bfd; }
  .project-card.waiting { border-left-color: #d29922; }
  .project-card.planning { border-left-color: #8b949e; }
  .project-card.active { border-left-color: #388bfd; }
  
  .card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px; }
  .card-header h3 { margin-bottom: 0; }
  
  .status-badge {
    font-size: 11px; padding: 3px 10px; border-radius: 20px; font-weight: 500;
    white-space: nowrap;
  }
  .status-badge.active { background: #388bfd22; color: #58a6ff; }
  .status-badge.waiting { background: #d2992222; color: #d29922; }
  .status-badge.planning { background: #8b949e22; color: #8b949e; }
  
  .progress-bar { 
    height: 4px; background: #21262d; border-radius: 2px; margin-bottom: 6px;
    overflow: hidden;
  }
  .progress-fill { height: 100%; background: #388bfd; border-radius: 2px; transition: width 0.3s; }
  .progress-label { font-size: 12px; color: #8b949e; margin-bottom: 12px; }
  
  .task-list { display: flex; flex-direction: column; gap: 6px; }
  .task-item { 
    display: flex; gap: 8px; font-size: 13px; color: #c9d1d9;
    padding: 4px 0; line-height: 1.4;
  }
  .task-icon { flex-shrink: 0; width: 18px; text-align: center; }
  
  .blockers-card { border-left: 3px solid #f85149; }
  .blocker-item { font-size: 13px; padding: 6px 0; color: #f0883e; }
  .blocker-item.clear { color: #3fb950; }
  
  .next-card { border-left: 3px solid #3fb950; }
  .next-item { 
    font-size: 13px; padding: 8px 12px; margin-bottom: 6px;
    background: #3fb95011; border-radius: 6px; color: #c9d1d9;
    counter-increment: next-counter;
  }
  .next-item::before {
    content: counter(next-counter) ". ";
    color: #3fb950; font-weight: 600;
  }
  .next-card { counter-reset: next-counter; }
  
  .stats-card { border-left: 3px solid #8b949e; }
  .stats-grid { 
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px;
  }
  .stat-item { text-align: center; }
  .stat-label { font-size: 11px; color: #8b949e; margin-bottom: 4px; text-transform: uppercase; }
  .stat-value { font-size: 24px; font-weight: 700; color: #e6edf3; }
  
  .leantime-badge {
    display: inline-block;
    background: #3fb95011;
    color: #3fb950;
    font-size: 11px;
    padding: 4px 8px;
    border-radius: 4px;
    margin-left: 8px;
  }
</style>
</head>
<body>
  <header>
    <h1><span>🦬</span> Choncho Dashboard <span class="leantime-badge">● Leantime Live</span></h1>
    <div class="meta">Last updated: ${now} · Auto-refreshes every 30s</div>
  </header>
  
  <div class="grid">${projectCards}</div>
  
  <div class="grid-3">
    ${blockersHtml}
    ${nextHtml}
    ${statsHtml}
  </div>
</body>
</html>`;
}

const server = http.createServer(async (req, res) => {
  if (req.url === '/' || req.url === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    const html = await buildDashboard();
    res.end(html);
  } else if (req.url === '/api/refresh') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', time: new Date().toISOString() }));
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

server.listen(PORT, '127.0.0.1', () => {
  console.log(`🦬 Dashboard running at http://localhost:${PORT}`);
  console.log(`📊 Pulling live data from Leantime API`);
});
