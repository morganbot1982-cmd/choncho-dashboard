#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

// Load merchant rules
const merchantRules = require('./merchant-coding-rules-updated.json');

// Read DEBITS CSV
const debitsPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-DEBITS-v1.csv');
const debitsData = fs.readFileSync(debitsPath, 'utf-8');
const lines = debitsData.split('\n');

console.log('Updating DEBITS CSV with actual account codes...\n');

let updatedPlaceholders = 0;
let appliedMerchantRules = 0;
let ikeaSplits = { fixed: 0, expense: 0 };
let uberEatsSplits = { meals: 0, drawings: 0 };
let stillNeedReview = 0;

const updatedLines = lines.map((line, index) => {
  if (index === 0) return line; // Keep header
  if (!line.trim()) return line; // Keep empty lines
  
  const columns = line.split(',');
  if (columns.length < 8) return line; // Skip malformed lines
  
  const amount = parseFloat(columns[1]);
  const payee = columns[2].replace(/^"|"$/g, '');
  const accountCode = columns[5];
  const notes = columns[7];
  
  // 1. Replace placeholder codes
  if (accountCode === 'NEW_FINES') {
    columns[5] = '504';
    columns[6] = 'BAS Excluded';
    updatedPlaceholders++;
    return columns.join(',');
  }
  
  if (accountCode === 'NEW_POSTAGE') {
    columns[5] = '425';
    columns[6] = 'GST on Expenses';
    updatedPlaceholders++;
    return columns.join(',');
  }
  
  if (accountCode === 'NEW_SOFTWARE') {
    columns[5] = '485';
    columns[6] = 'GST on Expenses';
    updatedPlaceholders++;
    return columns.join(',');
  }
  
  if (accountCode === 'NEW_OFFICE_EQUIP') {
    columns[5] = '435';
    columns[6] = 'GST on Expenses';
    updatedPlaceholders++;
    return columns.join(',');
  }
  
  // 2. IKEA split rule
  if (accountCode === 'NEW_FURNITURE' || payee.toLowerCase().includes('ikea')) {
    const absAmount = Math.abs(amount);
    if (absAmount >= 100) {
      columns[5] = '710';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Fixed asset - furniture"';
      ikeaSplits.fixed++;
    } else {
      columns[5] = '435';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Office expense - small items"';
      ikeaSplits.expense++;
    }
    return columns.join(',');
  }
  
  // 3. Apply merchant rules to unmatched transactions
  if (notes.includes('REVIEW - No rule matched') || !accountCode) {
    const payeeLower = payee.toLowerCase();
    
    // Groceries
    if (/coles|woolworths|aldi/i.test(payee)) {
      columns[5] = '880';
      columns[6] = 'BAS Excluded';
      columns[7] = '"Groceries - personal"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Uber Eats split
    if (/uber.*eats/i.test(payee)) {
      const absAmount = Math.abs(amount);
      if (absAmount <= 35) {
        columns[5] = '421';
        columns[6] = 'GST on Expenses';
        columns[7] = '"Business meal"';
        uberEatsSplits.meals++;
      } else {
        columns[5] = '880';
        columns[6] = 'BAS Excluded';
        columns[7] = '"Personal"';
        uberEatsSplits.drawings++;
      }
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Transport (Uber rides, Lime)
    if (/uber.*trip|uber.*pending|uber.*lime/i.test(payee)) {
      columns[5] = '493';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Local transport"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Fabric stores
    if (/spotlight|lincraft/i.test(payee)) {
      columns[5] = '310';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Fabric/materials - COGS"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Amazon/eBay
    if (/amazon|ebay/i.test(payee)) {
      columns[5] = '435';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Office supplies/equipment"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Phone/Internet
    if (/optus|telstra|vodafone|superloop/i.test(payee)) {
      columns[5] = '429';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Phone/Internet"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Subscriptions
    if (/apple\.com|shopify|patreon|chatly|netflix|spotify|youtube|godaddy/i.test(payee)) {
      columns[5] = '485';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Software/subscriptions"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // BP fuel
    if (/\bbp\b/i.test(payee)) {
      columns[5] = '449';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Vehicle fuel"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // BCC Parking
    if (/bcc.*parking/i.test(payee)) {
      columns[5] = '493';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Travel - Local parking"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Transport/Personal
    if (/transportmainrds|elite focus/i.test(payee)) {
      columns[5] = '880';
      columns[6] = 'BAS Excluded';
      columns[7] = '"Personal"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Cash withdrawals
    if (/cash|atm|withdrawal|branch/i.test(payee)) {
      columns[5] = '880';
      columns[6] = 'BAS Excluded';
      columns[7] = '"Cash withdrawal"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // London Transport
    if (/tfl travel/i.test(payee)) {
      columns[5] = '494';
      columns[6] = 'GST Free Imports';
      columns[7] = '"International travel - London"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Xero
    if (/xero/i.test(payee)) {
      columns[5] = '485';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Accounting software"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Utilities (Red Energy)
    if (/red energy/i.test(payee)) {
      columns[5] = '429';
      columns[6] = 'GST on Expenses';
      columns[7] = '"Utilities"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Super Cheap Auto
    if (/super cheap auto/i.test(payee)) {
      columns[5] = '880';
      columns[6] = 'BAS Excluded';
      columns[7] = '"Personal - auto parts"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Aliexpress
    if (/aliexpress/i.test(payee)) {
      columns[5] = '310';
      columns[6] = 'GST on Expenses';
      columns[7] = '"COGS - supplies"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Golf (personal)
    if (/golf|victoria park/i.test(payee)) {
      columns[5] = '880';
      columns[6] = 'BAS Excluded';
      columns[7] = '"Personal - recreation"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Vet clinic (personal)
    if (/vet/i.test(payee)) {
      columns[5] = '880';
      columns[6] = 'BAS Excluded';
      columns[7] = '"Personal - vet"';
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    // Restaurants/Cafes - Apply $35 rule
    const restaurantPatterns = /cafe|restaurant|bar|grill|taco|pizza|sushi|noodle|thai|chinese|indian|italian|gramps|pepe|favolosa|river garden|kfc|cocos|cantaloupe|pilot|costa|vosh|dashi|kirk/i;
    if (restaurantPatterns.test(payee)) {
      const absAmount = Math.abs(amount);
      if (absAmount <= 35) {
        columns[5] = '421';
        columns[6] = 'GST on Expenses';
        columns[7] = '"Business meal"';
        uberEatsSplits.meals++; // Using same counter
      } else {
        columns[5] = '880';
        columns[6] = 'BAS Excluded';
        columns[7] = '"Personal - dining"';
        uberEatsSplits.drawings++; // Using same counter
      }
      appliedMerchantRules++;
      return columns.join(',');
    }
    
    stillNeedReview++;
  }
  
  return line;
});

// Write updated CSV
const outputPath = path.join(__dirname, 'processed', 'wise-aud-xero-import-DEBITS-v2.csv');
fs.writeFileSync(outputPath, updatedLines.join('\n'));

console.log(`✅ Updated ${updatedPlaceholders} placeholder codes with actual account numbers`);
console.log(`✅ Applied merchant rules to ${appliedMerchantRules} unmatched transactions`);
console.log(`📊 IKEA split: ${ikeaSplits.fixed} → Fixed Asset (710), ${ikeaSplits.expense} → Office Expense (435)`);
console.log(`🍔 Uber Eats split: ${uberEatsSplits.meals} → Meals (421), ${uberEatsSplits.drawings} → Drawings (880)`);
console.log(`📋 Still need review: ${stillNeedReview} transactions`);
console.log(`\nSaved: ${outputPath}\n`);

// Verify totals
let debitTotal = 0;
let txnCount = 0;
for (let i = 1; i < updatedLines.length; i++) {
  const line = updatedLines[i].trim();
  if (!line) continue;
  const columns = line.split(',');
  if (columns.length < 8) continue;
  const amount = parseFloat(columns[1]);
  if (!isNaN(amount)) {
    debitTotal += amount;
    txnCount++;
  }
}

console.log('Control Total Validation:');
console.log(`Transactions: ${txnCount} (expected: 1633)`);
console.log(`Total Debits: $${debitTotal.toFixed(2)} (expected: -$197,962.09)`);
