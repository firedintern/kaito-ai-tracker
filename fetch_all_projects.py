#!/usr/bin/env python3
"""
Kaito-Listed AI Agents - Post-TGE Performance Tracker
Uses CoinMarketCap for current data + hardcoded TGE prices for ROI calculation
"""

import json
import requests
from datetime import datetime

# ========================================
# API KEY - Load from config file
# ========================================
try:
    from config import CMC_API_KEY
except ImportError:
    print("❌ Error: config.py not found!")
    print("   1. Copy config_template.py to config.py")
    print("   2. Add your CoinMarketCap API key to config.py")
    exit(1)

# ========================================
# API ENDPOINTS
# ========================================
CMC_BASE_URL = "https://pro-api.coinmarketcap.com/v2"


def load_projects():
    """Load projects from database (now includes TGE prices)"""
    with open('projects_database.json', 'r') as f:
        return json.load(f)


def get_current_prices_cmc(symbols):
    """Fetch current prices and market data from CoinMarketCap"""
    url = f"{CMC_BASE_URL}/cryptocurrency/quotes/latest"
    
    headers = {
        'X-CMC_PRO_API_KEY': CMC_API_KEY,
        'Accept': 'application/json'
    }
    
    params = {
        'symbol': ','.join(symbols),
        'convert': 'USD'
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"❌ Error fetching CMC data: {e}")
        return None


def calculate_days_since_tge(tge_date_str):
    """Calculate days since token generation event"""
    try:
        tge_date = datetime.strptime(tge_date_str, "%Y-%m-%d")
        today = datetime.now()
        delta = today - tge_date
        return delta.days
    except:
        return None


def fetch_all_data():
    """Main function to fetch all token data"""
    print("\n" + "="*70)
    print("🚀 KAITO-LISTED AI AGENTS - POST-TGE PERFORMANCE TRACKER")
    print("="*70)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"💡 Data: CoinMarketCap (current) + Manual TGE Prices (historical)")
    print("="*70 + "\n")
    
    # Load projects (now includes TGE prices!)
    projects = load_projects()
    print(f"📊 Tracking {len(projects)} Kaito-listed AI Agent projects...\n")
    
    # Prepare symbols for batch CMC request
    symbols = [p['token_symbol'] for p in projects]
    
    # Fetch current data from CoinMarketCap
    print("💰 Fetching current prices from CoinMarketCap...")
    cmc_data = get_current_prices_cmc(symbols)
    
    if not cmc_data or 'data' not in cmc_data:
        print("❌ Failed to fetch CMC data")
        return
    
    print("✅ Current prices fetched successfully!\n")
    
    # Process each project
    results = []
    
    for idx, project in enumerate(projects, 1):
        print(f"Project {idx}/{len(projects)}: {project['name']}")
        
        symbol = project['token_symbol']
        tge_date_str = project.get('tge_date')
        tge_price = project.get('tge_price')  # Get hardcoded TGE price
        
        # Get current data from CMC
        token_data = {}
        if symbol in cmc_data['data']:
            cmc_info = cmc_data['data'][symbol][0]  # CMC returns array
            quote = cmc_info['quote']['USD']
            
            token_data = {
                'current_price': quote['price'],
                'market_cap': quote['market_cap'],
                'volume_24h': quote['volume_24h'],
                'percent_change_24h': quote['percent_change_24h'],
                'percent_change_7d': quote['percent_change_7d'],
                'percent_change_30d': quote['percent_change_30d']
            }
            
            print(f"   ✅ Price: ${token_data['current_price']:.6f}")
            print(f"   ✅ Market Cap: ${token_data['market_cap']:,.0f}")
            print(f"   ✅ 24h Change: {token_data['percent_change_24h']:.2f}%")
        else:
            print(f"   ❌ Token ${symbol} not found on CoinMarketCap")
            continue
        
        # Calculate days since TGE
        days_since_tge = None
        if tge_date_str:
            days_since_tge = calculate_days_since_tge(tge_date_str)
            if days_since_tge:
                print(f"   📅 Days since TGE: {days_since_tge} days")
        
        # Calculate All-Time ROI using hardcoded TGE price
        all_time_roi = None
        
        if tge_price:
            current_price = token_data['current_price']
            all_time_roi = ((current_price - tge_price) / tge_price) * 100
            
            print(f"   💵 TGE Price: ${tge_price:.6f}")
            print(f"   📈 All-Time ROI: {all_time_roi:+.2f}%")
        else:
            print(f"   ⚠️  No TGE price available")
        
        # Compile result
        result = {
            'project_name': project['name'],
            'twitter': project['twitter'],
            'token_symbol': symbol,
            'tge_date': tge_date_str,
            'days_since_tge': days_since_tge,
            'tge_price': tge_price,
            'current_price': token_data['current_price'],
            'market_cap': token_data['market_cap'],
            'volume_24h': token_data['volume_24h'],
            'percent_change_24h': token_data['percent_change_24h'],
            'percent_change_7d': token_data['percent_change_7d'],
            'percent_change_30d': token_data['percent_change_30d'],
            'all_time_roi': all_time_roi,
            'timestamp': datetime.now().isoformat()
        }
        
        results.append(result)
        print()  # Blank line between projects
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"tracker_results_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump({
            'metadata': {
                'timestamp': datetime.now().isoformat(),
                'total_projects': len(results),
                'data_sources': ['CoinMarketCap', 'Manual TGE Prices']
            },
            'projects': results
        }, f, indent=2)
    
    print("="*70)
    print("✅ DATA COLLECTION COMPLETE!")
    print(f"📁 Results saved to: {filename}")
    print("="*70 + "\n")
    
    # Print summary
    print("💹 Performance Summary:")
    if results:
        total_mcap = sum(r['market_cap'] for r in results if r['market_cap'])
        best_24h = max(results, key=lambda x: x['percent_change_24h'])
        worst_24h = min(results, key=lambda x: x['percent_change_24h'])
        
        print(f"   💰 Total Market Cap: ${total_mcap/1e6:.1f}M")
        print(f"   🏆 Best 24h: {best_24h['project_name']} ({best_24h['percent_change_24h']:+.2f}%)")
        print(f"   📉 Worst 24h: {worst_24h['project_name']} ({worst_24h['percent_change_24h']:+.2f}%)")
        
        # All-time ROI summary
        roi_results = [r for r in results if r['all_time_roi'] is not None]
        if roi_results:
            best_roi = max(roi_results, key=lambda x: x['all_time_roi'])
            worst_roi = min(roi_results, key=lambda x: x['all_time_roi'])
            avg_roi = sum(r['all_time_roi'] for r in roi_results) / len(roi_results)
            
            print(f"\n   🚀 Best All-Time ROI: {best_roi['project_name']} ({best_roi['all_time_roi']:+.2f}%)")
            print(f"   📊 Worst All-Time ROI: {worst_roi['project_name']} ({worst_roi['all_time_roi']:+.2f}%)")
            print(f"   📈 Average ROI: {avg_roi:+.2f}%")
    
    print("\n🎯 Next step: Copy results to dashboard")
    print(f"   Run: cp {filename} tracker_results_latest.json")
    print()


if __name__ == "__main__":
    fetch_all_data()
