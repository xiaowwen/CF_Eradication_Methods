import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import precision_recall_fscore_support
from sklearn.utils.multiclass import unique_labels
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import KFold
from sklearn.model_selection import RandomizedSearchCV
from pprint import pprint

input_genes = pd.read_csv(filepath_or_buffer='ml_train_input.txt', sep='\t', header=0, index_col=0)

def RF_Model(X, y, n_estimators, criterion, max_depth, min_samples_split, min_samples_leaf, max_features, bootstrap):
    
    RF_classifier = RandomForestClassifier(n_estimators=n_estimators, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, max_features=max_features, bootstrap = bootstrap, random_state=42)

    RF_classifier.fit(X,y)
    
    preds         = RF_classifier.predict(X)
    confusion     = confusion_matrix(y, preds , sample_weight=None)
    labels        = unique_labels(y, preds)
    inp           = precision_recall_fscore_support(y, preds, labels=labels, average=None)
    res_conf      = confusion.ravel().tolist()
    res_inp       = np.asarray(inp).ravel().tolist()

    print("Precision | Recall | Fscore | Support")
    print("----------------------------------------------------------")
    pprint(res_inp)
    print("----------------------------------------------------------")

    print("Confision Matrix")
    print("----------------------------------------------------------")
    pprint(confusion)
    print("----------------------------------------------------------")

    print("Feature Importance")
    feature_importance_list = []
    max_feat_index_list = []

    feature_importance = RF_classifier.feature_importances_
    
    for i in range(20):

        max_feat_index     = np.argmax(feature_importance)
        feature_importance_list.append([max_feat_index, feature_importance[max_feat_index]])
        max_feat_index_list.append(max_feat_index)
        feature_importance[max_feat_index] = 0.0

    pprint(feature_importance_list)
    print("----------------------------------------------------------")

    return [RF_classifier, max_feat_index_list]

def XGBoost_Model(X, y, n_estimators, learning_rate, criterion, max_depth, min_samples_split, min_samples_leaf, max_features, loss):

    XGB_classifier = GradientBoostingClassifier(n_estimators=n_estimators, learning_rate=learning_rate, criterion=criterion, max_depth=max_depth, min_samples_split=min_samples_split, min_samples_leaf=min_samples_leaf, max_features=max_features, loss = loss, random_state=42)

    XGB_classifier.fit(X,y)

    preds         = XGB_classifier.predict(X)
    confusion     = confusion_matrix(y, preds , sample_weight=None)
    labels        = unique_labels(y, preds)
    inp           = precision_recall_fscore_support(y, preds, labels=labels, average=None)
    res_conf      = confusion.ravel().tolist()
    res_inp       = np.asarray(inp).ravel().tolist()

    print("=================XGBoost Model=============================")
    print("Precision | Recall | Fscore | Support")
    print("----------------------------------------------------------")
    pprint(res_inp)
    print("----------------------------------------------------------")

    print("Confision Matrix")
    print("----------------------------------------------------------")
    pprint(confusion)
    print("----------------------------------------------------------")

    print("Feature Importance")
    feature_importance_list = []
    max_feat_index_list = []

    feature_importance = XGB_classifier.feature_importances_

    for i in range(20):

        max_feat_index     = np.argmax(feature_importance)
        feature_importance_list.append([max_feat_index, feature_importance[max_feat_index]])
        max_feat_index_list.append(max_feat_index)
        feature_importance[max_feat_index] = 0.0

    pprint(feature_importance_list)
    print("----------------------------------------------------------")

    return [XGB_classifier, max_feat_index_list]


# Hyperparameter selection for Random Forest Classsifier

y = input_genes['phenotypes'].values
del input_genes['phenotypes']
X = input_genes.values

print(len(input_genes.columns))
# Run RF Model
model, max_import = RF_Model(X, y,n_estimators=1380, criterion='entropy', max_depth=10, min_samples_split=10, min_samples_leaf=1, max_features='auto', bootstrap = True)
pprint(input_genes.columns[max_import].values.tolist())

# Run XGBoost Model
model, max_import = XGBoost_Model(X, y, n_estimators=1380, learning_rate=0.3, criterion='friedman_mse', max_depth=None, min_samples_split=5, min_samples_leaf=1, max_features='sqrt', loss='exponential')
#model, max_import = XGBoost_Model(X, y, n_estimators=302, learning_rate=0.3, criterion='friedman_mse', max_depth=None, min_samples_split=5, min_samples_leaf=1, max_features='sqrt', loss='exponential')
pprint(input_genes.columns[max_import].values.tolist())

#Best RF model (1000 iterations): {'bootstrap': False, 'criterion': 'entropy', 'max_depth': 30, 'max_features': 'sqrt', 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 138}
#Best RF model2: {'bootstrap': True, 'criterion': 'entropy', 'max_depth': 10, 'max_features': 'auto', 'min_samples_leaf': 1, 'min_samples_split': 10, 'n_estimators': 138}

#Best XGBoost:{'criterion': 'mse','learning_rate': 0.3,'loss':'exponential','max_depth': 30,'max_features':'sqrt','max_leaf_nodes': None,'min_samples_leaf':4,'min_samples_split':2,'n_estimators': 1030}
#Best XGBoost2:{'criterion': 'friedman_mse', 'learning_rate': 0.3, 'loss': 'exponential', 'max_depth': None, 'max_features': 'sqrt', 'max_leaf_nodes': None, 'min_samples_leaf': 1, 'min_samples_split': 5, 'n_estimators': 138}

#Best XGBoost3:
#{'criterion': 'friedman_mse', 'learning_rate': 0.3, 'loss': 'exponential', 'max_depth': None, 'max_features': 'sqrt', 'max_leaf_nodes': None, 'min_samples_leaf': 1, 'min_samples_split': 5, 'n_estimators': 302}

