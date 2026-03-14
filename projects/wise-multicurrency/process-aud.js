#!/usr/bin/env node
/**
 * Wise AUD Transaction Processor
 * Categorizes 2,070 AUD transactions for Xero import
 */

const fs = require('fs');
const path = require('path');

// Read AUD CSV
const audFile = path.join(__dirname, 'raw/statement_16108725_AUD_2017-04-28_2026-02-26.csv');
const chartFile = path.join(__dirname, 'ChartOfAccounts.csv');

console.log('📊 Processing Wise AUD transactions...\n');

// Parse CSV helper
function parseCSV(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    const lines = content.split('\n').filter(l => l.trim());
    const headers = lines[0].split(',').map(h => h.replace(/"/g, '').trim());
    
    return lines.slice(1).map(line => {
        // Simple CSV parser (handles quoted fields)
        const values = [];
        let current = '';
        let inQuotes = false;
        
        for (let char of line) {
            if (char === '"') {
                inQuotes = !inQuotes;
            } else if (char === ',' && !inQuotes) {
                values.push(current.trim());
                current = '';
            } else {
                current += char;
            }
        }
        values.push(current.trim());
        
        const obj = {};
        headers.forEach((h, i) => {
            obj[h] = values[i] || '';
        });
        return obj;
    });
}

// Categorization rules
function categorizeTransaction(txn) {
    const desc = txn.Description.toLowerCase();
    const merchant = (txn.Merchant || '').toLowerCase();
    const amount = parseFloat(txn.Amount);
    const type = txn['Transaction Type'];
    const detailsType = txn['Transaction Details Type'];
    
    // Default category
    let accountCode = '880'; // Owner A Drawings (conservative default)
    let accountName = 'Owner A Drawings';
    let notes = '';
    
    // CREDIT transactions (money in)
    if (type === 'CREDIT') {
        if (desc.includes('received money from leif oh leif')) {
            accountCode = '881';
            accountName = 'Owner Funds Introduced';
            notes = 'Transfer from company';
        } else if (merchant.includes('photography') || desc.includes('photography')) {
            accountCode = '258';
            accountName = 'Photography Income';
        } else if (desc.includes('consulting') || merchant.includes('consultant')) {
            accountCode = '206';
            accountName = 'Consulting Revenue';
        } else if (desc.includes('rent')) {
            accountCode = '255';
            accountName = 'Rent Received';
        } else {
            accountCode = '260';
            accountName = 'Abyss Income';
            notes = 'Review - uncat income';
        }
    }
    
    // DEBIT transactions (money out)
    if (type === 'DEBIT') {
        // Card transactions
        if (detailsType === 'CARD') {
            // Groceries & Personal
            if (merchant.match(/coles|woolworth|aldi|iga|grocery/)) {
                accountCode = '880';
                accountName = 'Owner A Drawings';
                notes = 'Groceries - personal';
            }
            // Meals (solo, under $35)
            else if (merchant.match(/mcdonald|kfc|subway|cafe|coffee|restaurant/) && Math.abs(amount) <= 35) {
                accountCode = '421';
                accountName = 'Meals & Food';
                notes = 'Solo meal ≤$35';
            }
            // Entertainment (over $35 or ambiguous)
            else if (merchant.match(/restaurant|bar|pub|brewery|dining/) && Math.abs(amount) > 35) {
                accountCode = '420';
                accountName = 'Entertainment';
                notes = 'Meal >$35 - verify attendees';
            }
            // Bunnings, hardware
            else if (merchant.match(/bunnings|hardware|mitre 10/)) {
                accountCode = '429';
                accountName = 'General Expenses';
                notes = 'Hardware - verify business use';
            }
            // Amazon, online shopping
            else if (merchant.match(/amazon|ebay|online/)) {
                accountCode = '429';
                accountName = 'General Expenses';
                notes = 'Online purchase - verify';
            }
            // Fuel/petrol
            else if (merchant.match(/bp |shell|caltex|7-eleven|servo|petrol|fuel/)) {
                accountCode = '880';
                accountName = 'Owner A Drawings';
                notes = 'Fuel - no business vehicle';
            }
        }
        
        // Transfers (between Wise accounts or external)
        if (detailsType === 'TRANSFER' || desc.includes('sent money to')) {
            if (desc.match(/cnyCNY|eur|usd|gbp/i)) {
                accountCode = '877';
                accountName = 'Tracking Transfers';
                notes = 'Inter-account transfer (Wise multi-currency)';
            } else {
                accountCode = '880';
                accountName = 'Owner A Drawings';
                notes = 'External transfer - verify';
            }
        }
        
        // International travel (if date range matches known trip)
        if (desc.match(/germany|berlin|europe|EUR/) && txn.Date.startsWith('2019')) {
            accountCode = '494';
            accountName = 'Travel - International';
            notes = '2019 Germany business trip';
        }
    }
    
    return { accountCode, accountName, notes };
}

// Process transactions
const transactions = parseCSV(audFile);
console.log(`📝 Loaded ${transactions.length} transactions\n`);

const categorized = transactions.map(txn => {
    const cat = categorizeTransaction(txn);
    return {
        ...txn,
        'Xero Account Code': cat.accountCode,
        'Xero Account Name': cat.accountName,
        'Categorization Notes': cat.notes
    };
});

// Summary stats
const summary = {};
categorized.forEach(txn => {
    const key = `${txn['Xero Account Code']} - ${txn['Xero Account Name']}`;
    if (!summary[key]) {
        summary[key] = { count: 0, total: 0 };
    }
    summary[key].count++;
    summary[key].total += parseFloat(txn.Amount);
});

console.log('📊 Categorization Summary:\n');
Object.entries(summary)
    .sort((a, b) => b[1].count - a[1].count)
    .forEach(([key, stats]) => {
        console.log(`${key}: ${stats.count} txns, $${stats.total.toFixed(2)}`);
    });

// Write output
const outputFile = path.join(__dirname, 'processed/wise-aud-categorized.csv');
const headers = Object.keys(categorized[0]);
const csvContent = [
    headers.join(','),
    ...categorized.map(row => headers.map(h => `"${row[h]}"`).join(','))
].join('\n');

fs.writeFileSync(outputFile, csvContent);
console.log(`\n✅ Output saved: ${outputFile}`);
console.log(`\n🔍 Review the categorization and refine before Xero import.`);
