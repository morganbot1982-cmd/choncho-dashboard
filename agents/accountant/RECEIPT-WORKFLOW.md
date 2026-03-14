# Receipt Reconciliation Workflow

## Phase 1: Manual Weekly Reconciliation (Current)

### How to Submit a Receipt

**Via WhatsApp:**
1. Take photo of receipt
2. Send photo with text: "receipt" (or just send the photo, I'll recognize it)
3. Agent extracts details and confirms

**What Gets Extracted:**
- Vendor/merchant name
- Total amount
- Date of purchase
- GST (if shown)
- Category guess (based on vendor)

**Storage:**
- Receipts saved to: `pending-receipts/YYYY-MM-DD-[vendor].json`
- Original photo: `pending-receipts/YYYY-MM-DD-[vendor].jpg`

### Weekly Reconciliation Session

**When:** Friday 4 PM (or on-demand)

**Process:**
1. Agent shows all pending receipts for the week
2. For each receipt:
   - Shows photo + extracted details
   - Searches Xero bank feed for matching transaction
   - Suggests category code
3. You approve/correct category
4. Agent creates summary for you to enter in Xero

### Commands

- **"receipt"** + photo → Submit receipt for processing
- **"show receipts"** → View all pending receipts
- **"reconcile receipts"** → Start weekly reconciliation session
- **"clear receipt [date]"** → Mark receipt as processed

## Phase 2: Semi-Automated (Future)
- Auto-match to bank feed transactions
- Create draft journal entries
- Approve via WhatsApp

## Phase 3: Full Automation (Future - Requires Approval)
- Direct coding in Xero
- Auto-reconciliation
- Weekly summary only
