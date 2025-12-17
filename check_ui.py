import matplotlib.pyplot as plt
import numpy as np

# --- Data Preparation ---
# Source 1: Avlijas et al. (2021) - Sustainability Journal
# Comparing Stock-Out Rates (Lower is better)
scenarios_stock = ['Manual Ordering', 'Automated Replenishment']
stock_out_rates = [3.72, 1.38] # Percentages

# Source 2: Job Done Automation (2024) - Case Study
# Comparing Processing Time (Lower is better)
scenarios_time = ['Manual Processing', 'Automated Processing']
time_spent_index = [100, 40] # Baseline 100%, Reduced by 60% -> 40%

# --- Plotting ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# GRAPH 1: Stock-Out Rate Comparison
bars1 = ax1.bar(scenarios_stock, stock_out_rates, color=['#e74c3c', '#27ae60'], width=0.6)
ax1.set_ylabel('Stock-Out Rate (%)', fontsize=12)
ax1.set_title('Impact on Product Availability (Stock-Outs)', fontsize=14, fontweight='bold')
ax1.set_ylim(0, 5)

# Add value labels
for bar in bars1:
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1,
             f'{height}%', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Add Source Citation to Graph 1
ax1.text(0.5, -0.15, 'Source: Avlijas et al. (2021), Sustainability Journal, 13(3)',
         transform=ax1.transAxes, ha='center', fontsize=10, style='italic', color='#555')


# GRAPH 2: Processing Time Efficiency
bars2 = ax2.bar(scenarios_time, time_spent_index, color=['#95a5a6', '#3498db'], width=0.6)
ax2.set_ylabel('Time Spent Index (Baseline=100)', fontsize=12)
ax2.set_title('Reduction in Administrative Labor Time', fontsize=14, fontweight='bold')
ax2.set_ylim(0, 120)

# Add value labels
for bar in bars2:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 2,
             f'{height}\n(Index)', ha='center', va='bottom', fontsize=12, fontweight='bold')

# Add Source Citation to Graph 2
ax2.text(0.5, -0.15, 'Source: Job Done Automation (2024), Case Study: Retail Chain',
         transform=ax2.transAxes, ha='center', fontsize=10, style='italic', color='#555')

plt.tight_layout()
plt.show()