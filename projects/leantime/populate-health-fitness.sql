-- Populate Health & Fitness Agent project (ID 15) with tasks
-- Priority: 1=High, 2=Medium-High, 3=Medium, 4=Low
-- Status: 0=To Do, 1=In Progress, 3=Done

-- Phase 0: Baseline Assessment (Current Priority Tasks)

-- HIGH PRIORITY TASKS (Do Now)
INSERT INTO zp_tickets (projectId, headline, description, priority, status, type, dateToFinish, userId) VALUES
(15, '🚨 Complete Gastro Email Form', 
'Colonoscopy clinic called - need to complete email form for A/Prof Daniel Worthley (Gastroenterology specialist).

**Action:** Fill out form and email back to clinic.
**Referral:** See referrals/ folder for details.
**Priority:** URGENT - blocking gastroscopy appointment.', 
1, 0, 'task', '2026-03-02 17:00:00', 1),

(15, '📞 Book ENT Appointment', 
'Call Dr Jo-Lyn McKenzie (ENT Specialist) to book appointment for enlarged tonsils assessment (possible tonsillectomy).

**Phone:** 07 3053 3833
**Referral:** See referrals/ folder
**Reason:** Enlarged tonsils
**Priority:** HIGH - one of 3 specialist referrals from GP.', 
1, 0, 'task', '2026-03-02 17:00:00', 1),

(15, '🩸 Complete Blood Work - 4Cyte Pathology', 
'Walk-in blood test at 4Cyte Pathology (fasting required for some tests).

**Tests:** FBC, lipids (fasting), HbA1c, thyroid, iron, STI screen
**Location:** 4Cyte Pathology (walk-in, no appointment)
**Phone:** 13 42 98
**Website:** www.4cyte.com.au
**Important:** Fast before going (lipids test requires fasting)
**Next:** Results will establish baseline health metrics.', 
1, 0, 'task', '2026-03-03 09:00:00', 1);

-- MEDIUM PRIORITY TASKS (This Week)
INSERT INTO zp_tickets (projectId, headline, description, priority, status, type, dateToFinish, userId) VALUES
(15, '⚖️ Baseline Measurements', 
'Measure and record current baseline metrics:

**To measure:**
- Weight (kg) - weigh same time each week (e.g., Monday morning)
- Waist (cm)
- Hips (cm) - optional
- Chest (cm) - optional
- Arms (cm) - optional

**Why:** Establish starting point to track meaningful progress.
**Where to record:** Create health-data/baseline.json', 
2, 0, 'task', '2026-03-05 17:00:00', 1),

(15, '📸 Baseline Photos', 
'Take baseline photos for personal progress tracking (private storage):

**Photos needed:**
- Front view
- Side view (left)
- Back view

**Important:** Private storage only (not shared). For your own progress comparison.
**Where to save:** health-data/ folder (local only).', 
2, 0, 'task', '2026-03-05 17:00:00', 1),

(15, '🍽️ Track Food for 3-5 Days', 
'Log everything you eat for 3-5 days to estimate current calorie intake BEFORE making any changes.

**Goal:** Awareness of current eating patterns (not restriction).
**How:** Write down or photo log every meal/snack.
**Why:** Establishes baseline intake to calculate realistic calorie targets.
**Next:** Use this data to calculate TDEE and deficit goals.', 
2, 0, 'task', '2026-03-07 17:00:00', 1),

(15, '🧮 Calculate TDEE', 
'Calculate Total Daily Energy Expenditure using online calculator.

**Inputs needed:**
- Age
- Weight (from baseline measurements)
- Height
- Activity level (likely "sedentary" or "lightly active")

**Use calculator:** tdeecalculator.net or similar
**Purpose:** Determine how many calories you burn daily (maintenance level).
**Next:** Set target calories based on weight loss goals (typically 500 cal deficit per day for 0.5kg/week loss).', 
2, 0, 'task', '2026-03-06 17:00:00', 1),

