#!/usr/bin/env node
/**
 * Process Money OUT (Debit) transactions - Apply merchant rules
 */

const fs = require('fs');
const path = require('path');

function parseCSVLine(line) {
    const parts = [];
    let current = '';
    let inQuotes = false;
    
    for (let char of line) {
        if (char === '"') {
            inQuotes = !inQuotes;
        } else if (char === ',' && !inQuotes) {
            parts.push(current);
            current = '';
        } else {
            current += char;
        }
    }
    parts.push(current);
    return parts;
}

const audFile = path.join(__dirname, 'raw/statement_16108725_AUD_2017-04-28_2026-02-26.csv');
const lines = fs.readFileSync(audFile, 'utf-8').split('\n');

const debits = [];
for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    
    const parts = parseCSVLine(line);
    const amount = parseFloat(parts[3]);
    
    if (amount < 0) {
        debits.push({
            id: parts[0],
            date: parts[1],
            amount: amount,
            desc: parts[5],
            merchant: parts[14] || '',
            type: parts[21],
            detailType: parts[22]
        });
    }
}

console.log(`💸 Processing ${debits.length} MONEY OUT transactions\n`);

// Categorization logic
function categorize(txn) {
    const merchant = txn.merchant.toLowerCase();
    const desc = txn.desc.toLowerCase();
    const amount = txn.amount;
    
    let code = '';
    let name = '';
    let tax = 'GST on Expenses';
    let notes = '';
    
    // Conversions - leave uncoded
    if (txn.detailType === 'CONVERSION') {
        return { code: '', name: 'UNCODED', tax: '', notes: 'Currency conversion - Jason to advise' };
    }
    
    // Travel
    if (merchant.match(/flights on booking/)) {
        return { code: '494', name: 'Travel - International', tax, notes: 'International flight' };
    }
    if (merchant.match(/hotel at booking|jetstar|qantas|virgin australia/)) {
        return { code: '492', name: 'Travel - National', tax, notes: 'Domestic travel' };
    }
    if (merchant.match(/ace .*melbourne.*tullamarine/) && amount < 0) {
        return { code: '492', name: 'Travel - National', tax, notes: 'Car rental' };
    }
    if (merchant.match(/uber.*trip|uber   \*trip/)) {
        return { code: '493', name: 'Travel - Local', tax, notes: 'Uber ride' };
    }
    
    // Meals
    if (merchant.match(/uber.*eats/)) {
        if (amount >= -35) {
            return { code: '421', name: 'Meals & Food', tax, notes: 'Uber Eats ≤$35' };
        } else {
            return { code: '880', name: 'Owner A Drawings', tax: 'BAS Excluded', notes: 'Uber Eats >$35 - personal' };
        }
    }
    
    // Groceries
    if (merchant.match(/coles|woolworth|aldi|iga/)) {
        return { code: '880', name: 'Owner A Drawings', tax: 'BAS Excluded', notes: 'Groceries - personal' };
    }
    
    // Fines
    if (merchant.match(/sper|qld treasury/)) {
        return { code: 'NEW_FINES', name: 'Fines', tax: 'BAS Excluded', notes: 'QLD fines - not deductible' };
    }
    
    // Software
    if (merchant.match(/apple\.com\/bill|apple bill/)) {
        return { code: '429', name: 'General Expenses', tax, notes: 'Apple subscriptions' };
    }
    if (merchant.match(/clo\/clo3d|clo3d/)) {
        return { code: 'NEW_SOFTWARE', name: 'Software/Subscriptions', tax, notes: 'CLO3D design software' };
    }
    
    // Office/Hardware
    if (merchant.match(/ikea/)) {
        return { code: 'NEW_FURNITURE', name: 'Office Furniture', tax, notes: 'Office furniture' };
    }
    if (merchant.match(/bunnings/)) {
        return { code: 'NEW_OFFICE_EQUIP', name: 'Office Equipment/Supplies', tax, notes: 'Hardware/supplies' };
    }
    
    // Shipping
    if (merchant.match(/my post business|post office|australia post/)) {
        return { code: 'NEW_POSTAGE', name: 'Postage & Shipping', tax, notes: 'Shipping costs' };
    }
    
    // International purchases (Japan)
    if (merchant.match(/rakutenpay.*tokyo|tokyo|japan/)) {
        return { code: '429', name: 'General Expenses', tax: 'GST Free Imports', notes: 'Japan purchases' };
    }
    
    // Transfers (personal)
    if (txn.detailType === 'TRANSFER') {
        if (desc.match(/sent money to morgan|sent money to.*schoermer/i)) {
            return { code: '', name: 'UNCODED', tax: '', notes: 'Transfer to Morgan - leave uncoded' };
        }
        return { code: '880', name: 'Owner A Drawings', tax: 'BAS Excluded', notes: 'Personal transfer out' };
    }
    
    // Default: flag for review
    return { code: '', name: 'UNCODED', tax: '', notes: 'REVIEW - No rule matched' };
}

