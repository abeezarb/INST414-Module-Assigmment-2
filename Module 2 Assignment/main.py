import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pydot

fileName = 'instagram_global_top_1000.csv'
df = pd.read_csv(fileName)
df = df.dropna()
g = nx.Graph()

# Amount of followers the lowest followed account in the dataset has
smallestAcc = df['Followers'].min()
print('Lowest Amount of Followers:',smallestAcc)

# Add all the potential categories as nodes
allCategories = list()
for category in df['Category']:
    category = category.split('|')
    for categoryName in category:
        if categoryName not in allCategories:
            allCategories.append(categoryName)
            g.add_node(categoryName)

# Add all the accounts as nodes
allAccounts = list()
for account in df['Account']:
    allAccounts.append(account)
    g.add_node(account)

# Node related Information
print('Category Nodes:', len(allCategories))
print('Account Nodes:', len(allAccounts))
print('Total Nodes:', len(g.nodes))

# Adding edges between Category Nodes and Account Nodes
for account in allAccounts:
    accountInfo = df.loc[df['Account'] == account]
    accountCategories = accountInfo['Category'].values
    for categories in accountCategories:
        categories = categories.split('|')
        for categoryName in categories:
            g.add_edge(account, categoryName, weight = 0.5)

# Printing Categories with the highest edges (degree centrality)
degreeCentrality = nx.degree_centrality(g)
sortedCentrality = sorted(degreeCentrality.items(), key = lambda item: item[1], reverse=True)

categoryLabels = dict()
i = 0
for node in sortedCentrality[:10]:
    if node[0] in allCategories:
        print('[' + str(i) + ']',node[0] + ' |', node[1])
        categoryLabels[node[0]] = node[0]
        i += 1

# Creating Visualization of Graph
d = dict(g.degree)
nx.draw(g, labels=categoryLabels, font_size=7, font_color='r', node_size=[x * 0.75 for x in d.values()])
plt.show()