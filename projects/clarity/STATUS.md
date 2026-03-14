# Clarity - Project Status

**Last Updated:** March 14, 2026  
**Status:** ✅ Full Basic Tier Complete + Pro Tier Built + Dream Month Pro Mode Added

## What Clarity Is
Real-time daily P&L dashboard for e-commerce stores. Track revenue, costs, ad spend, and profit margins with adjustable cost drivers that recalculate historical data instantly.

## Session Summary: March 14, 2026

### Dream Month Pro Mode Built ✅

**New feature:** Pro Mode toggle on Dream Month page

**What was built:**
- Added Pro/Basic mode toggle switch to Dream Month
- Pro mode shows all comprehensive inputs:
  - Revenue Ex GST (not just calculated from AOV × Orders)
  - Items Sold, Store Sessions (for conversion metrics)
  - Facebook/Google/TikTok ad spend breakdown
  - Salaries, Subscriptions, Office Expenses
- Pro mode uses full comprehensive calculations:
  - Conversion Rate, Items Per Order, Revenue Per Visit
  - Cost Per Visit, Cost Per Acquisition
  - VCR, FCR, MER with detailed breakdowns
  - All metrics from comprehensive view
- Basic mode maintains simple functionality (CPA, ad spend, AOV, orders)
- Blue-shaded inputs in Pro mode match spreadsheet structure
- Seamless toggle between modes preserves user experience

**Technical implementation:**
- Imported `calculateComprehensive` from `comprehensiveCalculations.ts`
- Added `ComprehensiveInput` interface for Pro mode state
- Conditional rendering based on `proMode` state
- Maintains backward compatibility with existing basic functionality

**Files modified:**
- `app/dream/page.tsx` - Added Pro mode toggle and comprehensive calculations

**Validation:**
- Pro mode shows all comprehensive metrics correctly
- Basic mode unchanged (CPA, ad spend, AOV, orders)
- Toggle switch works smoothly
- Default values set for realistic scenario modeling
- Help text updates based on active mode

**Commit:**
- SHA: aeac7c7
- Message: "Add Pro Mode toggle to Dream Month page with full comprehensive calculations"

---

## Session Summary: March 12, 2026

### Annual Planning Dashboard Built ✅

**New feature:** Full year planning and variance tracking

**What was built:**
- New database table: `MonthlyForecast` (stores monthly revenue targets)
- New page: `/annual` - Annual Planning Dashboard
- API route: `/api/forecast` (GET/POST for forecast CRUD)
- Navigation: Added "Annual" buttons to TODAY, MONTHLY, and DRIVERS pages

**Features:**
- 12-month table view (Forecast, Actual, Variance $, Variance %)
- Click-to-edit forecasts (Enter to save, Escape to cancel)
- Auto-calculates actual revenue from daily data
- Color-coded variance (green = beat target, red = missed)
- Year navigation (◄ ► arrows)
- TOTAL row with yearly summaries

**Technical fixes:**
- Fixed Prisma client import (used shared instance from `@/lib/prisma`)
- Ran `npx prisma generate` after schema change
- All calculations working correctly with real 2023 data

**Validation:**
- Tested with 2023 Parca® data ($60,260 total)
- Set $10,000 forecast for April → -$846.91 variance (-8.5%) ✅
- Edit functionality confirmed working

**Files created/modified:**
- `prisma/schema.prisma` - Added MonthlyForecast model
- `app/annual/page.tsx` - Annual planning page (new)
- `app/api/forecast/route.ts` - Forecast API (new)
- `app/page.tsx` - Added Annual button
- `app/monthly/page.tsx` - Added Annual button
- `app/drivers/page.tsx` - Added Annual button

---

## Session Summary: March 11, 2026

### Major Progress Today

✅ **Fixed critical profit calculation bug**
- Problem: Variable costs were multiplying total revenue by orders (costs 40x too high)
- Solution: Calculate avg revenue per order first, then multiply
- File: `/Users/userclaw/.openclaw/workspace/projects/clarity/app/lib/calculations.ts`
- Result: Margins now accurate (39.5% instead of -1286%)

✅ **Imported real Parca® 2023 data**
- 156 days of Morgan's actual e-commerce business
- March - October 2023
- $60,260 revenue | 455 orders | $9,286 ad spend | $132 AOV
- Files:
  - `/tmp/parca-2023.xlsx` (source data)
  - `/Users/userclaw/.openclaw/workspace/projects/clarity/app/scripts/parca-2023-data.ts` (parsed)
  - `/Users/userclaw/.openclaw/workspace/projects/clarity/app/prisma/import-all-parca.ts` (importer)

✅ **Updated Drivers to match Parca costs**
- Product Cost: 35%
- Shipping: $12
- Packaging: $1
- Pick/Pack: $0
- Merchant Fee: 2%
- Transaction Fee: $0.45