// Process all debits
const categorized = debits.map(txn => {
    const cat = categorize(txn);
    return {
        date: txn.date,
        amount: txn.amount,
        merchant: txn.merchant,
        desc: txn.desc,
        accountCode: cat.code,
        accountName: cat.name,
        taxType: cat.tax,
        notes: cat.notes
    };
});

// Summary stats
const summary = {};
categorized.forEach(txn => {
    const key = txn.accountCode || 'UNCODED';
    if (!summary[key]) {
        summary[key] = { name: txn.accountName, count: 0, total: 0 };
    }
    summary[key].count++;
    summary[key].total += txn.amount;
});

console.log('📊 Categorization Summary:\n');
Object.entries(summary)
    .sort((a,b) => a[1].total - b[1].total)
    .forEach(([code, stats]) => {
        console.log(`${code || 'UNCODED'} - ${stats.name}: ${stats.count} txns, $${stats.total.toFixed(2)}`);
    });

// Calculate totals
const coded = categorized.filter(t => t.accountCode);
const uncoded = categorized.filter(t => !t.accountCode);

console.log(`\n📈 Progress:`);
console.log(`  Coded: ${coded.length} transactions`);
console.log(`  Uncoded: ${uncoded.length} transactions (need review)`);
console.log(`  Total processed: ${categorized.length}`);

// Generate Xero CSV
const dateParts = (d) => d.split('-');
const xeroRows = categorized.map(row => {
    const parts = dateParts(row.date);
    const xeroDate = `${parts[0]}/${parts[1]}/${parts[2]}`;
    
    return {
        Date: xeroDate,
        Amount: row.amount.toFixed(2),
        Payee: row.merchant || row.desc.substring(0, 50),
        Description: row.desc.substring(0, 100),
        Reference: '',
        AccountCode: row.accountCode,
        TaxType: row.taxType,
        Notes: row.notes
    };
});

const headers = ['*Date', '*Amount', '*Payee', '*Description', '*Reference', 'AccountCode', 'TaxType', 'Notes'];
const csvContent = [
    headers.join(','),
    ...xeroRows.map(row => [
        row.Date,
        row.Amount,
        `"${row.Payee}"`,
        `"${row.Description}"`,
        `"${row.Reference}"`,
        row.AccountCode,
        row.TaxType,
        `"${row.Notes}"`
    ].join(','))
].join('\n');

const outputFile = path.join(__dirname, 'processed/wise-aud-xero-import-DEBITS-v1.csv');
fs.writeFileSync(outputFile, csvContent);

console.log(`\n💾 Output: ${outputFile}`);
console.log(`\n⚠️  NEW ACCOUNTS NEEDED:`);
console.log(`  - Fines (Expense, BAS Excluded)`);
console.log(`  - Software/Subscriptions (Expense, GST on Expenses)`);
console.log(`  - Office Furniture (Fixed Asset or Expense)`);
console.log(`  - Office Equipment/Supplies (Expense, GST on Expenses)`);
console.log(`  - Postage & Shipping (Expense, GST on Expenses)`);

// Show top uncoded merchants for quick review
const uncodedMerchants = {};
uncoded.forEach(u => {
    const m = u.merchant || 'NO MERCHANT';
    if (!uncodedMerchants[m]) uncodedMerchants[m] = { count: 0, total: 0 };
    uncodedMerchants[m].count++;
    uncodedMerchants[m].total += u.amount;
});

console.log(`\n🔍 Top 20 Uncoded Merchants (need rules):\n`);
Object.entries(uncodedMerchants)
    .sort((a,b) => a[1].total - b[1].total)
    .slice(0, 20)
    .forEach(([merchant, stats]) => {
        console.log(`${merchant}: ${stats.count} txns, $${stats.total.toFixed(2)}`);
    });
