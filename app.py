from flask import Flask, render_template, request, redirect, url_for
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

# Simple in-memory database (for demo only - use a real DB in production)
assets = [
    {"id": 1, "type": "Loans", "amount": 5000000, "maturity": "2025-12-31", "rate": 0.05},
    {"id": 2, "type": "Securities", "amount": 2000000, "maturity": "2024-06-30", "rate": 0.03}
]

liabilities = [
    {"id": 1, "type": "Deposits", "amount": 4000000, "maturity": "2024-12-31", "rate": 0.02},
    {"id": 2, "type": "Bonds", "amount": 1000000, "maturity": "2026-06-30", "rate": 0.04}
]

def calculate_maturity_gaps():
    """Calculate maturity gaps for different time buckets"""
    asset_maturities = defaultdict(float)
    liability_maturities = defaultdict(float)
    
    time_buckets = {
        '0-30': 30,
        '31-90': 90,
        '91-180': 180,
        '181-365': 365,
        '1-2y': 730,
        '2-5y': 1825,
        '5+y': float('inf')
    }
    
    today = datetime.now().date()
    
    for asset in assets:
        maturity_date = datetime.strptime(asset['maturity'], '%Y-%m-%d').date()
        days_to_maturity = (maturity_date - today).days
        
        for bucket, days in time_buckets.items():
            if days_to_maturity <= days:
                asset_maturities[bucket] += asset['amount']
                break
    
    for liability in liabilities:
        maturity_date = datetime.strptime(liability['maturity'], '%Y-%m-%d').date()
        days_to_maturity = (maturity_date - today).days
        
        for bucket, days in time_buckets.items():
            if days_to_maturity <= days:
                liability_maturities[bucket] += liability['amount']
                break
    
    maturity_gaps = {
        bucket: asset_maturities.get(bucket, 0) - liability_maturities.get(bucket, 0)
        for bucket in time_buckets
    }
    
    # Format values for display
    formatted_assets = {k: "${:,.2f}".format(v) for k, v in asset_maturities.items()}
    formatted_liabilities = {k: "${:,.2f}".format(v) for k, v in liability_maturities.items()}
    formatted_gaps = {k: "${:,.2f}".format(v) for k, v in maturity_gaps.items()}
    
    return formatted_gaps, formatted_assets, formatted_liabilities

def calculate_lcr():
    """Calculate Liquidity Coverage Ratio"""
    try:
        hqla = sum(a['amount'] for a in assets if a['type'] in ['Cash', 'Securities'])
        stressed_outflows = sum(
            l['amount'] * 0.05 if l['type'] == 'Deposits' else l['amount'] * 0.10
            for l in liabilities
        )
        
        lcr = hqla / stressed_outflows if stressed_outflows > 0 else None
        return "{:.2%}".format(lcr) if lcr is not None else "N/A"
    except Exception as e:
        print(f"Error calculating LCR: {e}")
        return "N/A"

def calculate_ldr():
    try:
        total_loans = sum(a['amount'] for a in assets if a['type'] == 'Loans')
        total_deposits = sum(l['amount'] for l in liabilities if l['type'] == 'Deposits')
        return total_loans / total_deposits if total_deposits > 0 else float('inf')
    except:
        return float('inf')

def calculate_nim():
    try:
        interest_income = sum(a['amount'] * a['rate'] for a in assets)
        interest_expense = sum(l['amount'] * l['rate'] for l in liabilities)
        avg_earning_assets = sum(a['amount'] for a in assets if a['type'] in ['Loans', 'Securities'])
        return (interest_income - interest_expense) / avg_earning_assets if avg_earning_assets > 0 else 0
    except:
        return 0

def calculate_nsfr():
    try:
        available_funding = sum(
            l['amount'] * 0.95 if l['type'] == 'Deposits' else l['amount'] * 0.85
            for l in liabilities
        )
        required_funding = sum(
            a['amount'] * 0.65 if a['type'] == 'Loans' else a['amount'] * 0.50
            for a in assets
        )
        return available_funding / required_funding if required_funding > 0 else float('inf')
    except:
        return float('inf')

def check_liquidity_alerts():
    """Generate liquidity risk alerts"""
    alerts = []
    
    lcr_display = calculate_lcr()
    if lcr_display != "N/A":
        try:
            lcr_value = float(lcr_display.strip('%')) / 100
            if lcr_value < 1.0:
                alerts.append(f"Warning: LCR is {lcr_display} (below 100% requirement)")
        except ValueError:
            pass
    
    maturity_gaps, _, _ = calculate_maturity_gaps()
    for bucket, gap in maturity_gaps.items():
        if '-' in gap:  # Negative gap
            alerts.append(f"Negative gap in {bucket} bucket: {gap}")
    
    return alerts

@app.route('/')
def dashboard():
    """Main dashboard with all ALM metrics"""
    total_assets = sum(a['amount'] for a in assets)
    total_liabilities = sum(l['amount'] for l in liabilities)
    net_interest_income = (
        sum(a['amount'] * a['rate'] for a in assets) - 
        sum(l['amount'] * l['rate'] for l in liabilities)
    )
        # New ratio calculations
    ldr = calculate_ldr()
    nim = calculate_nim()
    nsfr = calculate_nsfr()
    
    # Format ratios safely
    ratios = {
        'ldr': float(ldr) if ldr != float('inf') else None,
        'nim': float(nim) if nim != float('inf') else None,
        'nsfr': float(nsfr) if nsfr != float('inf') else None
    }
    
    maturity_gaps, asset_maturities, liability_maturities = calculate_maturity_gaps()
    lcr_display = calculate_lcr()
    alerts = check_liquidity_alerts()
    
    return render_template('dashboard.html', 
                         total_assets="${:,.2f}".format(total_assets),
                         total_liabilities="${:,.2f}".format(total_liabilities),
                         net_interest_income="${:,.2f}".format(net_interest_income),
                         ratios=ratios,
                         assets=assets[-5:],
                         liabilities=liabilities[-5:],
                         maturity_gaps=maturity_gaps,
                         asset_maturities=asset_maturities,
                         liability_maturities=liability_maturities,
                         lcr_display=lcr_display,
                         alerts=alerts)

@app.route('/assets', methods=['GET', 'POST'])
def manage_assets():
    """Asset management view"""
    if request.method == 'POST':
        new_asset = {
            "id": len(assets) + 1,
            "type": request.form['type'],
            "amount": float(request.form['amount']),
            "maturity": request.form['maturity'],
            "rate": float(request.form['rate'])
        }
        assets.append(new_asset)
        return redirect(url_for('manage_assets'))
    return render_template('assets.html', assets=assets)

@app.route('/liabilities', methods=['GET', 'POST'])
def manage_liabilities():
    """Liability management view"""
    if request.method == 'POST':
        new_liability = {
            "id": len(liabilities) + 1,
            "type": request.form['type'],
            "amount": float(request.form['amount']),
            "maturity": request.form['maturity'],
            "rate": float(request.form['rate'])
        }
        liabilities.append(new_liability)
        return redirect(url_for('manage_liabilities'))
    return render_template('liabilities.html', liabilities=liabilities)

if __name__ == '__main__':
    app.run(debug=True)