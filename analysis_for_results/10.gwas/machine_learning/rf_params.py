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

def hyperparameters(classifier, X, y, grid, iterations, fold):
    
    print("Input Parameter Grid: ")
    pprint(random_grid)
    optimized_classifier = RandomizedSearchCV(estimator = classifier, param_distributions = grid, n_iter = iterations, cv = fold, verbose = 2, random_state = 42, n_jobs = -1)
    optimized_classifier.fit(X,y)
    print("Best Parameter Set: ")
    pprint(optimized_classifier.best_params_)

    return optimized_classifier

# Hyperparameter selection for Random Forest Classsifier

n_estimators = [int(x) for x in np.linspace(start = 100, stop = 2000, num = 50)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
bootstrap = [True, False]
criterion = ['gini','entropy']

random_grid = {'n_estimators': n_estimators,
              'max_features': max_features,
              'max_depth': max_depth,
              'min_samples_split': min_samples_split,
              'min_samples_leaf': min_samples_leaf,
              'bootstrap': bootstrap,
              'criterion': criterion,
        }

y = input_genes['phenotypes'].values
del input_genes['phenotypes']
X = input_genes.values

#hyperparameters(classifier=RTClassifier, X=X, y=y, grid=random_grid, iterations=1000, fold=4)
#{'bootstrap': False, 'criterion': 'entropy', 'max_depth': 30, 'max_features': 'sqrt', 'min_samples_leaf': 4, 'min_samples_split': 10, 'n_estimators': 138}

# XGBoost Classifier

n_estimators = [int(x) for x in np.linspace(start = 100, stop = 2000, num = 50)]
max_features = ['auto', 'sqrt']
max_depth = [int(x) for x in np.linspace(1, 30, num = 30)]
max_depth.append(None)
min_samples_split = [2, 5, 10]
min_samples_leaf = [1, 2, 4]
criterion = ['friedman_mse','mse']
learning_rate = [0.05, 0.1, 0.3]
loss = ['deviance','exponential']
max_leaf_nodes = [int(x) for x in np.linspace(2, 6, num = 5)]
max_leaf_nodes.append(None)

xgboost_grid = {'n_estimators': n_estimators,
              'max_features': max_features,
              'max_depth': max_depth,
              'min_samples_split': min_samples_split,
              'min_samples_leaf': min_samples_leaf,
              'criterion': criterion,
              'learning_rate':learning_rate,
              'loss':loss,
              'max_leaf_nodes':max_leaf_nodes,

        }

#xgbooster = GradientBoostingClassifier(random_state=42)
#hyperparameters(classifier=xgbooster, X=X, y=y, grid=xgboost_grid, iterations=10000, fold=4)

RTClassifier = RandomForestClassifier(random_state=42)
pprint(RTClassifier.get_params())
hyperparameters(classifier=RTClassifier, X=X, y=y, grid=random_grid, iterations=50000, fold=4)

