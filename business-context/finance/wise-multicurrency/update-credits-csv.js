#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Load the account mapping
const accountMapping = require('./categorization-rules-updated.json');

// Read the CREDITS CSV
const creditsPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-CREDITS.csv');
const creditsData = fs.readFileSync(creditsPath, 'utf-8');
const lines = creditsData.split('\n');

// Create payer to account code lookup
const payerToAccount = {};
for (const [accountCode, config] of Object.entries(accountMapping.accountMapping)) {
  for (const payer of config.payers) {
    payerToAccount[payer.toUpperCase()] = {
      code: accountCode,
      taxType: config.taxType
    };
  }
}

// Special handling
const leaveUncodedPayers = accountMapping.leaveUncoded.payers.map(p => p.toUpperCase());
const companyTransferPayers = accountMapping.specialHandling.companyTransfers.payers.map(p => p.toUpperCase());

console.log('Updating CREDITS CSV with actual account codes...\n');

let updatedCount = 0;
let uncodedCount = 0;
let transferCount = 0;
let conversionCount = 0;

const updatedLines = lines.map((line, index) => {
  if (index === 0) return line; // Keep header
  if (!line.trim()) return line; // Keep empty lines
  
  const columns = line.split(',');
  if (columns.length < 8) return line; // Skip malformed lines
  
  const payee = columns[2].replace(/^"|"$/g, '').trim().toUpperCase();
  const accountCode = columns[5];
  const description = columns[3].replace(/^"|"$/g, '').toLowerCase();
  
  // Handle conversions
  if (description.includes('conversion') || description.includes('converted')) {
    conversionCount++;
    return line; // Leave uncoded for Jason
  }
  
  // Handle company transfers
  if (companyTransferPayers.includes(payee)) {
    transferCount++;
    return line; // Leave uncoded for manual matching
  }
  
  // Handle Morgan Schoermer transfers
  if (leaveUncodedPayers.includes(payee)) {
    uncodedCount++;
    return line; // Leave for Morgan to decide
  }
  
  // Update with actual account code if we have a mapping
  const mapping = payerToAccount[payee];
  if (mapping && accountCode.startsWith('NEW_') || accountCode === 'TBD') {
    columns[5] = mapping.code;
    columns[6] = mapping.taxType;
    updatedCount++;
    return columns.join(',');
  }
  
  return line;
});

// Write updated CSV
const outputPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-CREDITS-v2.csv');
fs.writeFileSync(outputPath, updatedLines.join('\n'));

console.log(`✅ Updated ${updatedCount} transactions with actual account codes`);
console.log(`📋 ${uncodedCount} Morgan Schoermer transfers left uncoded`);
console.log(`🔄 ${transferCount} company transfers left uncoded (manual matching)`);
console.log(`💱 ${conversionCount} conversions left uncoded (Jason to advise)`);
console.log(`\nSaved: ${outputPath}\n`);

// Verify totals
let creditTotal = 0;
let txnCount = 0;
for (let i = 1; i < updatedLines.length; i++) {
  const line = updatedLines[i].trim();
  if (!line) continue;
  const columns = line.split(',');
  if (columns.length < 8) continue;
  const amount = parseFloat(columns[1]);
  if (!isNaN(amount)) {
    creditTotal += amount;
    txnCount++;
  }
}

console.log('Control Total Validation:');
console.log(`Transactions: ${txnCount} (expected: 436)`);
console.log(`Total Credits: $${creditTotal.toFixed(2)} (expected: $198,003.59)`);
