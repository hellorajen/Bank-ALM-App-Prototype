# Bank-ALM-App-Prototype

basic ALM

Key Concepts to Implement
Maturity Matching: Align asset and liability maturity dates

Liquidity Gap Analysis: Identify timing mismatches

## Reserve Requirements: Ensure sufficient liquid assets

Key Matching Strategies Implemented
Time Bucket Analysis:

Assets and liabilities are grouped by maturity periods

Gaps are calculated for each time period

Liquidity Coverage Ratio (LCR):

Measures high-quality liquid assets vs. stressed outflows

Basel III requires minimum 100% LCR

Early Warning System:

Alerts for negative gaps

## LCR threshold monitoring

How to Use This Enhanced System

Monitor the Dashboard:

Check LCR stays above 100%

Watch for negative gaps in any time bucket

Take Corrective Actions:

If short-term gaps exist, adjust by:

Raising more stable deposits

Selling liquid assets

Adjusting loan maturities

Strategic Planning:

Use the gap analysis to inform:

New product offerings

Funding strategies

Investment decisions
---------------

Negative Gap vs. Positive Gap (Plain English Explanation)
1. Positive Gap (Good)
What it means:

Assets > Liabilities in a given time period.

The bank has more money coming in (from loans, investments, etc.) than money going out (deposits, borrowings, etc.).

The bank is not at risk of running out of cash in this period.

Example:

Assets maturing in 0-30 days: $10 million

Liabilities due in 0-30 days: $8 million

Gap: +$2 million (Positive)

Interpretation: The bank has $2 million extra to cover obligations.

2. Negative Gap (Risky)
What it means:

Liabilities > Assets in a given time period.

The bank has more money going out (deposits, debt payments, etc.) than money coming in (loan repayments, investment returns, etc.).

The bank may face a cash shortage in this period.

Example:

Assets maturing in 31-90 days: $5 million

Liabilities due in 31-90 days: $7 million

Gap: -$2 million (Negative)

Interpretation: The bank is short $2 million and may need to borrow or sell assets to cover payments.

Why Does This Matter?
Positive Gap → Safe (Bank has enough liquidity)

Negative Gap → Warning (Bank may need emergency funding)

Banks try to minimize negative gaps by:
✔ Extending loan maturities (getting money back later)
✔ Attracting long-term deposits (keeping money longer)
✔ Selling liquid assets (raising quick cash)

This is called Asset-Liability Management (ALM)—ensuring the bank always has enough cash to meet obligations.
