#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

console.log('Creating final Xero import file (CREDITS + DEBITS)...\n');

// Read CREDITS
const creditsPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-CREDITS-v2.csv');
const creditsData = fs.readFileSync(creditsPath, 'utf-8');
const creditsLines = creditsData.split('\n');

// Read DEBITS (final)
const debitsPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-DEBITS-FINAL.csv');
const debitsData = fs.readFileSync(debitsPath, 'utf-8');
const debitsLines = debitsData.split('\n');

// Combine (keep one header)
const finalLines = [creditsLines[0]]; // Header

// Add all CREDITS (skip header)
for (let i = 1; i < creditsLines.length; i++) {
  if (creditsLines[i].trim()) {
    finalLines.push(creditsLines[i]);
  }
}

// Add all DEBITS (skip header)
for (let i = 1; i < debitsLines.length; i++) {
  if (debitsLines[i].trim()) {
    finalLines.push(debitsLines[i]);
  }
}

// Write final file
const finalPath = path.join(__dirname, 'WISE-AUD-XERO-IMPORT-FINAL.csv');
fs.writeFileSync(finalPath, finalLines.join('\n'));

console.log(`✅ Created: ${finalPath}`);

// Validate totals
let creditTotal = 0;
let debitTotal = 0;
let totalTransactions = 0;
let codedTransactions = 0;
let uncodedTransactions = 0;

for (let i = 1; i < finalLines.length; i++) {
  const line = finalLines[i].trim();
  if (!line) continue;
  
  const cols = line.split(',');
  if (cols.length < 8) continue;
  
  const amount = parseFloat(cols[1]);
  const accountCode = cols[5];
  
  if (!isNaN(amount)) {
    totalTransactions++;
    
    if (amount > 0) {
      creditTotal += amount;
    } else {
      debitTotal += amount;
    }
    
    if (accountCode && accountCode.trim() && !cols[7].includes('REVIEW')) {
      codedTransactions++;
    } else {
      uncodedTransactions++;
    }
  }
}

const netTotal = creditTotal + debitTotal;

console.log(`\n📊 Final Import Summary:`);
console.log(`   Total Transactions: ${totalTransactions}`);
console.log(`   Coded: ${codedTransactions} (${Math.round(codedTransactions/totalTransactions*100)}%)`);
console.log(`   Uncoded: ${uncodedTransactions}`);
console.log(`\n💰 Control Totals:`);
console.log(`   Credits:  $${creditTotal.toFixed(2)} (expected: $198,003.59)`);
console.log(`   Debits:   $${debitTotal.toFixed(2)} (expected: -$197,962.09)`);
console.log(`   Net:      $${netTotal.toFixed(2)} (expected: $41.50)`);

if (Math.abs(creditTotal - 198003.59) < 0.01 && 
    Math.abs(debitTotal - (-197962.09)) < 0.01 &&
    Math.abs(netTotal - 41.50) < 0.01) {
  console.log(`\n✅ TOTALS VALIDATED - Ready for Xero import!`);
} else {
  console.log(`\n⚠️  Warning: Totals don't match control baseline`);
}
