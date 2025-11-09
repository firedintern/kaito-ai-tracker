# 🌐 Vercel Deployment Guide

## 🎯 Goal
Deploy your Kaito AI Agents Tracker to the web with a custom domain!

## 📋 Prerequisites
- ✅ GitHub account
- ✅ Vercel account (free!)
- ✅ Generated `dashboard.html` file

---

## 🚀 Method 1: Quick Deploy (Recommended)

### Step 1: Push to GitHub

```bash
cd ~/Desktop/kaito-tracker

# Initialize git (if not done yet)
git init

# Add files
git add .gitignore
git add fetch_all_projects.py
git add generate_dashboard_degen.py
git add projects_database.json
git add config_template.py
git add README.md
git add vercel.json
git add dashboard.html

# Commit
git commit -m "Initial commit: Kaito AI Agents Tracker 🚀"

# Add your GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/kaito-ai-tracker.git

# Push
git push -u origin main
```

### Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **"Add New..."** → **"Project"**
3. **Import Git Repository**
   - Select your `kaito-ai-tracker` repo
   - Click **"Import"**

4. **Configure Project**
   - **Framework Preset:** Other
   - **Root Directory:** `./`
   - **Build Command:** (leave empty)
   - **Output Directory:** (leave empty)
   - Click **"Deploy"**

5. **Wait for deployment** (~30 seconds)

6. **Your site is live!** 🎉
   - URL: `https://kaito-ai-tracker.vercel.app`
   - Or your custom domain!

---

## 🌐 Method 2: Buy Domain on Vercel

Since you've done this before with Fear & Greed Index:

### Step 1: Deploy (same as above)

### Step 2: Add Custom Domain

1. Go to your project in Vercel
2. Click **"Settings"** → **"Domains"**
3. Click **"Buy a domain"**
   - Search for your desired domain (e.g., `kaito-tracker.com`)
   - Vercel will show prices (~$15-20/year)
   - Complete purchase

4. **Domain auto-configures!**
   - Vercel handles DNS automatically
   - SSL certificate included (HTTPS)
   - Live in ~2 minutes

### Alternative: Use Existing Domain

If you already own a domain:
1. Go to **"Settings"** → **"Domains"**
2. Click **"Add"**
3. Enter your domain
4. Follow DNS configuration instructions
5. Wait for DNS propagation (~5-30 mins)

---

## 🔄 Updating Your Dashboard

### Option A: Manual Updates (Simple)

```bash
# 1. Update data locally
cd ~/Desktop/kaito-tracker
python3 fetch_all_projects.py
python3 generate_dashboard_degen.py

# 2. Push to GitHub
git add dashboard.html
git commit -m "Update: latest prices $(date +%Y-%m-%d)"
git push

# 3. Vercel auto-deploys! ✨
# Your site updates in ~30 seconds
```

### Option B: Scheduled Updates (Advanced)

Use GitHub Actions to auto-update daily:

1. Add secrets to GitHub repo:
   - Go to repo **"Settings"** → **"Secrets and variables"** → **"Actions"**
   - Click **"New repository secret"**
   - Name: `CMC_API_KEY`
   - Value: Your CoinMarketCap API key

2. Create `.github/workflows/update-dashboard.yml`:
```yaml
name: Update Dashboard

on:
  schedule:
    - cron: '0 0 * * *'  # Daily at midnight UTC
  workflow_dispatch:  # Manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install requests
      
      - name: Create config
        run: |
          echo "CMC_API_KEY = '${{ secrets.CMC_API_KEY }}'" > config.py
      
      - name: Fetch data
        run: python3 fetch_all_projects.py
      
      - name: Generate dashboard
        run: python3 generate_dashboard_degen.py
      
      - name: Commit and push
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add dashboard.html tracker_results_latest.json
          git commit -m "Auto-update: $(date +%Y-%m-%d)" || exit 0
          git push
```

3. **Done!** Dashboard updates automatically every day! 🎉

---

## 📊 Vercel Analytics (Optional)

Add free analytics to track visitors:

1. Go to your project in Vercel
2. Click **"Analytics"**
3. Click **"Enable Analytics"**
4. Free tier includes:
   - Page views
   - Unique visitors
   - Top pages
   - Device stats

---

## 🎨 Custom Domains Examples

**Option 1: Short & Catchy**
- `kaito-tracker.com` 💎
- `aiagents.watch` 🔥
- `tge-tracker.xyz` 🚀

**Option 2: Branded**
- `your-name-kaito.com`
- `degen-ai-tracker.com`

**Option 3: Fun/Meme**
- `aiape.com` 🦍
- `chad-ai.com` 💪
- `gm-ai.xyz` ☀️

---

## ✅ Deployment Checklist

Before deploying:
- [ ] Run `generate_dashboard_degen.py` to create latest `dashboard.html`
- [ ] Test locally at `localhost:3000/dashboard.html`
- [ ] Verify no API keys in code
- [ ] Check `.gitignore` is working
- [ ] Add screenshot to README
- [ ] Update README with your GitHub username
- [ ] Push to GitHub
- [ ] Deploy to Vercel
- [ ] Test live site
- [ ] Add custom domain (optional)
- [ ] Share with the world! 🌐

---

## 🔒 Security Checklist

- [ ] `config.py` is in `.gitignore`
- [ ] Never commit API keys
- [ ] Only `config_template.py` in repo
- [ ] Dashboard has no sensitive data
- [ ] GitHub secrets configured (if using Actions)

---

## 💡 Pro Tips

1. **Update regularly** - Fresh data = more viewers
2. **Share on Twitter** - Tag the projects you're tracking
3. **Add more tokens** - More data = more valuable
4. **Monitor analytics** - See what people like
5. **Iterate the design** - Make it yours!

---

## 🆘 Troubleshooting

**"Deployment failed"**
- Check vercel.json is valid
- Make sure dashboard.html exists
- Check Vercel build logs

**"Site shows old data"**
- Regenerate dashboard locally
- Push new dashboard.html to GitHub
- Vercel auto-deploys on push

**"Domain not working"**
- Wait 5-30 mins for DNS propagation
- Check domain configuration in Vercel
- Try incognito mode (clear cache)

---

## 🎉 Success!

Your Kaito AI Agents Tracker is now live on the internet! 

**Next steps:**
1. Share your URL on Twitter
2. Add more tokens
3. Get feedback from the community
4. Iterate and improve

**WAGMI** 🚀 **LFG** 🔥

---

Need help? Open an issue on GitHub!
