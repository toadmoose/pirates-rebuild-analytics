import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import time

print("Starting Pittsburgh Pirates Rebuild Analytics...")
start_time = time.time()

# Load data
roster = pd.read_csv('pirates_data.csv')
team_history = pd.read_csv('team_history.csv')

# Create a single comprehensive visualization
plt.figure(figsize=(20, 16))
plt.suptitle('Pittsburgh Pirates Rebuild Analytics Dashboard', fontsize=24, y=0.98)

# Create grid for subplots
gs = gridspec.GridSpec(3, 2, height_ratios=[1, 1, 1.2])

# 1. Team History Chart (top left)
ax1 = plt.subplot(gs[0, 0])
ax1.plot(team_history['Season'], team_history['Wins'], marker='o', linewidth=2, color='#FDB827')
ax1.set_title('Pirates Win Totals by Season', fontsize=16)
ax1.set_xlabel('Season')
ax1.set_ylabel('Wins')
ax1.grid(True, alpha=0.3)
ax1.axhline(y=81, color='#27A9E1', linestyle='--', alpha=0.7)  # .500 line
ax1.set_ylim(bottom=0)

# 2. WAR by Position Chart (top right)
ax2 = plt.subplot(gs[0, 1])
position_war = roster.groupby('Position')['WAR'].sum().reset_index()
bars = ax2.bar(position_war['Position'], position_war['WAR'], color='#27A9E1')
ax2.set_title('Team WAR by Position', fontsize=16)
ax2.set_xlabel('Position')
ax2.set_ylabel('Total WAR')
# Add values on top of bars
for bar in bars:
    height = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
            f'{height:.1f}', ha='center', va='bottom')

# 3. Best Players Table (middle left)
ax3 = plt.subplot(gs[1, 0])
# ====================================================================
# TITLE POSITION: This controls where the title appears
# IMPORTANT: To move the title closer to the table, change this line
# The default position is y=1.0 (top of the cell)
# Try reducing this value to move the title down closer to the table
# Example: y=0.9 or y=0.85 or even y=0.75 depending on how close you want it
# ====================================================================
ax3.set_title('5 Best Players by WAR', fontsize=16, y=0.79)  # <-- ADJUST THIS y VALUE
ax3.axis('tight')
ax3.axis('off')
best_players = roster.sort_values('WAR', ascending=False).head(5)
best_table = ax3.table(
    cellText=best_players[['Name', 'Position', 'Age', 'WAR']].values,
    colLabels=['Name', 'Position', 'Age', 'WAR'],
    loc='center',
    cellLoc='center'
)
best_table.auto_set_font_size(False)
best_table.set_fontsize(12)
best_table.scale(1, 1.5)
for (i, j), cell in best_table.get_celld().items():
    if i == 0:  # Header row
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#000000')
    else:
        cell.set_facecolor('#FDB827' if i % 2 == 0 else '#FFFFFF')

# 4. Oldest Players Table (middle right)
ax4 = plt.subplot(gs[1, 1])
# ====================================================================
# TITLE POSITION: This controls where the title appears
# IMPORTANT: To move the title closer to the table, change this line
# The default position is y=1.0 (top of the cell)
# Try reducing this value to move the title down closer to the table
# Make sure to use the same value as you used for the other table title
# ====================================================================
ax4.set_title('3 Oldest Players', fontsize=16, y=0.79)  # <-- ADJUST THIS y VALUE
ax4.axis('tight')
ax4.axis('off')
oldest_players = roster.sort_values('Age', ascending=False).head(3)
oldest_table = ax4.table(
    cellText=oldest_players[['Name', 'Position', 'Age', 'WAR']].values,
    colLabels=['Name', 'Position', 'Age', 'WAR'],
    loc='center',
    cellLoc='center'
)
oldest_table.auto_set_font_size(False)
oldest_table.set_fontsize(12)
oldest_table.scale(1, 1.5)
for (i, j), cell in oldest_table.get_celld().items():
    if i == 0:  # Header row
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#000000')
    else:
        cell.set_facecolor('#FDB827' if i % 2 == 0 else '#FFFFFF')

# 5. Summary Statistics and Recommendations (bottom)
ax5 = plt.subplot(gs[2, :])
ax5.axis('off')

# Calculate key metrics
total_war = roster['WAR'].sum()
total_salary = roster['Salary'].sum()
avg_age = roster['Age'].mean()
young_talent = roster[roster['Age'] < 25]['WAR'].sum()
pitching_war = roster[roster['Position'].isin(['SP', 'RP'])]['WAR'].sum()
hitting_war = roster[~roster['Position'].isin(['SP', 'RP'])]['WAR'].sum()

# Create summary text
summary = (
    f"PIRATES REBUILD STRATEGY RECOMMENDATIONS\n\n"
    f"Team Overview: {total_war:.1f} Total WAR | ${total_salary/1000000:.1f}M Total Payroll | {avg_age:.1f} Average Age\n\n"
    f"Strengths:\n"
    f"• Young talent foundation: {young_talent:.1f} WAR from players under 25\n"
    f"• Pitching core: {pitching_war:.1f} WAR from pitchers (Paul Skenes as potential ace)\n\n"
    f"Recommended Rebuild Strategy:\n"
    f"1. Build around core young players (Skenes, Cruz, Hayes)\n"
    f"2. Consider trading veteran assets (Reynolds, McCutchen) for prospects\n"
    f"3. Prioritize player development system to maximize young talent\n"
    f"4. Target 2026-2027 for competitive window opening"
)

ax5.text(0.5, 0.5, summary, fontsize=14, ha='center', va='center', 
         bbox=dict(boxstyle='round', facecolor='#f9f9f9', alpha=0.8))

# Add Pirates colors and branding
plt.figtext(0.5, 0.01, 'Pittsburgh Pirates Rebuild Analytics - Project for Xylem Analytics Internship',
           ha='center', fontsize=10, style='italic')

# Adjust layout
plt.tight_layout(rect=[0, 0.03, 1, 0.95])

# Save high-quality image
plt.savefig('pirates_analytics_dashboard.png', dpi=300, bbox_inches='tight')
plt.close()

print(f"\nAnalysis complete! Dashboard image saved to 'pirates_analytics_dashboard.png'")
print(f"Process completed in {time.time() - start_time:.2f} seconds")