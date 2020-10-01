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
df2 = pd.read_sql_query(q1,conn)

# Create a visualization
ax = sns.lineplot(
    data=df1,
    x="timestamp", y="kielecki", )
ax.set(xlabel='Czas', ylabel='PLN', title='Ceny Kieleckiego')
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
# plt.show()

# ax = df1.plot(x="timestamp", y="kielecki", legend=False)
# ax2 = ax.twinx()
# df2.plot(x="timestamp", y="kielecki", ax=ax2, legend=False, color="r")
# ax.figure.legend()
plt.show()
