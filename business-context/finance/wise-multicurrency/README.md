# Wise Multi-Currency Import - Take 2

**Date Started:** Feb 25, 2026 11:13 PM
**Deadline:** Midnight (47 minutes)

## The Problem (First Import)
- Treated all 8 Wise currency accounts as AUD
- Mixed currencies without conversion tracking
- 1,907 transactions imported incorrectly into Xero
- Need to delete and re-import properly

## The Fix (This Import)
Process each currency account separately:
1. **AUD** - Primary account (largest, ~2.2MB statement)
2. **EUR** - European transactions
3. **CNY** - Chinese Yuan (supplier payments likely)
4. **USD** - US Dollar transactions
5. **GBP** - British Pound
6. **HKD** - Hong Kong Dollar
7. **JPY** - Japanese Yen
8. **AED** - UAE Dirham

## Folder Structure
- `raw/` - Original CSV exports from Wise (by currency)
- `processed/` - Cleaned/categorized CSVs ready for Xero
- `analysis/` - Summary reports, currency breakdowns, totals

## Multi-Currency Strategy
**Option 1: Separate Xero Accounts (Recommended)**
- Create 8 bank accounts in Xero (Wise AUD, Wise USD, Wise EUR, etc.)
- Import each currency into its matching account
- Xero handles forex tracking automatically

**Option 2: Convert All to AUD**
- Use historical exchange rates for each transaction date
- Import everything into single AUD account
- More complex, higher error risk

**Decision:** TBD - will consult with Jason's existing Wise setup first

## Processing Steps
1. Morgan exports CSVs from Wise (one per currency, same date range)
2. Copy CSVs to `/Users/Shared/OpenClaw Inbox/wise-statements-multicurrency/`
3. Choncho processes each file:
   - Validate currency matches filename
   - Analyze transaction patterns
   - Apply account code mapping (from backup reference)
   - Generate Xero-ready import files
4. Review summaries before Xero import
5. Import to Xero (one currency at a time)

## Reference Files
- Old (incorrect) import: `/Users/Shared/OpenClaw Inbox/wise_reconciliation_v26.csv`
- Backup will be created before deletion
- Account coding logic preserved for reuse

## Timeline
- **23:13-23:30** - CSV export from Wise
- **23:30-23:50** - Process and categorize
- **23:50-00:00** - Validate and prep for Xero

Let's get it done. 🦬
