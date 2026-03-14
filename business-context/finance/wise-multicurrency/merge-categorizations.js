#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('Merging Morgan\'s categorizations back into main file...\n');

// Tax type mapping based on account codes
const accountTaxTypes = {
  '200': 'GST on Income',
  '201': 'GST on Income',
  '204': 'GST on Income',
  '206': 'GST on Income',
  '212': 'GST on Income',
  '213': 'GST on Income',
  '214': 'GST on Income',
  '215': 'BAS Excluded', // Car loan
  '216': 'GST on Income',
  '265': 'GST on Income',
  '310': 'GST on Expenses', // COGS
  '400': 'GST on Expenses', // Advertising
  '404': 'GST on Expenses', // Unknown - assuming expenses
  '420': 'GST on Expenses',
  '421': 'GST on Expenses', // Meals
  '425': 'GST on Expenses', // Freight
  '429': 'GST on Expenses', // General
  '435': 'GST on Expenses', // Office
  '449': 'GST on Expenses', // Motor Vehicle
  '453': 'GST on Expenses', // Unknown - assuming expenses
  '485': 'GST on Expenses', // Subscriptions
  '492': 'GST on Expenses', // Travel National
  '493': 'GST on Expenses', // Travel Local
  '494': 'GST Free Imports', // Travel International
  '504': 'BAS Excluded', // Fines
  '710': 'GST on Expenses', // Fixed Asset
  '880': 'BAS Excluded'  // Owner Drawings
};

// Read categorized file
const categorizedPath = path.join(__dirname, 'processed', 'UNMATCHED-CATEGORIZED.csv');
const categorizedData = fs.readFileSync(categorizedPath, 'utf-8');
const categorizedLines = categorizedData.split('\n');

// Read original DEBITS file
const debitsPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-DEBITS-v2.csv');
const debitsData = fs.readFileSync(debitsPath, 'utf-8');
const debitsLines = debitsData.split('\n');

// Create lookup map from categorized data (by date+amount+payee)
const categorizationMap = {};
let categorizedCount = 0;

for (let i = 1; i < categorizedLines.length; i++) {
  const line = categorizedLines[i].trim();
  if (!line) continue;
  
  const cols = line.split(',');
  if (cols.length < 9) continue;
  
  const date = cols[0];
  const amount = cols[1];
  const payee = cols[2].replace(/^"|"$/g, '');
  const accountCode = cols[5];
  
  if (accountCode && accountCode.trim()) {
    const key = `${date}|${amount}|${payee}`;
    const taxType = accountTaxTypes[accountCode.trim()] || 'GST on Expenses';
    categorizationMap[key] = {
      accountCode: accountCode.trim(),
      taxType: taxType
    };
    categorizedCount++;
  }
}

console.log(`Loaded ${categorizedCount} categorizations from Morgan`);

// Update DEBITS file with categorizations
const updatedDebitsLines = debitsLines.map((line, index) => {
  if (index === 0) return line; // Keep header
  if (!line.trim()) return line;
  
  const cols = line.split(',');
  if (cols.length < 8) return line;
  
  const date = cols[0];
  const amount = cols[1];
  const payee = cols[2].replace(/^"|"$/g, '');
  const key = `${date}|${amount}|${payee}`;
  
  if (categorizationMap[key]) {
    cols[5] = categorizationMap[key].accountCode;
    cols[6] = categorizationMap[key].taxType;
    cols[7] = `"Categorized by Morgan"`;
    return cols.join(',');
  }
  
  return line;
});

// Write updated DEBITS
const outputPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-DEBITS-FINAL.csv');
fs.writeFileSync(outputPath, updatedDebitsLines.join('\n'));

console.log(`✅ Updated DEBITS file: ${outputPath}`);

// Verify totals
let debitTotal = 0;
let codedCount = 0;
let uncodedCount = 0;

for (let i = 1; i < updatedDebitsLines.length; i++) {
  const line = updatedDebitsLines[i].trim();
  if (!line) continue;
  const cols = line.split(',');
  if (cols.length < 8) continue;
  
  const amount = parseFloat(cols[1]);
  const accountCode = cols[5];
  
  if (!isNaN(amount)) {
    debitTotal += amount;
  }
  
  if (accountCode && accountCode.trim() && !cols[7].includes('REVIEW')) {
    codedCount++;
  } else {
    uncodedCount++;
  }
}

console.log(`\n📊 DEBITS Summary:`);
console.log(`   Coded: ${codedCount}`);
console.log(`   Uncoded: ${uncodedCount}`);
console.log(`   Total: $${debitTotal.toFixed(2)} (expected: -$197,962.09)`);

console.log(`\n✅ Ready to merge with CREDITS!`);
