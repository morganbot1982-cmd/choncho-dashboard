#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Read DEBITS v2
const debitsPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-DEBITS-v2.csv');
const debitsData = fs.readFileSync(debitsPath, 'utf-8');
const lines = debitsData.split('\n');

console.log('Extracting unmatched transactions for manual review...\n');

// New CSV header with helpful columns
const header = '*Date,*Amount,*Payee,*Description,*Reference,AccountCode,TaxType,Notes,MORGAN_ACCOUNT,MORGAN_TAX,MORGAN_NOTES';

const unmatchedLines = [header];
let count = 0;

for (let i = 1; i < lines.length; i++) {
  const line = lines[i].trim();
  if (!line) continue;
  
  const columns = line.split(',');
  if (columns.length < 8) continue;
  
  const notes = columns[7] || '';
  
  // Only extract lines that need review
  if (notes.includes('REVIEW - No rule matched')) {
    // Add three empty columns at the end for Morgan's input
    const newLine = line + ',,,';
    unmatchedLines.push(newLine);
    count++;
  }
}

// Write to file
const outputPath = path.join(__dirname, 'processed', 'UNMATCHED-FOR-REVIEW.csv');
fs.writeFileSync(outputPath, unmatchedLines.join('\n'));

console.log(`✅ Extracted ${count} unmatched transactions`);
console.log(`📁 Saved to: ${outputPath}`);
console.log('\nNext steps:');
console.log('1. Open UNMATCHED-FOR-REVIEW.csv in Excel/Numbers');
console.log('2. Fill in MORGAN_ACCOUNT, MORGAN_TAX, MORGAN_NOTES columns');
console.log('3. Save and tell Choncho when done');
console.log('4. I\'ll merge your codes back into the main CSV\n');
