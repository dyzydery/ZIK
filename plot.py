# Import seaborn
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
tips = pd.read_csv('zikDB.csv')
# Apply the default theme
sns.set_theme()
import sqlite3

conn = sqlite3.connect('zik.db')
q1 = "SELECT timestamp,kielecki FROM 'ceny';"
q2 = "SELECT timestamp,kielecki FROM 'zik';"

df1 = pd.read_sql_query(q1,conn)
df2 = pd.read_sql_query(q2,conn)

# Create a visualization
ax = sns.lineplot(
    data=df2,color="red",
    x="timestamp", y="kielecki", )
ax.set(xlabel='Czas', ylabel='PLN', title='Ceny Kieleckiego')
# ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
ax.set(xticks=df2.timestamp[2::50])
ax2 = ax.twinx()
ax = sns.lineplot(
    data=df1,
    x="timestamp", y="kielecki", )

ts = df1["timestamp"]
# xticks and xticks labels
xTicks = list(range(len(ts)))

xTickLabels = [i for i in range(len(ts))]
for xTick in xTicks:
    if xTick % 50 == 0:
        xTickLabels[xTick] = ts[xTick][:10]
    else:
        xTickLabels[xTick] = ''
        xTick = 0


ax.xaxis.grid(True)
ax.set_xticks(xTicks)
ax.set_xticklabels(xTickLabels, fontsize=6)

plt.show()
