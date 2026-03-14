// Xero Wise CNY Reconciliation Script
// Copy/paste this into browser console on the Wise AUD reconcile page (with CNY search active)

(async function() {
  console.log("🦬 Starting CNY reconciliation automation...");
  
  const delay = ms => new Promise(resolve => setTimeout(resolve, ms));
  
  // Helper to extract CNY amount from description
  function extractCNYAmount(text) {
    const match = text.match(/(\d+(?:,\d+)?(?:\.\d+)?)\s+CNY/);
    return match ? match[1].replace(',', '') : null;
  }
  
  // Find all unreconciled CNY transactions
  const transactions = Array.from(document.querySelectorAll('[class*="bank-rec-row"]')).filter(row => {
    const desc = row.textContent;
    return desc.includes('CNY') && desc.includes('Converted') && desc.includes('AUD to');
  });
  
  console.log(`Found ${transactions.length} CNY transactions to reconcile`);
  
  if (transactions.length === 0) {
    console.log("✅ No CNY transactions found - either done or search not active");
    return;
  }
  
  let processed = 0;
  let failed = 0;
  
  for (let i = 0; i < transactions.length; i++) {
    const row = transactions[i];
    const descText = row.textContent;
    const cnyAmount = extractCNYAmount(descText);
    
    console.log(`\n[${i+1}/${transactions.length}] Processing: ${descText.substring(0, 60)}...`);
    
    try {
      // Find and click Transfer button
      const transferBtn = row.querySelector('a[href*="javascript:"]') || 
                          Array.from(row.querySelectorAll('a')).find(a => a.textContent.trim() === 'Transfer');
      
      if (!transferBtn) {
        console.log("❌ Could not find Transfer button");
        failed++;
        continue;
      }
      
      transferBtn.click();
      await delay(1000);
      
      // Find bank account dropdown
      const accountDropdown = document.querySelector('input[type="text"][class*="account"], select[class*="account"]') ||
                              Array.from(document.querySelectorAll('input[type="text"]')).find(inp => 
                                inp.value && inp.value.includes('Leif'));
      
      if (!accountDropdown) {
        console.log("❌ Could not find account dropdown");
        failed++;
        continue;
      }
      
      // Click to open dropdown
      accountDropdown.click();
      await delay(500);
      
      // Find Wise CNY option
      const wiseCNYOption = Array.from(document.querySelectorAll('div, li, option')).find(el => 
        el.textContent && el.textContent.includes('Wise CNY'));
      
      if (!wiseCNYOption) {
        console.log("❌ Could not find Wise CNY option");
        failed++;
        continue;
      }
      
      wiseCNYOption.click();
      await delay(1000);
      
      // Find and fill CNY amount field
      if (cnyAmount) {
        const amountInputs = Array.from(document.querySelectorAll('input[type="text"], input[type="number"]'));
        const cnyInput = amountInputs.find(inp => {
          const label = inp.previousElementSibling?.textContent || inp.parentElement?.textContent || '';
          return label.includes('CNY') || label.includes('Amount') || inp.placeholder?.includes('CNY');
        });
        
        if (cnyInput) {
          cnyInput.focus();
          cnyInput.value = cnyAmount;
          cnyInput.dispatchEvent(new Event('input', { bubbles: true }));
          cnyInput.dispatchEvent(new Event('change', { bubbles: true }));
          await delay(500);
        }
      }
      
      // Find and click Reconcile button
      const reconcileBtn = Array.from(document.querySelectorAll('a, button')).find(el => 
        el.textContent.trim() === 'Reconcile' || 
        el.textContent.trim() === 'OK' ||
        (el.href && el.href.includes('javascript:') && el.textContent.includes('Reconcile')));
      
      if (!reconcileBtn) {
        console.log("❌ Could not find Reconcile button");
        failed++;
        continue;
      }
      
      reconcileBtn.click();
      await delay(2000); // Wait for reconciliation to process
      
      processed++;
      console.log(`✅ Reconciled ${cnyAmount} CNY`);
      
    } catch (error) {
      console.log(`❌ Error: ${error.message}`);
      failed++;
    }
    
    // Longer delay between transactions
    if (i < transactions.length - 1) {
      await delay(2000);
    }
  }
  
  console.log("\n" + "=".repeat(60));
  console.log(`🎯 COMPLETE: ${processed} reconciled, ${failed} failed`);
  console.log("Refresh the page to see updated list");
  
})();