(15, '🎯 Set Realistic Goals', 
'Set realistic, sustainable weight/fitness/energy goals based on baseline data.

**Consider:**
- Target weight (healthy rate: 0.5-1kg per week)
- Target waist measurement
- Target daily steps
- Target sleep hours
- Timeline (e.g., 6 months)

**Example:** Current 95kg → Target 85kg over 10-20 weeks
**Important:** Based on actual data, not wishful thinking.
**Where to record:** health-data/baseline.json', 
3, 0, 'task', '2026-03-08 17:00:00', 1),

(15, '📄 Create baseline.json', 
'Create health-data/baseline.json file with all baseline metrics and goals.

**Include:**
- Assessment date
- Current stats (weight, waist, height, age, activity level, steps, sleep)
- GP checkup results (blood pressure, cholesterol, notes)
- Goals (target weight, waist, steps, sleep, timeline)
- TDEE and target calories

**Example structure:** See health-fitness-agent/README.md
**Purpose:** Single source of truth for baseline → personalized agent settings.', 
3, 0, 'task', '2026-03-09 17:00:00', 1);

-- COMPLETED TASKS (For Reference/History)
INSERT INTO zp_tickets (projectId, headline, description, priority, status, type, dateToFinish, userId) VALUES
(15, '✅ Book GP Appointment', 
'Booked GP health check appointment.

**Completed:** Thu Feb 26, 2026, 11:15 AM
**Doctor:** Dr Glenn Clifford (GP, Men\'s Health & Preventative Medicine)
**Clinic:** One Health Clinics Albion
**Result:** 3 specialist referrals issued + blood work ordered.', 
3, 3, 'task', '2026-02-26 11:15:00', 1),

(15, '✅ Attend GP Appointment', 
'Attended GP health check appointment.

**Completed:** Thu Feb 26, 2026
**Outcome:** 3 specialist referrals issued (cardiology, gastro, ENT) + blood work ordered.', 
3, 3, 'task', '2026-02-26 11:15:00', 1),

(15, '✅ Book Cardiology Appointment', 
'Booked cardiology appointment with Dr Andrew Rainbird.

**Completed:** Booked Mon 9th March, 1:55 PM
**Location:** Advara HeartCare, Milton
**Tests:** Exercise Stress Echo, Calcium Score, CT Coronary Angiogram', 
2, 3, 'task', '2026-02-27 17:00:00', 1);

-- FUTURE MILESTONES (Phases 1-4)
INSERT INTO zp_tickets (projectId, headline, description, priority, status, type, dateToFinish, userId) VALUES
(15, 'Phase 1: Food Tracking MVP', 
'Set up WhatsApp/Telegram food tracking system.

**Features:**
- Photo message handler
- Image analysis → calorie estimation
- Daily log (CSV or Google Sheet)
- Evening recap message

**Timeline:** Week 1 after baseline complete
**Depends on:** Baseline assessment complete', 
3, 0, 'milestone', '2026-03-15 17:00:00', 1),

(15, 'Phase 2: Spending Tracker', 
'Implement personal spending tracker.

**Features:**
- Parse text messages ("spent $X on Y")
- Auto-categorize purchases
- Weekly spending summary

**Timeline:** Week 2
**Depends on:** Food tracking working', 
3, 0, 'milestone', '2026-03-22 17:00:00', 1),

(15, 'Phase 3: Movement Reminders', 
'Launch movement reminder system.

**Phase 1 routine:**
- 10 pushups, 3x/day (morning, midday, evening)
- Water reminders every 2 hours
- 5-minute walk after lunch

**Features:**
- Cron-based reminders
- Check-in system (reply "done")
- Streak tracking

**Timeline:** Week 3
**Depends on:** Baseline established, habits ready to start', 
3, 0, 'milestone', '2026-03-29 17:00:00', 1),

(15, 'Phase 4: Dashboard Integration', 
'Add health metrics to main dashboard.

**Show:**
- Today\'s calories logged
- Personal spending (daily/weekly)
- Movement streaks
- Weekly trends chart
- Quick stats (7-day avg, longest streak)

**Timeline:** Week 4
**Depends on:** All tracking systems working', 
4, 0, 'milestone', '2026-04-05 17:00:00', 1);
