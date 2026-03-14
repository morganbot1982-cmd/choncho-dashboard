# Health & Fitness Agent

## Overview
A dedicated sub-agent that helps Morgan track daily food intake, personal spending, and build sustainable movement habits. Focuses on awareness and gentle accountability rather than restrictive rules.

## Core Features

### 1. Food & Calorie Tracking
**Goal:** Awareness of what and how much you're eating daily

**How it works:**
- Send food photos to WhatsApp/Telegram whenever you eat
- Agent analyzes photo → estimates calories, macros, and food type
- Logs entry to daily tracker
- Provides daily/weekly summary without judgment

**Tech stack:**
- Image analysis via vision model (GPT-4V or Claude with vision)
- Simple CSV/JSON storage or Google Sheets for tracking
- Optional integration with MyFitnessPal API if needed

### 2. Personal Spending Tracker
**Goal:** Budget awareness for personal expenses

**How it works:**
- Text message: "Spent $45 coffee and lunch"
- Agent logs amount, category (auto-inferred or prompted)
- Weekly spending summary
- Optional budget alerts when approaching limits

**Storage:**
- CSV/JSON or Google Sheets
- Could integrate with Xero personal account later

### 3. Movement & Exercise Builder
**Goal:** Build sustainable daily movement habits starting small

**Phase 1 - Foundation (Weeks 1-4):**
- 10 pushups, 3x/day (morning, midday, evening)
- Water reminders every 2 hours during work
- 5-minute walk after lunch

**Phase 2 - Expansion (Weeks 5-8):**
- Add: 20 squats, 2x/day
- Add: 10-minute morning stretch routine
- Increase: 15 pushups per session

**Phase 3 - Routine (Weeks 9-12):**
- Full 20-minute morning routine
- Midday movement break (5 min)
- Evening wind-down stretch

**Tech stack:**
- Scheduled reminders via messaging (cron jobs)
- Check-in system: reply "done" to log completion
- Weekly progress report

### 4. Gentle Accountability
**Principles:**
- No shame, just data
- Celebrate streaks, don't punish breaks
- Focus on building habits, not perfection
- Adjust based on what's working

**Examples:**
- "3-day streak of morning pushups! 💪"
- "Noticed you haven't logged food today - everything okay?"
- "You've been sitting for 3 hours - time for a quick movement break?"

## Baseline Health Assessment

**Goal:** Establish current health status to set realistic goals and track meaningful progress

### Initial Data Collection

**1. GP Health Check** ✅ **COMPLETED**

**Appointment Details:**
- **Date:** Thursday, February 26, 2026
- **Time:** 11:15 AM (completed)
- **Doctor:** Dr Glenn Clifford | GP, Men's Health & Preventative Medicine
- **Clinic:** One Health Clinics Albion - Medical Centre
- **Location:** Albion Central, 6 Crosby Rd, Albion, QLD 4010

**Outcome: 3 Specialist Referrals + Blood Work**

See [Bookings Tracker](./bookings/BOOKINGS-TRACKER.md) for full details.

**Referrals Issued:**
1. **Cardiology** - Dr Andrew Rainbird (Advara HeartCare)
   - ✅ Booked: Monday 9th March, 1:55 PM, Milton
   - Tests: Exercise Stress Echo, Calcium Score, CT Coronary Angiogram
   
2. **Gastroenterology** - A/Prof Daniel Worthley
   - ⏳ Pending: Email form to complete (colonoscopy clinic called)
   - Test: Gastroscopy
   
3. **ENT Specialist** - Dr Jo-Lyn McKenzie
   - 📞 Pending: Need to call to book (07 3053 3833)
   - Reason: Enlarged tonsils, possible tonsillectomy

**Blood Work - 4Cyte Pathology:**
- ⏳ To do: Walk-in (fasting required)
- Tests: FBC, lipids, HbA1c, thyroid, iron, STI screen, etc.
- Contact: 13 42 98

**All referral documents:** See `referrals/` folder

**2. Self-Measured Baseline Metrics**
- **Weight:** Current weight (weigh same time each week, e.g., Monday morning)
- **Body measurements:** Waist, hips, chest, arms (optional but useful)
- **Photos:** Front, side, back (private, for your own progress tracking)
- **Activity level:** Current daily steps average (from phone)
- **Sleep:** Average hours per night
- **Energy levels:** Rate 1-10 throughout typical day

**3. Current Habits Assessment**
- **Food:** What do you typically eat? How often? Portion sizes?
- **Movement:** Current exercise (if any)? Sitting time per day?
- **Water intake:** How much water daily? (estimate cups/litres)
- **Stress:** Work stress, sleep quality, mental health baseline

**4. Calculate Starting Numbers**
- **TDEE (Total Daily Energy Expenditure):** Use online calculator based on age, weight, height, activity level
- **Current calorie intake estimate:** Track for 3-5 days to get average (before making changes)
- **Baseline step count:** Average daily steps from last week

### Goal Setting Framework

Based on baseline, set **realistic, sustainable goals:**

**Weight Loss Example:**
- Current: 95kg, want to reach: 85kg
- Healthy rate: 0.5-1kg per week
- Timeline: 10-20 weeks (2.5-5 months)
- Calorie deficit needed: ~500 calories/day below TDEE
- Track weekly, not daily (weight fluctuates)

**Fitness Example:**
- Current: Can't do 1 pushup
- Goal: 20 consecutive pushups
- Build: Start with wall/knee pushups, progress weekly
- Timeline: 8-12 weeks with consistent practice

**Energy/Wellbeing Example:**
- Current: Tired by 2pm daily, poor sleep
- Goal: Sustained energy throughout day
- Focus: Regular movement breaks, better hydration, earlier bedtime
- Measure: Daily energy rating (1-10)

### Agent Personalization

