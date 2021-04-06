import pandas as pd 
import csv
import matplotlib.pyplot as plt
import os
encountersdict = {73: 'Cloud of Darkness', 74: 'Shadowkeeper', 75: 'Fatebreaker', 76: "Eden's Promise", 77: 'Oracle of Darkness'}
encounterids = [73, 74, 75, 76, 77]
jobs = ['Paladin', 'Warrior', 'Dark Knight', 'Gunbreaker','White Mage','Scholar','Astrologian', 'Monk', 'Dragoon', 'Ninja', 'Samurai', 'Bard', 'Machinist', 'Dancer', 'Black Mage', 'Summoner', 'Red Mage']


def killtime_rdps_graph(characters, dir, encounters, encounternames, jobs):
    ''' Graphs killtime against raid dps. Has the option to highlight certain characters.
    '''
    for encounter in encounters:
        for job in jobs:
            df = pd.read_csv(dir + "/{}{}.txt".format(job, encounter))
            plt.figure(figsize=(20,18))
            plt.title(encounternames[encounter] + ' All Parses for ' + job)
            plt.ylabel('Kill Time (Minutes)')
            plt.xlabel('Raid DPS')
            newdf = df[df["name"].isin(characters)]
            plt.scatter(df['rdps'], df['killtime']/60000, s=32)
            plt.scatter(newdf['rdps'], newdf['killtime']/60000, c='red',s=128)
            plt.savefig('graphoutputs/'+ job + str(encounter)+'.png')
            plt.close()