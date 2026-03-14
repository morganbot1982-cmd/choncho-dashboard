-- Bulk import Morgan's real projects into Leantime
-- Delete existing fake projects (IDs 14-21)
DELETE FROM zp_projects WHERE id >= 14;

-- Insert real projects
INSERT INTO zp_projects (id, name, details, clientId, type, state) VALUES
(14, 'Wise/Xero Bank Reconciliation', 
 'Major accounting project (Feb 2026) - reconciled 2,113 Wise transactions spanning Nov 2020 to Feb 2026. Coded all transactions to Xero account codes, cleaned up owner funds introduced, reclassified revenue streams, and prepared final import CSV.\n\nKey work: Coded 2,070 transactions, split revenue ($24.6K business sales, $10.4K photography, $5.7K consulting), reclassified $156K owner funds, tagged personal income for tax, created merchant coding rules, analyzed duplicates (674 transactions flagged).\n\nNext: Import to Xero, delete duplicates, complete reconciliation.', 
 1, 'project', 0),

(15, 'Health & Fitness Agent', 
 'Personal health tracking system - AI sub-agent for food/calorie logging, personal spending tracker, and daily movement habit building. Focus on awareness and gentle accountability.\n\nFeatures: Food tracking via photo analysis (WhatsApp/Telegram), personal spending tracker, movement reminders (pushups, water, walks), gentle accountability (streaks, no shame).\n\nStatus: GP health check complete (Feb 26), 3 specialist referrals issued (cardiology booked, gastro + ENT pending), blood work pending.\n\nNext phases: Baseline metrics, food tracking MVP, spending tracker, movement reminders, dashboard integration.', 
 1, 'project', 0),

(16, 'Ecommerce JV', 
 'Joint venture with partner (old colleague, ex-sales manager) - automated ecommerce business importing accessories from China via existing supplier network.\n\nSetup: Shopify + 3PL fulfillment, fully automated backend, $20K AUD budget. Accessories first (no sizing complexity).\n\nExperience: 15 years AU clothing/distribution, warehousing → sales → design/photography → production management → own brand → current handmade headwear.\n\nNext: Partnership agreement, first product selection, Shopify setup, automation stack.', 
 1, 'project', 0),

(17, 'Task Copilot', 
 'Voice-first AI task assistant that knows full business context and keeps Morgan on track across all work (digital and physical). Accessible by voice or text from anywhere, including away from computer.\n\nCore principles: Push not pull (agent reaches out), voice-first (talk like a colleague), context-aware (knows business structure), one thing at a time (ADHD-friendly), capture everything (instant voice/text input).\n\nPhases: Morning briefings + nudges (NOW) → Dedicated sub-agent → Voice interface → Smart scheduling.\n\nStatus: Planning/design phase, full brief complete.', 
 1, 'project', 0),

(18, 'Dashboard', 
 'Local project dashboard running at http://localhost:3333. Reads from NOW.md, auto-refreshes every 30s.\n\nShows: Project cards, progress, blockers, next actions, recent activity.\n\nPhase 1 complete. Future: Health metrics integration, task copilot integration, real-time updates.', 
 1, 'project', 0),

(19, 'OpenClaw Installation Guide', 
 'Comprehensive installation and setup guide for OpenClaw - deployed to Netlify (https://symphonious-jelly-e98e67.netlify.app).\n\nGitHub: https://github.com/morganbot1982-cmd/openclaw-installation-guide\nAuto-deploys on push to main.\n\nStatus: Live and complete.', 
 1, 'project', 0),

(20, 'Headwear Samples', 
 'Workshop production work - handmade headwear brand with in-house sample workshop. Physical/workshop tasks away from computer.\n\nCurrent focus: Sample production, materials sourcing, production workflow optimization.', 
 1, 'project', 0),

(21, 'Voice Assistant', 
 'Voice interface development - hands-free task capture and updates for workshop/physical work.\n\nIntegration possibilities: Telegram voice messages (transcription → task), WhatsApp voice notes, custom voice interface (web or native), Apple Shortcuts for Siri-like trigger.\n\nStatus: Early exploration phase.', 
 1, 'project', 0),

(22, 'Icon Press', 
 'Project work (details TBD).', 
 1, 'project', 0);

-- Assign all projects to Morgan (user ID 1)
INSERT INTO zp_relationuserproject (userId, projectId, projectRole) VALUES
(1, 14, 'owner'),
(1, 15, 'owner'),
(1, 16, 'owner'),
(1, 17, 'owner'),
(1, 18, 'owner'),
(1, 19, 'owner'),
(1, 20, 'owner'),
(1, 21, 'owner'),
(1, 22, 'owner')
ON DUPLICATE KEY UPDATE userId=userId;
