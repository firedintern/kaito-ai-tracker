# Kaito AI Agents Tracker [Update 2026: Kaito platform has been deprecated]

**Post-TGE token performance tracker for Kaito-listed AI agent projects**

Track real-time prices, market caps, and all-time ROI for AI agent tokens with a beautiful degen-themed dashboard.

## Features

- 🎯 **Live Price Tracking** - Real-time data from CoinMarketCap
- 💎 **All-Time ROI Calculation** - Track performance since TGE
- 🚀 **Degen Dashboard** - Beautiful, animated UI with crypto vibes
- 📊 **Performance Metrics** - 24h, 7d, 30d price changes
- 🔥 **Easy to Update** - Add new tokens in seconds

## Live Demo

https://kaito-ai-tracker.vercel.app/

## Quick Start

### Prerequisites

- Python 3.7+
- CoinMarketCap API key (free tier: [Get it here](https://coinmarketcap.com/api/))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/kaito-ai-tracker.git
cd kaito-ai-tracker
```

2. **Set up your API key**
```bash
cp config_template.py config.py
# Edit config.py and add your CoinMarketCap API key
```

3. **Run the tracker**
```bash
# Fetch latest data
python3 fetch_all_projects.py

# Generate dashboard
python3 generate_dashboard_degen.py

# Start local server
python3 -m http.server 3000
```

4. **View dashboard**
Open `http://localhost:3000/dashboard.html` in your browser

## 📊 Adding New Tokens

Edit `projects_database.json`:

```json
{
  "name": "New Project",
  "twitter": "@NewProject",
  "token_symbol": "NEW",
  "tge_date": "2025-11-01",
  "tge_price": 0.15,
  "category": "AI Agents"
}
```

Then run the tracker again!

## Deploy to Vercel

### Option 1: Manual Deploy (Easiest)

1. Run locally to generate `dashboard.html`
2. Go to [Vercel](https://vercel.com)
3. Click "Add New" → "Project"
4. Import your GitHub repo
5. Set Framework Preset to "Other"
6. Deploy!

### Option 2: Auto-Deploy with GitHub Actions

Coming soon! 🚧

## 📁 Project Structure

```
kaito-ai-tracker/
├── fetch_all_projects.py       # Data collector
├── generate_dashboard_degen.py # Dashboard generator
├── projects_database.json      # Your projects & TGE prices
├── config_template.py          # API key template
├── config.py                   # Your API key (gitignored)
├── .gitignore                  # Protects your secrets
└── dashboard.html              # Generated dashboard
```

## Security

- ✅ API keys are **never** committed to GitHub
- ✅ `config.py` is in `.gitignore`
- ✅ Only push template files
- ✅ Dashboard contains no sensitive data

## Tech Stack

- **Python 3** - Data collection
- **CoinMarketCap API** - Real-time prices
- **Vanilla HTML/CSS/JS** - No dependencies!
- **Vercel** - Hosting (optional)

## Current Tokens

- **Virtuals Protocol** ($VIRTUAL) - +13,424% ROI 🔥
- **INFINIT** ($IN) - +82% ROI
- **Newton** ($NEWT)
- **Creator Bid** ($BID)
- **Wayfinder** ($PROMPT)

## Contributing

Want to add more features? PRs welcome!

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a PR

## License

MIT License - feel free to use this for your own projects!

## ⚠️ Disclaimer

**NFA - Not Financial Advice!**

This tool is for educational and informational purposes only. Always DYOR.

---
