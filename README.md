# Choncho Dashboard 🦬

A lightweight, real-time project dashboard built for personal project management.

## Features

- **Live project tracking** - Reads from NOW.md markdown file
- **Auto-refresh** - Updates every 30 seconds
- **Progress visualization** - Shows completion status per project
- **Blockers & next actions** - Clear visibility of what's blocking progress
- **Recent activity** - Timeline view of daily work logs

## Quick Start

```bash
# Start the dashboard
cd projects/dashboard
node server.js
```

Visit: `http://localhost:3333`

## How It Works

The dashboard parses `NOW.md` (your current work state) and renders it as a clean, auto-refreshing web interface. No database needed - just markdown files.

### File Structure

- `NOW.md` - Current projects, status, blockers, next actions
- `memory/YYYY-MM-DD.md` - Daily work logs
- `projects/dashboard/server.js` - Lightweight Node.js server

## Future Plans

- Calendar integration
- Task detail modal views
- Time tracking
- GitHub integration
- API for automated task creation

## License

MIT (or choose later)
