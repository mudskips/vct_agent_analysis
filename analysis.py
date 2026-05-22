import pandas as pd
import matplotlib.pyplot as plt


#bringing in my csv files
data_picks = pd.read_csv("vct_2026/agents/agents_pick_rates.csv")
data_wins = pd.read_csv("vct_2026/agents/teams_picked_agents.csv")

#sort data_picks to only include rows for all maps and all stages
filtered_data_picks = data_picks[(data_picks["Map"] == "All Maps") & (data_picks["Stage"] == "All Stages")]

#get rid of the % on the pick rates and turn it into a float
filtered_data_picks["Pick Rate"] = filtered_data_picks["Pick Rate"].str.replace("%", "").astype(float)

#group by agent name and average the pick rates from each event
grouped_by_agent_picks = filtered_data_picks.groupby("Agent")
overall_pick_rates = grouped_by_agent_picks["Pick Rate"].mean().reset_index()

filtered_data_wins = data_wins[(data_wins["Stage"] == "All Stages") & (data_wins["Match Type"] == "All Match Types")]

grouped_by_agent_wins = filtered_data_wins.groupby("Agent")
overall_wins = grouped_by_agent_wins[["Total Wins By Map", "Total Maps Played"]].sum()

#add win rate column as the first column
overall_wins.insert(0, "Win Rate", (overall_wins["Total Wins By Map"]/overall_wins["Total Maps Played"])*100)

#combine these two dataframes into one readable one
temp_table = pd.merge(overall_pick_rates, overall_wins, on="Agent")
final_table = temp_table.drop(columns = ["Total Wins By Map", "Total Maps Played"])

#start working on visual part
plt.scatter(final_table["Pick Rate"], final_table["Win Rate"])
plt.xlabel("Agent Pick Rate")
plt.ylabel("Agent Win Rate")

#add labels for agent names
for i, row in final_table.iterrows():
    plt.text(row["Pick Rate"], row["Win Rate"], row["Agent"])

#display plot
plt.show()
