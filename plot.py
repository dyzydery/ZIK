# Import seaborn
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

import sqlite3

def savePlot(produkt):
    sns.set_theme()
    conn = sqlite3.connect('zik.db')
    q1 = "SELECT timestamp,"+produkt+" FROM 'ceny';"
    q2 = "SELECT timestamp,"+produkt+" FROM 'zik';"

    df1 = pd.read_sql_query(q1,conn)
    df2 = pd.read_sql_query(q2,conn)

    # Create a visualization
    ax = sns.lineplot(
        data=df2,color="red",
        x="timestamp", y=produkt, )
    ax.set(xlabel='Czas', ylabel='PLN', title=produkt)
    # ax.set(xticks=df2.timestamp[2::50])
    ax2 = ax.twinx()
    ax = sns.lineplot(
        data=df1,
        x="timestamp", y=produkt, )

    ts = df1["timestamp"]
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
    plt.savefig("wykresy/"+produkt+".png")
    plt.clf()

produkty = ['kielecki','pizza','maslo','jablka','makaron','chleb','mydlo','kurczak','jajka','rolex','whisky','piwo','buty','auto_Mean','auto_Median','telefon','bigmac','m2wtorny','m2pierwotny','benzyna','lot','fryzjer','upc','prad','lekarz_Mean','lekarz_Median','aspiryna','karma','kasjer','xau','chf','usd','kindle']

for p in produkty:
    savePlot(p)
# plt.show()
