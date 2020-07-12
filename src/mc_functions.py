import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import recall_score
from sklearn.model_selection import KFold

def cat_df(df, category):
    '''Gives count of each status_group within each
        category value.

        Function calculates the number of each pump status
        within each category of the column passed in. Structures
        information and returns in a pandas DataFrame.

        Args
            df: Pandas DataFrame with water pump functionality
                status and category values
            category:
                Column in df that function determines pump count
                for each status group in each category of given column
            
        Returns
            pandas DataFrame with count of each status group in each
            column category

    '''
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
    '''Plots number of each status group within
        each value of given category

        Function uses cat_df function to determine the number
        of each pump status within each value of given category.
        It then uses the returned dataframe to plot this information.
        
         Args
            df: Pandas DataFrame with water pump functionality
                status and category values
            category:
                Column in df that function determines pump count
                for each status group in each category of given column
        
        Returns
            Creates grouped barchart visualizing number of each
            pump status within each value of category

    '''
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
    '''Groups values in cat

    Function takes in a column with too many different values
    and groups together those that are outside the top n-1.

    Args
        df: pandas DataFrame that contains variable
            to be summarized
        cat:
            column in df to be summarized
        n:
            total number of categories to be stored in column
    
    Returns
        new_cat: cat summarized with n unique values

    '''
    top_cats = df[cat].value_counts()[:(n-1)]
    new_cat = []
    for val in df[cat]:
        if val not in top_cats:
            new_cat.append('{}_other'.format(cat))
        else:
            new_cat.append(val)
    return new_cat

def plot_confusion_matrix(y_true, y_pred):
    '''Plot confusion matrix with labels

    Function creates a confusion matrix with y_true
    and y_pred and transforms it into dataframe labeling
    the true values and model's predicted values

    Args
        y_true: True values
        y_pred: Model's predicted values

    Returns:
        cm_df: Confusion matrix as pandas DataFrame

    '''
    cm = confusion_matrix(y_true, y_pred)
    labels = ['Functional', 'Repair', 'Failing']
    cm_df = pd.DataFrame(cm, columns=labels, index=labels)
    return cm_df

def process_categories(train_df, test_df, cats):
    '''One Hot Encode's categorical variables

    Function OneHotEncode's categorical variables, cats,
    in train_df and test_df and returns encoded
    categorical variables as a dataframe

    Args:
        train_df: training data to be encoded
        test-df: testing data to be encoded
        cats: categorical columns in train_df and test_df

    Returns
        train_df_e: training data with columns cats
                    encoded
        test_df_e: testing data with columns cats
                    encoded

    '''
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
    '''Scales numerical variables

    Function uses StandardScaler to scale the numerical
    variables, nums in train_df and test_df and returns
    those dataframes with their numerical columns scaled.

    Args
        train_df: training data to be scaled
        test_df: testing data to be scaled
        nums: numerical columns in train_df and test_df
    
    Returns
        train_df: training data with scaled numerical data
        test_df: testing data with scaled numerical data

    '''
    scaler = StandardScaler()

    # fit_transform training data
    train_df[nums] = scaler.fit_transform(train_df[nums])
    # transform testing data
    test_df[nums] = scaler.transform(test_df[nums])

    # return dataframes
    return train_df, test_df

def process_data(train, test, cats, nums):
    '''Processes data for modeling

    Function scales numerical columns, nums, and categorical
    columns, cats, in dataframes train and test. Returns
    dataframes with scaled numerical data and One Hot Encoded
    categorical data

    Args:
        train: training data to be processed
        test: testing data to be processed
        cats: categorical columns to be One Hot Encoded
        nums: numerical columns to be scaled with StandardScaler
    
    Returns:
        train_df_sc: processed training data
        test_df_sc: processed testing data

    '''

    # create copies of subsetted dataframes
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
    '''Creates basic dataframe

    Function combines training features and labels into
    a single dataframe and drops the columns deemed
    unneccesary.

    Returns:
        df: dataframe with training features and target variable
            and dropped redundant/unneccesary columns

    '''

    # store features and targets in df
    vals = pd.read_csv('../../notebooks/training_set_values')
    labels = pd.read_csv('../../notebooks/training_set_labels')

    # join dataframes on 'id' column
    df = labels.merge(vals, on='id', how='outer')

    # drop unnecessary columns
    to_drop = ['Unnamed: 0_x', 'Unnamed: 0_y', 'id', 'num_private', 
    'scheme_name', 'funder', 'wpt_name', 'subvillage', 'region_code', 'district_code',
    'ward', 'public_meeting', 'recorded_by', 'permit', 'extraction_type_class',
    'management', 'payment_type', 'source', 'source_class', 'scheme_management','date_recorded']

    df.drop(to_drop, axis=1, inplace=True)

    # return datarame
    return df

def cross_val_metrics(x_train, x_test, true_train, true_test, model, n, cat_vars, num_vars):
    ''' Calculates cross metrics and classification report 
        for training and testing data

        Function peforms a KFold cross validation on n splits
        from training data and calculates average recall for 
        training and validation splits. Processes data for each split
        using process_data. Prints out a classificaion report
        for training and testing data for model with features
        cat_vars and num_vars.

        Args
            X_train: training features dataframe
            X_test: testing features dataframe
            true_train: training labels
            true_test testing labels
            model: model to be fit
            n: number of splits for cross validation scores
            cat_vars: categorical features to be included
            num_vars: numerical features to be included
        
        Returns:
            average recall for training and validation splits
            over n number of splits

            Classification report for training and testing data

    '''

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

    # print classification report for training and testing data
    print('Training Report:')
    print(classification_report(true_train, train_pred))
    print('Testing Report')
    print(classification_report(true_test, test_pred))

    return model


 

def display_scores(true, preds, model_name):
   
    '''
    
    Returns a function running recall scores, classification_report, 
    and confusion_matrix for a model.
    
    '''
    
    
    rec = recall_score(true, preds, average='micro')
    rc = classification_report(true , preds)
    cm = confusion_matrix(true, preds)
    
    print("Model: {}".format(model_name))
    print("Recall: {}".format(rec))

    print("Classification Report:\n {}".format(rc))
    print("Confusion Matrix:\n {}".format(cm))
    print("--------------------------------------------------------------------------------")
    

    return display_scores
