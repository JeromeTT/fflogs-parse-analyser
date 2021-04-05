import pandas as pd 
import csv
import matplotlib.pyplot as plt
import os
encounternames = {73: 'Cloud of Darkness', 74: 'Shadowkeeper', 75: 'Fatebreaker', 76: "Eden's Promise", 77: 'Oracle of Darkness'}
encounterids = [73, 74, 75, 76, 77]
jobs = ['Paladin', 'Warrior', 'Dark Knight', 'Gunbreaker','White Mage','Scholar','Astrologian', 'Monk', 'Dragoon', 'Ninja', 'Samurai', 'Bard', 'Machinist', 'Dancer', 'Black Mage', 'Summoner', 'Red Mage']
for encounter in [77]:
    for job in ['Dragoon']:
        df = pd.read_csv("2021_04_06_001335/{}{}.txt".format(job, encounter))
        plt.figure(figsize=(10,9))
        plt.title(encounternames[encounter] + ' All Parses for ' + job)
        plt.ylabel('Kill Time (Minutes)')
        plt.xlabel('Raid DPS')
        print(df)
        color = ['#FF0000' if row[1]['report'] == '81dvHgpm9abRyKJk' else '#1f77b4' for row in df.iterrows()]
        size = [16 if row[1]['report'] == '81dvHgpm9abRyKJk' else 4 for row in df.iterrows()]
        plt.scatter(df['rdps'], df['killtime']/60000, c= color, s=size)
        
        plt.savefig('graphoutputs/'+ job + str(encounter)+'.png')
        plt.close()