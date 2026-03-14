# Quick Account Code Reference

Use these when filling in the MORGAN_ACCOUNT column in UNMATCHED-FOR-REVIEW.csv

## Revenue (Income)
- **200** - Sales (GST on Income)
- **201** - Income - Sean Maxwell Ferguson (GST on Income)
- **204** - Income - Maxine Pemble (GST on Income)
- **206** - Consulting Revenue (GST on Income)
- **212** - Income - Robert Cleary (GST on Income)
- **213** - Income - Dan Smith Rent Received (GST on Income)
- **214** - Income - Sky Point Roofing Labouring (GST on Income)
- **215** - Income - Win Mc Dowell Car Loan (BAS Excluded)
- **216** - Income - Morgan Williams Photography (GST on Income)
- **265** - Refunds (GST on Income)

## Cost of Goods Sold
- **310** - Cost of Goods Sold (GST on Expenses)

## Expenses
- **400** - Advertising (GST on Expenses)
- **420** - Entertainment (GST on Expenses)
- **421** - Meals & Food (GST on Expenses) - business meals ≤$35
- **425** - Freight and Courier (GST on Expenses)
- **429** - General Expenses (GST on Expenses)
- **435** - Office Expense (GST on Expenses)
- **449** - Motor Vehicle (GST on Expenses)
- **485** - Subscriptions (GST on Expenses)
- **492** - Travel - National (GST on Expenses)
- **493** - Travel - Local (GST on Expenses)
- **494** - Travel - International (GST Free Imports)
- **504** - Fines (BAS Excluded)

## Fixed Assets
- **710** - Fixed Asset (GST on Expenses) - large equipment/furniture ≥$100

## Personal
- **880** - Owner A Drawings (BAS Excluded) - all personal expenses

---

## Tax Types (for MORGAN_TAX column)

- **GST on Income** - For revenue/sales
- **GST on Expenses** - For most business expenses
- **GST Free Imports** - For international travel/purchases
- **BAS Excluded** - For personal drawings, fines, loan repayments (non-deductible)

---

## Quick Decision Guide

**Is it business or personal?**
- Personal → 880 Owner Drawings (BAS Excluded)
- Business → keep reading

**What kind of business expense?**
- Food/materials for resale → 310 COGS
- Meals ≤$35 → 421 Meals & Food
- Meals >$35 → 880 Drawings (personal)
- Software/subscriptions → 485 Subscriptions
- Office supplies/small items → 435 Office Expense
- Large furniture/equipment → 710 Fixed Asset
- Travel (flights/hotels/transport) → 492/493/494 depending on domestic/local/international
- Phone/internet/utilities → 429 General Expenses
- Fuel/car → 449 Motor Vehicle
- Shipping/postage → 425 Freight and Courier
- Advertising/marketing → 400 Advertising

**Not sure?**
- Default to 429 General Expenses if it's vaguely business-related
- Default to 880 Owner Drawings if it's personal
- Add a note in MORGAN_NOTES if unsure
