# 🚀 Deploy AI Features - Step-by-Step Guide

## Quick Overview
This guide will help you deploy the AI Statistical Interpreter to your GradStat application, both locally and on Render.com.

---

## 📋 Prerequisites

- ✅ OpenAI account (sign up at https://platform.openai.com)
- ✅ OpenAI API key
- ✅ Git installed
- ✅ Node.js 18+ installed
- ✅ Python 3.13+ installed

---

## 🔑 Step 1: Get OpenAI API Key

### 1.1 Create OpenAI Account
1. Go to: https://platform.openai.com
2. Click "Sign up" (or "Log in" if you have account)
3. Complete registration

### 1.2 Get API Key
1. Go to: https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Give it a name: "GradStat AI Interpreter"
4. Click "Create secret key"
5. **IMPORTANT:** Copy the key immediately (starts with `sk-`)
6. Save it securely - you won't see it again!

### 1.3 Add Payment Method (Optional but Recommended)
1. Go to: https://platform.openai.com/settings/organization/billing
2. Add payment method
3. Set spending limit (e.g., $10/month)
4. You get $5 free credit to start!

**Cost estimate:** ~$0.001 per analysis, so $5 = ~5000 analyses

---

## 💻 Step 2: Local Development Setup

### 2.1 Install OpenAI Package

```bash
# Navigate to worker directory
cd worker

# Install OpenAI package
pip install openai>=1.0.0

# Verify installation
pip list | grep openai
```

### 2.2 Set Environment Variable

**Windows (PowerShell):**
```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

**Windows (CMD):**
```cmd
set OPENAI_API_KEY=sk-your-key-here
```

**Mac/Linux:**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

**Or create .env file in worker directory:**
```bash
# In worker/.env
OPENAI_API_KEY=sk-your-key-here
```

### 2.3 Test LLM Interpreter

```bash
# From project root
python test_llm_interpreter.py
```

**Expected output:**
```
============================================================
Testing LLM Statistical Interpreter
============================================================

✅ OpenAI API key found!
✅ Using model: gpt-4o-mini

============================================================
Test 1: Generate Interpretation
============================================================

📊 Interpretation:
Your independent samples t-test shows a statistically significant...

✅ Test 1 PASSED

============================================================
Test 2: Answer Question
============================================================

❓ Question: What does Cohen's d mean?

💬 Answer:
Cohen's d is a measure of effect size...

✅ Test 2 PASSED

============================================================
Test 3: What-If Scenario
============================================================

🔮 Scenario: What if I doubled my sample size?

🤖 Analysis:
Doubling your sample size from 45 to 90 would...

✅ Test 3 PASSED

============================================================
🎉 ALL TESTS PASSED!
============================================================
```

---

## 🏃 Step 3: Run Locally

### 3.1 Start Worker
```bash
cd worker
python main.py
```

**Expected output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8001
```

### 3.2 Start Backend (New Terminal)
```bash
cd backend
node server.js
```

**Expected output:**
```
Server running on port 3001
Worker URL: http://localhost:8001
```

### 3.3 Start Frontend (New Terminal)
```bash
cd frontend
npm start
```

**Expected output:**
```
Compiled successfully!
Local: http://localhost:3000
```

### 3.4 Test in Browser

1. Open: http://localhost:3000
2. Enter password: `GradStat2025!SecureTest`
3. Upload a CSV file
4. Run an analysis
5. Scroll down to see **🤖 AI Statistical Interpreter**
6. Test all 3 tabs:
   - 💡 Interpretation
   - 💬 Ask Questions
   - 🔮 What-If Scenarios

---

## ☁️ Step 4: Deploy to Render.com

### 4.1 Commit Changes

```bash
# From project root
git add .
git commit -m "Add AI Statistical Interpreter with GPT-4"
git push origin main
```

### 4.2 Update Worker Dependencies

Render will automatically install from `worker/requirements.txt` which now includes:
```
openai>=1.0.0
```

### 4.3 Add Environment Variable to Render

1. **Go to Render Dashboard:**
   - https://dashboard.render.com

2. **Select gradstat-worker service**

3. **Go to "Environment" tab**

4. **Add environment variable:**
   - Click "Add Environment Variable"
   - **Key:** `OPENAI_API_KEY`
   - **Value:** `sk-your-actual-key-here`
   - Click "Save Changes"

5. **Wait for automatic redeploy** (~3 minutes)

### 4.4 Verify Deployment

1. **Check Worker Logs:**
   - Go to worker service → Logs tab
   - Look for: "Application startup complete"
   - No errors about OpenAI

2. **Check Backend Logs:**
   - Go to backend service → Logs tab
   - Should show: "Server running on port 3001"

3. **Test Frontend:**
   - Open: https://gradstat-frontend.onrender.com
   - Enter password
   - Run an analysis
   - Check AI Interpreter appears

---

## 🧪 Step 5: Test All Features

### 5.1 Test Interpretation Tab

1. Run any analysis (t-test, ANOVA, regression, etc.)
2. Scroll to AI Interpreter section
3. Click "💡 Interpretation" tab
4. Should see:
   - Overall interpretation paragraph
   - Key findings list
   - Concerns (if any)
   - Next steps

**If you see error:**
- Check OPENAI_API_KEY is set in Render
- Check OpenAI account has credits
- Check worker logs for errors

### 5.2 Test Ask Questions Tab

1. Click "💬 Ask Questions" tab
2. Type a question: "What does this p-value mean?"
3. Click "Send" or press Enter
4. Should see AI response in chat bubble
5. Try suggested questions
6. Ask follow-up questions

### 5.3 Test What-If Scenarios Tab

1. Click "🔮 What-If Scenarios" tab
2. Click any scenario button
3. Should see scenario analysis
4. Try multiple scenarios
5. Responses should be contextual to your data

---

## 📊 Step 6: Monitor Usage & Costs

### 6.1 Check OpenAI Usage

1. Go to: https://platform.openai.com/usage
2. View API usage by day
3. See costs per request
4. Monitor total spending

### 6.2 Set Spending Limits

1. Go to: https://platform.openai.com/settings/organization/billing/limits
2. Set monthly budget cap (e.g., $10)
3. Set email alerts at 50%, 75%, 90%
4. OpenAI will stop API calls if limit reached

### 6.3 Expected Costs

**Per analysis:**
- Interpretation: ~$0.0006
- Question: ~$0.0003
- What-if: ~$0.0004
- **Total:** ~$0.001-0.002 per analysis

**Monthly estimates:**
- 100 analyses: ~$0.50-1.00
- 500 analyses: ~$2.50-5.00
- 1000 analyses: ~$5.00-10.00

---

## 🔧 Troubleshooting

### Problem: "LLM service not available"

**Cause:** OPENAI_API_KEY not set

**Fix:**
1. Check environment variable is set
2. Restart worker service
3. Verify key starts with `sk-`
4. Check key is valid in OpenAI dashboard

### Problem: "Rate limit exceeded"

**Cause:** Too many requests to OpenAI

**Fix:**
1. Wait a few minutes
2. Upgrade OpenAI plan
3. Add rate limiting to your app

### Problem: "Insufficient credits"

**Cause:** OpenAI account out of credits

**Fix:**
1. Add payment method
2. Add credits to account
3. Check billing page

### Problem: AI responses are slow

**Cause:** Normal - GPT-4 takes 2-5 seconds

**Fix:**
- This is expected behavior
- Loading spinner shows progress
- Consider using gpt-3.5-turbo for faster responses (change in llm_interpreter.py)

### Problem: Responses are generic/not helpful

**Cause:** Insufficient context being sent

**Fix:**
1. Check analysis_data includes all fields
2. Verify sample_size and variables are populated
3. Ensure results object has p_value, effect_size, etc.

---

## 🎨 Customization Options

### Change AI Model

Edit `worker/llm_interpreter.py`:

```python
# Line 20
self.model = "gpt-4o-mini"  # Current (cheap, fast)

# Options:
self.model = "gpt-4o"        # More capable, 10x cost
self.model = "gpt-3.5-turbo" # Cheaper, faster, less capable
```

### Adjust Response Length

Edit `worker/llm_interpreter.py`:

```python
# Line 88 (interpretation)
max_tokens=1000  # Current

# Options:
max_tokens=500   # Shorter responses
max_tokens=1500  # Longer responses
```

### Change Temperature (Creativity)

Edit `worker/llm_interpreter.py`:

```python
# Line 87 (interpretation)
temperature=0.7  # Current (balanced)

# Options:
temperature=0.3  # More conservative
temperature=0.9  # More creative
```

---

## 🔒 Security Best Practices

### 1. Protect API Key
- ✅ Never commit to Git
- ✅ Use environment variables
- ✅ Rotate key periodically
- ✅ Use separate keys for dev/prod

### 2. Monitor Usage
- ✅ Set spending limits
- ✅ Enable email alerts
- ✅ Review usage weekly
- ✅ Check for unusual patterns

### 3. Rate Limiting
Consider adding rate limits:

```javascript
// In backend/server.js
const aiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 50 // 50 AI requests per 15 min
});

app.post('/api/interpret', aiLimiter, async (req, res) => {
  // ... existing code
});
```

### 4. User Privacy
- ✅ Inform users data is sent to OpenAI
- ✅ Add privacy notice
- ✅ Don't send sensitive identifiers
- ✅ Consider data anonymization

---

## 📈 Next Steps

### Immediate:
1. ✅ Test locally
2. ✅ Deploy to Render
3. ✅ Verify all features work
4. ✅ Monitor initial usage

### Short-term:
- Add user feedback mechanism
- Collect usage analytics
- Optimize prompts based on feedback
- Add more suggested questions

### Long-term:
- Consider caching common questions
- Add streaming responses
- Implement conversation export
- Add multi-language support

---

## 🎉 Success Checklist

- [ ] OpenAI API key obtained
- [ ] Local testing passed
- [ ] Worker deployed with API key
- [ ] Backend proxy working
- [ ] Frontend component displays
- [ ] Interpretation tab works
- [ ] Chat tab works
- [ ] What-if tab works
- [ ] Error handling tested
- [ ] Usage monitoring set up
- [ ] Spending limits configured
- [ ] Documentation reviewed

---

## 📞 Support Resources

### OpenAI:
- Dashboard: https://platform.openai.com
- Documentation: https://platform.openai.com/docs
- API Status: https://status.openai.com
- Support: https://help.openai.com

### GradStat:
- Implementation docs: `AI_INTERPRETER_IMPLEMENTATION.md`
- Test script: `test_llm_interpreter.py`
- Worker code: `worker/llm_interpreter.py`
- Frontend code: `frontend/src/components/AIInterpreter.tsx`

---

## 🎓 Tips for Best Results

### 1. Provide Good Context
The more information you include in analysis_data, the better the AI responses:
- Sample size
- Variable names
- All statistical results
- Assumption checks

### 2. Ask Specific Questions
Instead of: "What does this mean?"
Try: "What does a p-value of 0.023 mean for my study?"

### 3. Use What-If for Planning
Great for:
- Sample size planning
- Power analysis
- Study design decisions
- Methodological choices

### 4. Iterate on Prompts
If responses aren't helpful:
- Rephrase your question
- Add more context
- Try different scenarios
- Use suggested questions

---

**You're all set! 🚀**

Your GradStat application now has AI-powered statistical interpretation that will help users understand their results better than ever before!
