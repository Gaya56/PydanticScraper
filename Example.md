
# Example: Search for NBA Games Today

Here's exactly where to make changes for NBA games today:

## 🏀 **Search for NBA Games Today - Step by Step:**

### **Option 1: Quick Change (Easiest)**
**File:** `app.py`  
**Line:** ~25 (the prompt section)

```python
# Change this line:
"Research and compile recent climate change statistics..."

# To this:
"Find NBA games being played today with times, teams, and TV schedules"
```

### **Option 2: Better Search Results** 
**File:** `brave_search.py`  
**Line:** ~23

```python
# Add this for better sports results:
"include_domains": ["espn.com", "nba.com", "yahoo.com"]
```

### **Option 3: Fresh Results Only**
**File:** `brave_search.py`  
**Line:** ~24

```python
# Add this line:
"freshness": "pd",  # Past day only
```

## **Complete Steps:**
1. Edit `app.py` line 25 → Change the AI task
2. *(Optional)* Edit `brave_search.py` line 23 → Add sports domains  
3. *(Optional)* Edit `brave_search.py` line 24 → Add freshness filter
4. Run: `python3 app.py`

**Result:** AI will search for today's NBA games and compile schedules, times, and broadcast info! 🏀
