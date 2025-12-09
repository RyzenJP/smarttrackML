# 🚀 Deploy Updated ML Server to Heroku

## ✅ Yes! Upload the Updated `ml_models` Folder

You need to upload the updated `ml_models` folder to Heroku so the new database connection code is deployed.

---

## 📋 Files to Upload

Upload these files from `trackingv2/ml_models/` to your Heroku app:

### **Required Files:**
- ✅ `ml_server.py` - **Updated with production database defaults**
- ✅ `Procfile` - Tells Heroku how to run the app
- ✅ `requirements.txt` - Python dependencies
- ✅ `runtime.txt` - Python version

### **Optional Files (if you have them):**
- `maintenance_model.pkl` - Trained model (if exists)
- `maintenance_scaler.pkl` - Model scaler (if exists)
- `training_stats.json` - Training statistics (if exists)

### **Files to EXCLUDE (don't upload):**
- ❌ `__pycache__/` - Python cache (auto-generated)
- ❌ `*.log` - Log files
- ❌ `*.sql` - SQL files (not needed)
- ❌ `generate_synthetic_data.py` - Not needed on Heroku
- ❌ `seed_synthetic.py` - Not needed on Heroku
- ❌ `update_mileage.py` - Not needed on Heroku

---

## 🔧 Deployment Methods

### **Method 1: Via Heroku CLI (Recommended)**

If you have Heroku CLI installed:

```bash
# Navigate to ml_models folder
cd trackingv2/ml_models

# Login to Heroku (if not already)
heroku login

# Set Heroku remote (if not already set)
heroku git:remote -a endpoint-smarttrack-ec777ab9bb50

# Add and commit files
git init  # If not already a git repo
git add ml_server.py Procfile requirements.txt runtime.txt
git commit -m "Update database connection with production defaults"

# Deploy to Heroku
git push heroku main
# OR if your branch is master:
git push heroku master
```

---

### **Method 2: Via Heroku Dashboard (GitHub Integration)

1. **Push to GitHub:**
   ```bash
   cd trackingv2/ml_models
   git init
   git add ml_server.py Procfile requirements.txt runtime.txt
   git commit -m "Update database connection"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Connect Heroku to GitHub:**
   - Go to: https://dashboard.heroku.com/apps/endpoint-smarttrack-ec777ab9bb50/deploy
   - Click "GitHub" tab
   - Connect your repository
   - Enable "Automatic deploys" (optional)
   - Click "Deploy Branch"

---

### **Method 3: Via Heroku Dashboard (Manual Upload)

**Note:** Heroku doesn't support direct file upload. You need to use Git.

**Alternative:** Use Heroku CLI or GitHub integration (Methods 1 or 2).

---

## ✅ After Deployment

### 1. **Check Deployment Status:**
```bash
heroku logs --tail -a endpoint-smarttrack-ec777ab9bb50
```

Or via Dashboard: "More" → "View logs"

### 2. **Test Status Endpoint:**
```
https://endpoint-smarttrack-ec777ab9bb50.herokuapp.com/status
```

Should return JSON with server status.

### 3. **Test Training:**
```
POST https://endpoint-smarttrack-ec777ab9bb50.herokuapp.com/train
```

Or via your PHP bridge:
```
https://smarttrack.bccbsis.com/trackingv2/trackingv2/api/python_ml_bridge.php?action=train
```

---

## 🔍 Verify Files Are Updated

After deployment, check that the updated code is live:

1. **Check Heroku Logs:**
   ```bash
   heroku logs --tail -a endpoint-smarttrack-ec777ab9bb50
   ```

2. **Look for:**
   - `[SERVER] Smart Track ML Server starting...`
   - No database connection errors
   - Server running on port (Heroku assigns automatically)

---

## ⚠️ Important Notes

1. **Database Host:** The updated code uses `localhost` as default. If your Hostinger database uses a different host, you still need to set `DB_HOST` environment variable in Heroku.

2. **Remote MySQL:** Make sure Hostinger allows external MySQL connections from Heroku's IP addresses.

3. **Restart After Deploy:** Heroku should auto-restart, but you can manually restart:
   ```bash
   heroku restart -a endpoint-smarttrack-ec777ab9bb50
   ```

---

## 🐛 Troubleshooting

### Issue: "Can't connect to MySQL server"
- Check if Hostinger allows remote MySQL connections
- Verify database host is correct (might not be `localhost`)
- Set environment variables in Heroku if needed

### Issue: "Module not found"
- Check `requirements.txt` has all dependencies
- Heroku will auto-install on deploy

### Issue: "Application error"
- Check Heroku logs: `heroku logs --tail`
- Verify `Procfile` is correct
- Check `runtime.txt` Python version is supported

---

## ✅ Quick Checklist

- [ ] Updated `ml_server.py` with production database defaults
- [ ] `Procfile` exists and is correct
- [ ] `requirements.txt` has all dependencies
- [ ] `runtime.txt` specifies Python version
- [ ] Files committed to Git
- [ ] Pushed to Heroku (or GitHub)
- [ ] Heroku app restarted
- [ ] Tested status endpoint
- [ ] Tested training endpoint

---

*Last Updated: 2025-01-27*


