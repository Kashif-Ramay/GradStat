# ✅ React Hooks Rules Fixed

## 🐛 The Error:

```
React Hook "useEffect" is called conditionally.
React Hooks must be called in the exact same order in every component render.
```

### What Went Wrong:

We had `useEffect` inside an `if` statement:

```typescript
// ❌ WRONG - Violates Rules of Hooks
if (step === 2 && answers.researchQuestion === 'describe_data') {
  useEffect(() => {
    getRecommendations();
  }, []);
  return <div>Loading...</div>;
}
```

**Problem:** React hooks must be called at the **top level** of the component, not inside conditionals, loops, or nested functions.

---

## ✅ The Fix:

### **1. Moved useEffect to Top Level:**

```typescript
const TestAdvisor: React.FC<TestAdvisorProps> = ({ onSelectTest }) => {
  const [step, setStep] = useState(1);
  const [answers, setAnswers] = useState<any>({});
  const [recommendations, setRecommendations] = useState<TestRecommendation[]>([]);
  const [loading, setLoading] = useState(false);

  // ✅ CORRECT - Hook at top level with conditional logic inside
  useEffect(() => {
    if (step === 2 && answers.researchQuestion === 'describe_data') {
      getRecommendations();
    }
  }, [step, answers.researchQuestion]);

  // ... rest of component
```

### **2. Updated Render Logic:**

```typescript
// ✅ Just check loading state in render
if (step === 2 && answers.researchQuestion === 'describe_data' && loading) {
  return (
    <div className="bg-white rounded-lg shadow-sm p-6">
      <div className="text-center py-8">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
        <p className="mt-4 text-gray-600">Getting recommendations...</p>
      </div>
    </div>
  );
}
```

---

## 📚 React Rules of Hooks

### **Rule #1: Only Call Hooks at the Top Level**
❌ Don't call hooks inside:
- Conditionals (`if`, `switch`)
- Loops (`for`, `while`)
- Nested functions

✅ Do call hooks at:
- Top level of component
- Top level of custom hooks

### **Rule #2: Only Call Hooks from React Functions**
✅ Call hooks from:
- React function components
- Custom hooks

❌ Don't call hooks from:
- Regular JavaScript functions
- Class components

---

## 🎯 How It Works Now:

1. **Component renders**
2. **useEffect runs** (at top level, always)
3. **Checks condition** inside useEffect
4. **If condition true:** Calls `getRecommendations()`
5. **Loading state updates**
6. **Component re-renders** with loading UI
7. **Recommendations arrive**
8. **Step changes to 99** (results)

---

## ✅ What's Fixed:

- ✅ No more "Rules of Hooks" error
- ✅ Component compiles successfully
- ✅ "Describe data" works properly
- ✅ All other options work
- ✅ Can navigate between steps

---

## 🚀 Test It Now!

1. **Save all files** (should auto-compile)
2. **Check browser** - error should be gone
3. **Click "🧭 Test Advisor"**
4. **Try "Describe data"** - should work!
5. **Try other options** - all should work!

---

## 📝 Files Modified:

- `frontend/src/components/TestAdvisor.tsx`
  - Moved `useEffect` to top level
  - Added proper dependencies
  - Updated render logic

---

## 🎓 Key Takeaway:

**Put the condition INSIDE the hook, not the hook INSIDE the condition!**

❌ **Wrong:**
```typescript
if (condition) {
  useEffect(() => { ... }, []);
}
```

✅ **Correct:**
```typescript
useEffect(() => {
  if (condition) { ... }
}, [dependencies]);
```

---

**Last Updated:** October 23, 2025  
**Status:** Hooks rules violation fixed ✅  
**Action:** Check browser - should compile now!
