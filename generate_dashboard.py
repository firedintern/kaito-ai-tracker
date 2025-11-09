#!/usr/bin/env python3
"""
Generate DEGEN dashboard with embedded JSON data
Run this after fetch_all_projects.py
"""

import json
from datetime import datetime

def generate_dashboard():
    # Load the JSON data
    try:
        with open('tracker_results_latest.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("❌ Error: tracker_results_latest.json not found!")
        print("   Run fetch_all_projects.py first.")
        return
    
    projects = data['projects']
    
    # Calculate stats
    total_projects = len(projects)
    total_mcap = sum(p['market_cap'] for p in projects if p.get('market_cap'))
    
    best_24h = max(projects, key=lambda x: x.get('percent_change_24h', -float('inf')))
    best_24h_change = best_24h.get('percent_change_24h', 0)
    
    # Calculate best all-time ROI
    roi_projects = [p for p in projects if p.get('all_time_roi') is not None]
    if roi_projects:
        best_roi = max(roi_projects, key=lambda x: x['all_time_roi'])
        best_roi_value = best_roi['all_time_roi']
        best_roi_name = best_roi['project_name']
    else:
        best_roi_value = 0
        best_roi_name = "N/A"
    
    valid_days = [p['days_since_tge'] for p in projects if p.get('days_since_tge')]
    avg_days = round(sum(valid_days) / len(valid_days)) if valid_days else 0
    
    # Format market cap
    if total_mcap >= 1e9:
        mcap_str = f"${total_mcap/1e9:.2f}B"
    elif total_mcap >= 1e6:
        mcap_str = f"${total_mcap/1e6:.2f}M"
    else:
        mcap_str = f"${total_mcap:.0f}"
    
    # Generate table rows
    rows_html = ""
    for p in projects:
        # Format price
        price = p.get('current_price', 0)
        if price < 0.01:
            price_str = f"${price:.6f}"
        elif price < 1:
            price_str = f"${price:.4f}"
        else:
            price_str = f"${price:.2f}"
        
        # Format market cap
        mcap = p.get('market_cap', 0)
        if mcap >= 1e9:
            mcap_str_row = f"${mcap/1e9:.2f}B"
        elif mcap >= 1e6:
            mcap_str_row = f"${mcap/1e6:.2f}M"
        else:
            mcap_str_row = f"${mcap:.0f}"
        
        # Format changes - cleaner style
        def format_change(val):
            if val is None:
                return 'N/A', ''
            sign = '+' if val >= 0 else ''
            color_class = 'moon' if val >= 0 else 'rekt'
            return f"{sign}{val:.2f}%", color_class
        
        roi_str, roi_class = format_change(p.get('all_time_roi'))
        # Add fire emoji only for massive gains (>1000%)
        if p.get('all_time_roi') and p.get('all_time_roi') > 1000:
            roi_str = f"🔥 {roi_str}"
        
        change_24h_str, change_24h_class = format_change(p.get('percent_change_24h'))
        change_7d_str, change_7d_class = format_change(p.get('percent_change_7d'))
        change_30d_str, change_30d_class = format_change(p.get('percent_change_30d'))
        
        days_str = f"{p.get('days_since_tge', 'N/A')} days" if p.get('days_since_tge') else 'N/A'
        
        rows_html += f"""
                    <tr>
                        <td><strong>{p['project_name']}</strong><br><small style="color:#1da1f2">{p['twitter']}</small></td>
                        <td><span class="token">${p['token_symbol']}</span></td>
                        <td>{price_str}</td>
                        <td>{mcap_str_row}</td>
                        <td class="{roi_class}">{roi_str}</td>
                        <td class="{change_24h_class}">{change_24h_str}</td>
                        <td class="{change_7d_class}">{change_7d_str}</td>
                        <td class="{change_30d_class}">{change_30d_str}</td>
                        <td>{days_str}</td>
                    </tr>
        """
    
    # Get timestamp
    timestamp = data['metadata'].get('timestamp', '')
    if timestamp:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        timestamp_str = dt.strftime('%Y-%m-%d %H:%M:%S')
    else:
        timestamp_str = 'Unknown'
    
    # Determine best ROI emoji
    roi_display_emoji = '🔥💎🚀' if best_roi_value > 1000 else '🚀' if best_roi_value > 100 else '📈'
    
    # Generate HTML with DEGEN theme
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kaito AI Agents Tracker</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Space Grotesk', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            padding: 40px 20px;
            min-height: 100vh;
            position: relative;
            overflow-x: hidden;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 20% 50%, rgba(0, 255, 127, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 80% 80%, rgba(255, 0, 255, 0.1) 0%, transparent 50%),
                radial-gradient(circle at 40% 20%, rgba(0, 191, 255, 0.1) 0%, transparent 50%);
            pointer-events: none;
            z-index: 0;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}
        
        .header {{
            text-align: center;
            color: white;
            margin-bottom: 40px;
            animation: fadeInDown 0.6s ease;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 700;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .header .subtitle {{
            font-size: 1.1em;
            opacity: 0.8;
            color: #9ca3af;
            letter-spacing: 1px;
            font-weight: 500;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
            animation: fadeInUp 0.6s ease 0.2s both;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 20px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            border-color: rgba(59, 130, 246, 0.4);
            box-shadow: 0 12px 40px rgba(59, 130, 246, 0.2);
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: 700;
            background: linear-gradient(90deg, #3b82f6, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}
        
        .stat-label {{
            color: rgba(255, 255, 255, 0.7);
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}
        
        .table-container {{
            background: rgba(255, 255, 255, 0.05);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(59, 130, 246, 0.2);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            overflow-x: auto;
            animation: fadeInUp 0.6s ease 0.4s both;
        }}
        
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        thead {{
            background: linear-gradient(90deg, rgba(59, 130, 246, 0.2), rgba(6, 182, 212, 0.2));
            border-bottom: 1px solid rgba(59, 130, 246, 0.3);
        }}
        
        th {{
            padding: 20px 15px;
            text-align: left;
            font-weight: 700;
            font-size: 0.9em;
            color: #60a5fa;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        td {{
            padding: 20px 15px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: white;
        }}
        
        tbody tr {{
            transition: all 0.2s ease;
        }}
        
        tbody tr:hover {{
            background: rgba(59, 130, 246, 0.1);
            transform: scale(1.01);
        }}
        
        .moon {{
            color: #10b981;
            font-weight: 700;
        }}
        
        .rekt {{
            color: #ef4444;
            font-weight: 700;
        }}
        
        .token {{
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            color: white;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 700;
            display: inline-block;
            box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
        }}
        
        .footer {{
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            margin-top: 40px;
            font-size: 0.9em;
            animation: fadeIn 0.6s ease 0.6s both;
        }}
        
        .footer p {{
            margin: 5px 0;
        }}
        
        @keyframes fadeInDown {{
            from {{
                opacity: 0;
                transform: translateY(-30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeIn {{
            from {{
                opacity: 0;
            }}
            to {{
                opacity: 1;
            }}
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .stats-grid {{
                grid-template-columns: 1fr;
            }}
            
            table {{
                font-size: 0.85em;
            }}
            
            th, td {{
                padding: 12px 8px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Kaito AI Agents Tracker</h1>
            <div class="subtitle">Post-TGE Performance</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{total_projects}</div>
                <div class="stat-label">Projects Tracked</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{mcap_str}</div>
                <div class="stat-label">Total Market Cap</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{roi_display_emoji} {'+' if best_roi_value >= 0 else ''}{best_roi_value:.1f}%</div>
                <div class="stat-label">Best All-Time ROI</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{avg_days}d</div>
                <div class="stat-label">Avg Days Since TGE</div>
            </div>
        </div>

        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Project</th>
                        <th>Token</th>
                        <th>Price</th>
                        <th>Market Cap</th>
                        <th>All-Time ROI</th>
                        <th>24h Change</th>
                        <th>7d Change</th>
                        <th>30d Change</th>
                        <th>Days Since TGE</th>
                    </tr>
                </thead>
                <tbody>
{rows_html}
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Data: CoinMarketCap + Manual TGE Prices</p>
            <p>Last updated: {timestamp_str}</p>
        </div>
    </div>
</body>
</html>
"""
    
    # Save HTML
    with open('dashboard.html', 'w') as f:
        f.write(html)
    
    print("✅ Dashboard generated successfully!")
    print("📁 Saved to: dashboard.html")
    print("\n🎯 To view:")
    print("   1. python3 -m http.server 3000")
    print("   2. Open: http://localhost:3000/dashboard.html")
    print()

if __name__ == "__main__":
    generate_dashboard()
