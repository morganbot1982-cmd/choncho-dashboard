# 🦬 Agent Wrapper

A web UI for orchestrating agentic coding tools - chat with Claude, spawn coding agents, track projects.

## What This Is

**Phase 1 (Week 1):** Basic chat interface with Claude
- Clean web UI for conversational coding help
- Context-aware file uploads
- Session persistence
- Syntax highlighting

**Coming Soon:**
- Week 2: Spawn Codex/Claude Code agents from the UI
- Week 3: Multi-project management + Git integration
- Week 4: Cost tracking, Docker deployment

## Quick Start

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure API Key

```bash
# Copy the example env file
cp .env.local.example .env.local

# Edit .env.local and add your Anthropic API key
# Get one from: https://console.anthropic.com/
```

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Current Features (v0.1)

✅ **Chat Interface**
- Clean, responsive UI
- Real-time message streaming
- Keyboard shortcuts (Enter to send, Shift+Enter for newline)
- Loading states

✅ **Claude Integration**
- Using Claude Sonnet 4.5 (latest)
- Context-aware responses
- Error handling

## Tech Stack

- **Frontend:** Next.js 16 (App Router), React 19, TypeScript, Tailwind CSS
- **Backend:** Next.js API Routes
- **AI:** Anthropic Claude API
- **Deployment:** Ready for Docker/Railway/Vercel

## Project Structure

```
agent-wrapper/
├── app/
│   ├── api/
│   │   └── chat/
│   │       └── route.ts          # Claude API integration
│   ├── globals.css               # Global styles
│   ├── layout.tsx                # Root layout
│   └── page.tsx                  # Main chat interface
├── .env.local                    # API keys (not committed)
├── .env.local.example            # Template for env vars
├── next.config.ts                # Next.js config
├── tailwind.config.ts            # Tailwind config
├── tsconfig.json                 # TypeScript config
└── package.json                  # Dependencies
```

## Development Roadmap

### Week 1: Core Chat ✅
- [x] Basic Next.js setup
- [x] Chat UI with message history
- [x] Claude API integration
- [ ] File upload for code context
- [ ] Syntax highlighting
- [ ] Session persistence (SQLite)

### Week 2: Agent Spawning
- [ ] Terminal component (xterm.js)
- [ ] Spawn Claude Code in background
- [ ] Stream agent output to UI
- [ ] Job queue for tracking agents

### Week 3: Multi-Project
- [ ] Project switcher
- [ ] File tree viewer
- [ ] Git integration (status, diff, commit)
- [ ] Better context management

### Week 4: Polish
- [ ] Token/cost tracking
- [ ] Split view with resizable panels
- [ ] Docker deployment
- [ ] Basic auth

## Why This Exists

**Problem:** Existing agentic coding tools (Cursor, Windsurf, etc.) are:
- Expensive
- Closed-source
- Limited customization
- Poor orchestration for complex multi-agent workflows

**Solution:** Build our own wrapper that:
- Uses our own API keys (cheaper)
- Open architecture (can swap agents)
- Better multi-project management
- Learn by building

## Contributing

This is a personal project (for now). If it gets good, might open source the core.

## License

MIT (when we decide to share it)

---

**Built with 🦬 by Morgan + Choncho**