Once baseline is established, the agent will:
- **Tailor calorie targets** based on TDEE and goals
- **Adjust portion feedback** ("that looks like ~600 cal, about right for lunch")
- **Progressive exercise** (start where you can actually succeed)
- **Celebrate meaningful progress** ("Down 2kg this month! 🎉")
- **Flag concerns** ("Haven't logged food in 3 days, everything ok?")

### Baseline Data Storage

Create `health-data/baseline.json`:
```json
{
  "assessmentDate": "2026-02-23",
  "current": {
    "weight": 95,
    "height": 180,
    "age": 32,
    "waist": 98,
    "activityLevel": "sedentary",
    "averageSteps": 4500,
    "sleepHours": 6.5
  },
  "gpCheckup": {
    "date": "2026-03-01",
    "bloodPressure": "130/85",
    "cholesterol": "normal",
    "notes": "All clear, GP recommends gradual increase in activity"
  },
  "goals": {
    "targetWeight": 85,
    "targetWaist": 88,
    "targetSteps": 8000,
    "targetSleep": 7.5,
    "timeline": "6 months"
  },
  "tdee": 2400,
  "targetCalories": 1900,
  "deficitPerDay": 500
}
```

## Implementation Plan

### Phase 0: Baseline Assessment (Week 0)
- [x] Book GP appointment for health checkup (Thu Feb 26, 11:15 AM)
- [x] Attend GP appointment and receive referrals (completed Feb 26)
- [x] Book specialist appointments (1/3 booked, 2 pending)
- [ ] Complete gastro email form (colonoscopy clinic) ⚠️
- [ ] Book ENT appointment (call 07 3053 3833)
- [ ] Complete blood work (4Cyte walk-in, fasting)
- [ ] Measure and record current weight, measurements
- [ ] Take baseline photos (private storage)
- [ ] Track food for 3-5 days to estimate current intake
- [ ] Calculate TDEE using online calculator
- [ ] Set realistic weight/fitness/energy goals
- [ ] Create `health-data/baseline.json` with all metrics

### Phase 1: Food Tracking (Week 1)
- [ ] Set up WhatsApp/Telegram message handler for photos
- [ ] Implement image analysis → calorie estimation
- [ ] Create simple daily log (CSV or Google Sheet)
- [ ] Test with a few days of real data
- [ ] Build daily summary message (evening recap)

### Phase 2: Spending Tracker (Week 2)
- [ ] Parse text messages for spending ("spent $X on Y")
- [ ] Auto-categorize common purchases
- [ ] Add to daily log
- [ ] Weekly spending summary

### Phase 3: Movement Reminders (Week 3)
- [ ] Set up cron jobs for scheduled reminders
- [ ] Start with: water (every 2h), pushups (3x/day)
- [ ] Build check-in system (reply to confirm)
- [ ] Track completion streaks

### Phase 4: Dashboard Integration (Week 4)
- [ ] Add health metrics to main dashboard
- [ ] Show: today's calories, spending, movement streaks
- [ ] Weekly trends chart
- [ ] Quick stats (7-day average, longest streak, etc.)

### Phase 5: Refinement (Ongoing)
- [ ] Adjust reminder timing based on actual completion patterns
- [ ] Add new movements gradually based on progress
- [ ] Improve calorie estimation accuracy
- [ ] Build out exercise library for variety

## Sub-Agent Architecture

**Name:** HealthBot / FitBot / WellnessAgent (TBD)

**Session:** Isolated sub-agent (not main session)

**Triggers:**
- Photo message → analyze food, log calories
- Text message with "spent" → log spending
- Scheduled cron → send movement reminders
- Evening cron → daily summary

**Storage:**
- `health-data/food-log.csv` - daily food entries
- `health-data/spending-log.csv` - personal expenses
- `health-data/movement-log.csv` - exercise check-ins
- `health-data/stats.json` - streaks, totals, averages

**Messaging:**
- WhatsApp or Telegram (whichever is more reliable)
- Gentle, encouraging tone
- Emojis for celebrations: 💪 🔥 ✅ 💧

## Success Metrics

**Week 4:**
- Food logged 5+ days/week
- Movement reminders responded to 60%+ of the time
- Spending tracked (any amount of data = success)

**Week 8:**
- 7-day streak of morning pushups
- Water intake 6+ times/day consistently
- Calorie awareness (not restriction, just awareness)

**Week 12:**
- Full 20-minute morning routine established
- Personal spending tracked and categorized
- Movement breaks integrated into work flow

## Notes

- **Baseline first:** GP health check + measurements before starting (know your starting point)
- **Realistic goals:** Based on actual data, not wishful thinking (0.5-1kg/week is healthy)
- **Start slow:** Better to do 10 pushups daily than plan 100 and do none
- **Personalized:** Calorie targets and exercise progression based on YOUR baseline
- **Flexibility:** Reminders should adapt to your actual schedule
- **No guilt:** Missing a day doesn't break the streak, 2+ days prompts a gentle check-in
- **Privacy:** All health data stays local or in your controlled storage
- **Track trends:** Weekly averages matter more than daily fluctuations
- **Integration:** Could eventually feed data to Apple Health if you want

## Open Questions

1. **Messaging platform:** WhatsApp or Telegram? (whichever is more stable)
2. **Storage:** Local CSV vs Google Sheets vs database?
3. **Calorie goals:** Track only, or set daily targets?
4. **Reminder timing:** Fixed schedule or adapt to your patterns?
5. **Dashboard design:** Simple text stats or charts/graphs?

---

**Status:** Planning  
**Priority:** Medium (after Xero cleanup, alongside ecommerce JV)  
**Effort:** 2-3 weeks for MVP (all phases)  
**Blockers:** Need reliable messaging channel (WhatsApp/Telegram)
