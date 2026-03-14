#!/usr/bin/env node
/**
 * Generate Xero-compatible CSV for bank statement import
 * Format: https://central.xero.com/s/article/Import-a-precoded-CSV-bank-statement
 */

const fs = require('fs');
const path = require('path');

// Load categorization rules
const rules = JSON.parse(fs.readFileSync(path.join(__dirname, 'categorization-rules.json'), 'utf-8'));

// Parse Wise CSV
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

const transactions = [];
for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (!line) continue;
    
    const parts = parseCSVLine(line);
    transactions.push({
        id: parts[0],
        date: parts[1],
        dateTime: parts[2],
        amount: parseFloat(parts[3]),
        currency: parts[4],
        desc: parts[5],
        ref: parts[6],
        balance: parts[7],
        exchangeFrom: parts[8],
        exchangeTo: parts[9],
        exchangeRate: parts[10],
        payer: parts[11],
        payee: parts[12],
        payeeAcctNum: parts[13],
        merchant: parts[14],
        cardLast4: parts[15],
        cardHolder: parts[16],
        attachment: parts[17],
        note: parts[18],
        totalFees: parts[19],
        exchangeToAmount: parts[20],
        transactionType: parts[21],
        detailsType: parts[22]
    });
}

console.log(`📝 Processing ${transactions.length} AUD transactions for Xero import\n`);

// Build account code lookup
const payerToAccount = {};

// Existing accounts
Object.entries(rules.existingAccountCoding).forEach(([code, config]) => {
    config.payers.forEach(payer => {
        payerToAccount[payer.toLowerCase()] = {
            code: code === '200_NO_GST' ? '200' : code,
            name: config.name,
            taxType: config.taxType
        };
    });
});

// New accounts (use placeholder codes - Morgan will create in Xero first)
rules.newAccountsToCreate.forEach(acc => {
    acc.payers.forEach(payer => {
        payerToAccount[payer.toLowerCase()] = {
            code: 'NEW_' + acc.name.replace(/[^A-Z]/g, '').substring(0, 10).toUpperCase(),
            name: acc.name,
            taxType: acc.taxType,
            needsCreation: true
        };
    });
});

// Special handling lookups
const leaveUncoded = new Set(rules.leaveUncoded.payers.map(p => p.toLowerCase()));
const companyTransfers = new Set(rules.specialHandling.companyTransfers.payers.map(p => p.toLowerCase()));

// Categorize transactions
const xeroRows = [];
const summary = {
    coded: 0,
    uncoded: 0,
    transfers: 0,
    conversions: 0,
    byAccount: {}
};

transactions.forEach(txn => {
    const payer = (txn.payer || '').toLowerCase();
    const desc = txn.desc.toLowerCase();
    
    let accountCode = '';
    let taxType = '';
    let notes = '';
    let skip = false;
    
    // Company transfers (mark as transfer, no code)
    if (companyTransfers.has(payer) || desc.includes('leif oh leif')) {
        notes = 'TRANSFER TO LOLD';
        summary.transfers++;
        skip = false; // Include but no coding
    }
    // Leave uncoded (Morgan's personal transfers)
    else if (leaveUncoded.has(payer)) {
        notes = 'UNCODED - Morgan to handle';
        summary.uncoded++;
    }
    // Conversions (leave uncoded)
    else if (txn.detailsType === 'CONVERSION') {
        notes = 'CONVERSION - Jason to advise';
        summary.conversions++;
    }
    // Money Added (leave uncoded)
    else if (txn.detailsType === 'MONEY_ADDED') {
        notes = 'MONEY ADDED - Verify source';
        summary.uncoded++;
    }
    // Card Refunds
    else if (txn.detailsType === 'CARD' && txn.amount > 0) {
        accountCode = '265';
        taxType = 'GST on Income';
        notes = 'Card refund';
        summary.coded++;
    }
    // Match by payer
    else if (payerToAccount[payer]) {
        const acct = payerToAccount[payer];
        accountCode = acct.code;
        taxType = acct.taxType;
        if (acct.needsCreation) {
            notes = `NEW ACCOUNT NEEDED: ${acct.name}`;
        }
        summary.coded++;
    }
    // Unmatched
    else if (txn.amount > 0) {
        notes = 'UNCODED - Review payer';
        summary.uncoded++;
    }
    
    // Track by account
    if (accountCode) {
        if (!summary.byAccount[accountCode]) {
            summary.byAccount[accountCode] = { count: 0, total: 0 };
        }
        summary.byAccount[accountCode].count++;
        summary.byAccount[accountCode].total += txn.amount;
    }
    
    // Convert date to DD/MM/YYYY for Xero
    const dateParts = txn.date.split('-');
    const xeroDate = `${dateParts[0]}/${dateParts[1]}/${dateParts[2]}`;
    
    // Only include money IN (credits) for this first pass
    if (txn.amount > 0) {
        xeroRows.push({
            Date: xeroDate,
            Amount: txn.amount.toFixed(2),
            Payee: txn.payer || txn.desc.substring(0, 50),
            Description: txn.desc.substring(0, 100),
            Reference: txn.ref || txn.id,
            AccountCode: accountCode,
            TaxType: taxType,
            Notes: notes
        });
    }
});

// Generate Xero CSV
const xeroHeaders = ['*Date', '*Amount', '*Payee', '*Description', '*Reference', 'AccountCode', 'TaxType', 'Notes'];
const xeroCSV = [
    xeroHeaders.join(','),
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

// Write output
const outputFile = path.join(__dirname, 'processed/wise-aud-xero-import-CREDITS.csv');
fs.writeFileSync(outputFile, xeroCSV);

console.log('✅ Xero Import CSV Generated\n');
console.log('📊 Summary:\n');
console.log(`Total money IN transactions: ${xeroRows.length}`);
console.log(`  Coded: ${summary.coded}`);
console.log(`  Transfers to LOLD: ${summary.transfers}`);
console.log(`  Conversions (uncoded): ${summary.conversions}`);
console.log(`  Uncoded (other): ${summary.uncoded}\n`);

console.log('📋 By Account Code:\n');
Object.entries(summary.byAccount)
    .sort((a,b) => b[1].total - a[1].total)
    .forEach(([code, stats]) => {
        console.log(`  ${code}: ${stats.count} txns, $${stats.total.toFixed(2)}`);
    });

console.log(`\n💾 Output: ${outputFile}`);
console.log('\n⚠️  NEW ACCOUNTS TO CREATE IN XERO FIRST:\n');
rules.newAccountsToCreate.forEach(acc => {
    console.log(`  - ${acc.name} (Revenue, ${acc.taxType})`);
});
console.log('\n🔍 Then import this CSV to Wise AUD account in Xero.');
