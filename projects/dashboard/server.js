const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = 3333;
const WORKSPACE = path.resolve(__dirname, '../..');

function readFile(relPath) {
  try {
    return fs.readFileSync(path.join(WORKSPACE, relPath), 'utf8');
  } catch { return null; }
}

function parseMarkdownSections(md) {
  const sections = [];
  let current = null;
  for (const line of md.split('\n')) {
    const h2 = line.match(/^## (.+)/);
    const h3 = line.match(/^### (.+)/);
    if (h2) {
      current = { title: h2[1], level: 2, items: [], subsections: [] };
      sections.push(current);
    } else if (h3 && current) {
      const sub = { title: h3[1], level: 3, items: [] };
      current.subsections.push(sub);
    } else if (current) {
      const target = current.subsections.length > 0 ? current.subsections[current.subsections.length - 1] : current;
      if (line.trim()) target.items.push(line);
    }
  }
  return sections;
}

function getMemoryFiles() {
  const memDir = path.join(WORKSPACE, 'memory');
  try {
    return fs.readdirSync(memDir)
      .filter(f => f.match(/^\d{4}-\d{2}-\d{2}\.md$/))
      .sort()
      .reverse()
      .slice(0, 7);
  } catch { return []; }
}

function buildDashboard() {
  const now = readFile('NOW.md') || '# No NOW.md found';
  const sections = parseMarkdownSections(now);
  const memoryFiles = getMemoryFiles();
  
  // Read today's memory
  const today = new Date().toLocaleDateString('en-CA', { timeZone: 'Australia/Brisbane' });
  const todayMemory = readFile(`memory/${today}.md`);

  // Build project cards
  let projectCards = '';
  const activeSection = sections.find(s => s.title === 'Active Projects');
  if (activeSection) {
    for (const sub of activeSection.subsections) {
      const titleMatch = sub.title.match(/\d+\.\s*(.+)/);
      const name = titleMatch ? titleMatch[1] : sub.title;
      const statusLine = sub.items.find(i => i.includes('**Status:**'));
      const status = statusLine ? statusLine.replace(/.*\*\*Status:\*\*\s*/, '').replace(/\*\*/g, '') : 'Unknown';
      
      const done = sub.items.filter(i => i.includes('✅')).length;
      const pending = sub.items.filter(i => i.includes('⏳')).length;
      const warning = sub.items.filter(i => i.includes('⚠️')).length;
      const total = done + pending + warning || 1;
      const pct = Math.round((done / total) * 100);
      
      const statusClass = status.toLowerCase().includes('waiting') || status.toLowerCase().includes('pending') ? 'waiting' :
                          status.toLowerCase().includes('progress') ? 'active' :
                          status.toLowerCase().includes('planning') || status.toLowerCase().includes('early') ? 'planning' : 'active';
      
      let itemsHtml = '';
      for (const item of sub.items) {
        if (item.startsWith('**Status:**')) continue;
        const cleaned = item.replace(/^-\s*/, '').replace(/\*\*/g, '');
        const icon = item.includes('✅') ? '✅' : item.includes('⏳') ? '⏳' : item.includes('⚠️') ? '⚠️' : item.includes('📄') ? '📄' : '•';
        const text = cleaned.replace(/^[✅⏳⚠️📄]\s*/, '');
        itemsHtml += `<div class="task-item"><span class="task-icon">${icon}</span><span>${text}</span></div>`;
      }

      projectCards += `
        <div class="card project-card ${statusClass}">
          <div class="card-header">
            <h3>${name}</h3>
            <span class="status-badge ${statusClass}">${status}</span>
          </div>
          <div class="progress-bar"><div class="progress-fill" style="width:${pct}%"></div></div>
          <div class="progress-label">${done} done · ${pending} pending · ${warning} issues</div>
          <div class="task-list">${itemsHtml}</div>
        </div>`;
    }
  }

  // Blockers
  const blockerSection = sections.find(s => s.title === 'Blockers');
  let blockersHtml = '<div class="card blockers-card"><h3>🚧 Blockers</h3>';
  if (blockerSection && blockerSection.items.length) {
    for (const item of blockerSection.items) {
      if (item.trim().startsWith('-')) {
        blockersHtml += `<div class="blocker-item">${item.replace(/^-\s*/, '').replace(/\*\*/g, '<strong>').replace(/\*\*/g, '</strong>')}</div>`;
      }
    }
  } else {
    blockersHtml += '<div class="blocker-item clear">No blockers 🎉</div>';
  }
  blockersHtml += '</div>';

  // Next actions
  const nextSection = sections.find(s => s.title === 'Next Actions');
  let nextHtml = '<div class="card next-card"><h3>📋 Next Actions</h3>';
  if (nextSection) {
    for (const item of nextSection.items) {
      if (item.trim().match(/^\d+\./)) {
        nextHtml += `<div class="next-item">${item.replace(/^\d+\.\s*/, '').replace(/\*\*/g, '')}</div>`;
      }
    }
  }
  nextHtml += '</div>';

  // Recent activity
  let activityHtml = '<div class="card activity-card"><h3>📅 Recent Activity</h3>';
  for (const f of memoryFiles.slice(0, 5)) {
    const date = f.replace('.md', '');
    const content = readFile(`memory/${f}`);
    const preview = content ? content.split('\n').filter(l => l.startsWith('- ')).slice(0, 3).map(l => l.replace(/^-\s*/, '').substring(0, 80)).join(' · ') : '';
    activityHtml += `<div class="activity-item"><span class="activity-date">${date}</span><span class="activity-preview">${preview || 'No entries'}</span></div>`;
  }
  activityHtml += '</div>';

  const lastUpdated = now.match(/\*Last updated: (.+)\*/)?.[1] || 'Unknown';

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
  
  .activity-card { border-left: 3px solid #8b949e; }
  .activity-item { 
    display: flex; gap: 12px; padding: 8px 0; font-size: 13px;
    border-bottom: 1px solid #21262d;
  }
  .activity-item:last-child { border-bottom: none; }
  .activity-date { color: #58a6ff; font-family: monospace; white-space: nowrap; flex-shrink: 0; }
  .activity-preview { color: #8b949e; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  
  .bottom-row { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  @media (max-width: 900px) { .bottom-row { grid-template-columns: 1fr; } }
</style>
</head>
<body>
  <header>
    <h1><span>🦬</span> Choncho Dashboard</h1>
    <div class="meta">Last updated: ${lastUpdated} · Auto-refreshes every 30s</div>
  </header>
  
  <div class="grid">${projectCards}</div>
  
  <div class="grid-3">
    ${blockersHtml}
    ${nextHtml}
    ${activityHtml}
  </div>
</body>
</html>`;
}

const server = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/index.html') {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(buildDashboard());
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
});
