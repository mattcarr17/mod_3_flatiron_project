import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import recall_score
from sklearn.model_selection import KFold

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

def process_categories(train_df, test_df, cats):
    ohe = OneHotEncoder()

    # fit_transform training data
    train_encoded = ohe.fit_transform(train_df[cats])
    # transform testing data
    test_encoded = ohe.transform(test_df[cats])

    # create dataframes
    train_df_e = pd.DataFrame(train_encoded.todense(), index=train_df[cats].index, columns=ohe.get_feature_names())
    test_df_e = pd.DataFrame(test_encoded.todense(), index=test_df[cats].index, columns=ohe.get_feature_names())

    # return dataframes
    return train_df_e, test_df_e

def process_numerics(train_df, test_df, nums):
    scaler = StandardScaler()

    # fit_transform training data
    train_df[nums] = scaler.fit_transform(train_df[nums])
    # transform testing data
    test_df[nums] = scaler.transform(test_df[nums])

    # return dataframes
    return train_df, test_df

def process_data(train, test, cats, nums):

    train_df = train[cats+nums].copy()
    test_df = test[cats+nums].copy()


    # OHE categorical data
    train_encoded, test_encoded = process_categories(train_df, test_df, cats)

    # drop original categorical columns
    train_df.drop(cats, axis=1, inplace=True)
    test_df.drop(cats, axis=1, inplace=True)

    # scale numerical data
    train_df_sc, test_df_sc = process_numerics(train_df, test_df, nums)

    # combine scaled numeric and OHE categorical
    train_df_sc = pd.concat([train_df_sc, train_encoded], axis=1)
    test_df_sc = pd.concat([test_df_sc, test_encoded], axis=1)

    # return dataframes
    return train_df_sc, test_df_sc

def create_base_df():

    # store features and targets in df
    vals = pd.read_csv('../../notebooks/training_set_values')
    labels = pd.read_csv('../../notebooks/training_set_labels')

    # join dataframes on 'id' column
    df = labels.merge(vals, on='id', how='outer')

    # drop unnecessary columns
    to_drop = ['Unnamed: 0_x', 'Unnamed: 0_y', 'id', 'num_private', 
    'scheme_name', 'funder', 'longitude', 'latitude', 'wpt_name', 'subvillage', 'region_code', 'district_code',
    'lga', 'ward', 'public_meeting', 'recorded_by', 'permit', 'extraction_type', 'extraction_type_class',
    'management', 'payment_type', 'quality_group', 'quantity_group', 'source', 'source_class',
    'waterpoint_type', 'scheme_management','date_recorded']

    df.drop(to_drop, axis=1, inplace=True)

    # return datarame
    return df

def cross_val_metrics(x_train, x_test, true_train, true_test, model, n, cat_vars, num_vars):

    #instanitate KFold with n splilts
    folds = KFold(n_splits=n)

    # cross_val over n splits
    train_recall = []
    val_recall = []
    for train, val in folds.split(x_train):

        # process data
        x_train_f, x_val_f = process_data(x_train.iloc[train], x_train.iloc[val], cat_vars, num_vars)

        # fit model on processed training data
        model.fit(x_train_f, true_train.iloc[train])

        # predictions for train and val data
        train_preds = model.predict(x_train_f)
        val_preds = model.predict(x_val_f)

        # calculate recall and append to list
        train_recall.append(recall_score(true_train.iloc[train], train_preds, average='weighted'))
        val_recall.append(recall_score(true_train.iloc[val], val_preds, average='weighted'))

    # print average recall score
    print('Training Recall: {}'.format(np.mean(train_recall)))
    print('Val Recall: {}'.format(np.mean(val_recall)))

    # process data for overall score and confusion matrix
    x_train_, x_test_ = process_data(x_train, x_test, cat_vars, num_vars)

    # fit model for cm
    model.fit(x_train_, true_train)

    # make predictions
    train_pred = model.predict(x_train_)
    test_pred = model.predict(x_test_)

    # print recall score for training and testing data
    print('Training Recall: {}'.format(recall_score(true_train, train_pred, average='weighted')))
    print('Testing Recall: {}'.format(recall_score(true_test, test_pred, average='weighted')))
    
    # confusion_matrix for training and testing data
    print('Training CM:')
    print(plot_confusion_matrix(true_train, train_pred))
    print('Testing CM:')
    print(plot_confusion_matrix(true_test, test_pred))

    return model