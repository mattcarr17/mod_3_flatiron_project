import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix

def cat_df(df, category):
    func_count = {}
    repair_count = {}
    fail_count = {}
    for val in df[category].unique():
        func_count[val] = 0
        repair_count[val] = 0
        fail_count[val] = 0
    for idx, row in df.iterrows():
        if row['status_group'] == 'functional':
            func_count[row[category]] += 1
        elif row['status_group'] == 'functional needs repair':
            repair_count[row[category]] += 1
        elif row['status_group'] == 'non functional':
            fail_count[row[category]] += 1
    return pd.DataFrame(data = [func_count.values(), fail_count.values(),repair_count.values()], 
                    index=['functional', 'failing', 'repair'], columns = func_count.keys())

def plot_category(df, category):
    new_df = cat_df(df, category)

    fig, ax = plt.subplots(figsize=(15, 10))

    x_labels = new_df.columns
    y = new_df.values
    width = .25
    x1 = np.arange(len(y[0]))
    x2 = [x + width for x in x1]
    x3 = [x + width for x in x2]
    labels = new_df.index
    ax.bar(x1, y[0], label=labels[0], width=width)
    ax.bar(x2, y[1], label=labels[1], width=width)
    ax.bar(x3, y[2], label=labels[2], width=width)
    ax.set_title('Number of Pumps Per {} Category'.format(category.replace('_', ' ').title()), fontsize=18)
    ax.set_ylabel('Number of Pumps', fontsize=15)
    ax.set_xlabel('{} Categories'.format(category.replace('_', ' ').title()), fontsize=15)
    plt.xticks([r + width for r in range(len(y[0]))], x_labels)
    plt.legend()

    return new_df

def summarize_variable(df, cat, n):
    top_cats = df[cat].value_counts()[:(n-1)]
    new_cat = []
    for val in df[cat]:
        if val not in top_cats:
            new_cat.append('{}_other'.format(cat))
        else:
            new_cat.append(val)
    return new_cat

def plot_confusion_matrix(y_true, y_pred):
    cm = confusion_matrix(y_true, y_pred)
    labels = ['Functional', 'Repair', 'Failing']
    cm_df = pd.DataFrame(cm, columns=labels, index=labels)
    return cm_df