### Real Data Breakdown (by month)
- **Mar '23:** 24 days | $8,684 revenue | 64 orders
- **Apr '23:** 26 days | $9,423 revenue | 64 orders  
- **May '23:** 28 days | $11,161 revenue | 74 orders ⭐ (best month)
- **Jun '23:** 23 days | $8,106 revenue | 51 orders
- **Jul '23:** 13 days | $6,103 revenue | 43 orders
- **Aug '23:** 12 days | $6,523 revenue | 52 orders
- **Sep '23:** 27 days | $9,470 revenue | 99 orders
- **Oct '23:** 3 days | $790 revenue | 8 orders

## Current State

**Running locally:**
- Dev server: `npm run dev` in `/Users/userclaw/.openclaw/workspace/projects/clarity/app`
- URL: http://localhost:3000
- Database: SQLite (`dev.db`) with 156 days of real data

**All 4 screens working:**
- TODAY dashboard (daily P&L snapshot)
- MONTHLY calendar view (color-coded profit days)
- ANNUAL planning (forecast vs actual with variance tracking) ⭐ NEW
- DRIVERS editor (adjust costs → history recalculates)

**To view real data:**
- App defaults to "today" (March 2026, no data)
- Click left arrow (◄) ~36 times to reach March 2023
- OR manually navigate to months with data (Mar-Oct 2023)

## Next Feature: Dream Month (Scenario Modeling)

**Concept discussed:** "What if I optimize X cost driver?"

**Potential features:**
1. **Goal Setting** - Set dream targets, show actual vs dream
2. **Scenario Modeling** ⭐ - Create "Dream Drivers" profile, test cost changes
3. **Gap Analysis** - Show what's needed to hit goals
4. **Reverse Engineering** - Input desired profit → calculate requirements

**Morgan's interest:** Scenario modeling (#2) - being able to test "what if?" scenarios before making business decisions.

**Next steps (when resuming):**
1. ✅ ~~Annual Planning Dashboard~~ - COMPLETE (Mar 12, 2026)
2. Build Dream Month scenario modeling
   - Add "Dream" profile alongside current drivers
   - Show side-by-side comparison on monthly view
   - "What if" calculator showing profit impact
3. Add "Jump to First Month" button (skip manual navigation to Mar 2023)
4. Consider deploying to Vercel for live testing

## Tech Stack (Final)
- Framework: Next.js 14 (App Router)
- Database: SQLite (Prisma ORM) - *migrate to PostgreSQL for production*
- Styling: Tailwind CSS
- UI Components: Shadcn/ui
- Language: TypeScript
- Deployment: Ready for Vercel

## Key Files
- **App code:** `/Users/userclaw/.openclaw/workspace/projects/clarity/app/`
- **Calculations:** `/app/lib/calculations.ts` (FIXED - critical bug resolved)
- **Data import:** `/app/scripts/parse-parca-excel.js` + `/app/prisma/import-all-parca.ts`
- **Real data:** `/app/scripts/parca-2023-data.ts` (156 days)
- **Database:** `/app/dev.db` (SQLite with real Parca data)

## Documentation
- `README.md` - Complete setup guide
- `DEPLOYMENT.md` - Vercel deployment instructions
- `QUICKSTART.md` - Quick start guide

## Blockers
None - ready to continue with Dream Month feature

## Session Continuity Notes

**For next session:**
- Read this STATUS.md file first
- App is running at `http://localhost:3000`
- Database: `./dev.db` (SQLite)
- Start dev server: `cd /Users/userclaw/.openclaw/workspace/projects/clarity/app && npm run dev`

**What's Complete:**
- ✅ Basic Tier: TODAY (7 metrics), MONTHLY (inline edit), ANNUAL, DREAM MONTH, DRIVERS
- ✅ Pro Tier: COMPREHENSIVE view (full Shopify metrics)
- ✅ 2023 data loaded (156 days with Pro estimates)
- ✅ Decimal formatting (2 places everywhere)
- ✅ Monthly view inline editing (no popups)
- ✅ "Today" button on all pages

**What's Next (when resuming):**
1. ✅ **Dream Month Pro Mode** - COMPLETE (Mar 14, 2026) - Toggle for Basic/Pro scenarios with full comprehensive calculations
2. **Reports** - Generate summaries (daily/weekly/monthly/yearly)
3. **CSV Export** - Download data for Excel/Sheets
4. **Dashboard with Graphs** - Visual analytics (charts)
5. **Branding** - Rename "Clarity" → "Clarat" throughout

**Product Strategy:**
- **Basic (Free):** Quick daily overview + planning
- **Pro (Paid):** Deep analysis + reports + export + graphs

**Context preserved:**
- All Parca 2023 data in database (both basic + pro fields)
- Shared data model (Basic→Pro upgrade works seamlessly)
- Real-time calculations working perfectly
- All navigation working

---

**🚀 Ready to build Pro features!**  
Resume with: "Let's continue with Clarat" and read this STATUS.md.
