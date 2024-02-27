import pandas as pd
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor, GaussianProcessClassifier
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, precision_score, \
    recall_score, f1_score, silhouette_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, LogisticRegression
from sklearn.neural_network import MLPRegressor, MLPClassifier
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier, \
    ExtraTreesClassifier, BaggingClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.svm import SVR, SVC
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN, MeanShift, SpectralClustering, AffinityPropagation
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder

class ModelEvaluator:
    def __init__(self):
        pass

    def explore_dataset(df):
        """
        Perform data exploration on the provided DataFrame.

        Args:
        df (DataFrame): The DataFrame to explore.

        Returns:
        None
        """
        # Understanding the structure of the dataset
        dataset_shape = pd.DataFrame({"Value": [df.shape]})
        dataset_shape.index = ['Dataset Shape']

        # Data types of each column
        column_datatypes = pd.DataFrame(df.dtypes, columns=['Data Type'])

        # Display a few sample rows
        sample_rows = df.head()

        # Identify numeric and categorical columns
        numeric_columns = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_columns = df.select_dtypes(exclude=[np.number]).columns.tolist()

        # Check for missing values
        missing_values = df.isnull().sum().reset_index()
        missing_values.columns = ['Column', 'Missing Values']

        # Calculate summary statistics for numerical features
        summary_statistics = df.describe().transpose()

        # For categorical features, check unique values and their frequencies
        unique_values_categorical = pd.DataFrame(columns=['Column', 'Unique Values'])
        for feature in categorical_columns:
            unique_values = df[feature].value_counts().reset_index()
            unique_values.columns = ['Value', 'Frequency']
            unique_values['Column'] = feature
            unique_values_categorical = pd.concat([unique_values_categorical, unique_values], ignore_index=True)

        # Convert numeric columns and categorical columns into table format
        numeric_columns_df = pd.DataFrame({"Numeric Columns": numeric_columns})
        categorical_columns_df = pd.DataFrame({"Categorical Columns": categorical_columns})

        # Print the results in a tabular format
        print("Dataset Shape:")
        print(dataset_shape)
        print("\nColumn Data Types:")
        print(column_datatypes)
        print("\nSample Rows:")
        print(sample_rows)
        print("\nNumeric Columns:")
        print(numeric_columns_df)
        print("\nCategorical Columns:")
        print(categorical_columns_df)
        print("\nMissing Values:")
        print(missing_values)
        print("\nSummary Statistics:")
        print(summary_statistics)
        print("\nUnique Values for Categorical Columns:")
        print(unique_values_categorical)

    def encode_categorical_columns(df, columns):
        """
        Encode specified categorical columns in the DataFrame.

        Args:
        df (DataFrame): The DataFrame containing the columns to encode.
        columns (list): The list of column names to encode.

        Returns:
        DataFrame: The DataFrame with specified categorical columns encoded.
        """
        for col in columns:
            # Use label encoding for low cardinality columns
            if df[col].nunique() <= 5:
                label_encoder = LabelEncoder()
                df[col] = label_encoder.fit_transform(df[col])
            # Use one-hot encoding for high cardinality columns
            else:
                df = pd.get_dummies(df, columns=[col], drop_first=True)

        return df

    def evaluate_regression_algorithms(self, X_train, X_test, y_train, y_test):
        algorithms = {
            'Linear Regression': LinearRegression(),
            'Ridge Regression': Ridge(),
            'Lasso Regression': Lasso(),
            'Neural Network Regression': MLPRegressor(),
            'Decision Tree Regression': DecisionTreeRegressor(),
            'Random Forest': RandomForestRegressor(),
            'KNN Model': KNeighborsRegressor(),
            'Support Vector Machines (SVM)': SVR(),
            'Gaussian Regression': GaussianProcessRegressor(),
            'Polynomial Regression': make_pipeline(PolynomialFeatures(degree=2), LinearRegression()),
        }

        results = {}
        for name, model in algorithms.items():
            # Fit the model
            model.fit(X_train, y_train)

            # Predict on the test set
            predictions = model.predict(X_test)

            # Calculate evaluation metrics
            mse = mean_squared_error(y_test, predictions)
            rmse = mean_squared_error(y_test, predictions, squared=False)
            mae = mean_absolute_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            # Store metrics in dictionary
            results[name] = {'Mean Squared Error': mse, 'Root Mean Squared Error': rmse,
                             'Mean Absolute Error': mae, 'R2 Score': r2}

            # Print results for this model
            print("\nRegression Model:", name)
            print("Mean Squared Error:", mse)
            print("Root Mean Squared Error:", rmse)
            print("Mean Absolute Error:", mae)
            print("R2 Score:", r2)

        # Choose the best model based on average RMSE and R2 score
        best_model = min(results, key=lambda x: (results[x]['Root Mean Squared Error'], -results[x]['R2 Score']))

        # Print the reason for selecting the best model
        print("\nBest Regression Model:", best_model)
        print("Reason: This model has the lowest RMSE and highest R2 Score among all models.")

        return best_model, results[best_model]

    def evaluate_classification_algorithms(self, X_train, X_test, y_train, y_test):
        algorithms = {
            'Logistic Regression': LogisticRegression(),
            'Decision Tree': DecisionTreeClassifier(),
            'Random Forest': RandomForestClassifier(),
            'SVM': SVC(),
            'k-NN': KNeighborsClassifier(),
            'Naive Bayes': GaussianNB(),
            'Neural Network': MLPClassifier(),
            'Gradient Boosting': GradientBoostingClassifier(),
            'Linear Discriminant Analysis': LinearDiscriminantAnalysis(),
            'Extra Trees': ExtraTreesClassifier(),
            'Bagging': BaggingClassifier(),
            'Gaussian Process': GaussianProcessClassifier()
        }

        results = {}
        for name, model in algorithms.items():
            # Fit the model
            model.fit(X_train, y_train)

            # Predict on the test set
            predictions = model.predict(X_test)

            # Calculate evaluation metrics
            accuracy = accuracy_score(y_test, predictions)
            precision = precision_score(y_test, predictions, average='weighted')
            recall = recall_score(y_test, predictions, average='weighted')
            f1 = f1_score(y_test, predictions, average='weighted')

            # Store metrics in dictionary
            results[name] = {'Accuracy': accuracy, 'Precision': precision, 'Recall': recall, 'F1 Score': f1}

            # Print results for this model
            print("\nClassification Model:", name)
            print("Accuracy:", accuracy)
            print("Precision:", precision)
            print("Recall:", recall)
            print("F1 Score:", f1)

        # Choose the best model based on average F1 score
        best_model = max(results, key=lambda x: results[x]['F1 Score'])

        # Print the reason for selecting the best model
        print("\nBest Classification Model:", best_model)
        print("Reason: This model has the highest F1 Score among all models.")

        return best_model, results[best_model]

    def evaluate_clustering_algorithms(self, X):
        algorithms = {
            'K-Means': KMeans(),
            'Hierarchical Clustering (Agglomerative)': AgglomerativeClustering(),
            'DBSCAN': DBSCAN(),
            'Mean Shift': MeanShift(),
            'Gaussian Mixture Models (GMM)': GaussianMixture(),
            'Affinity Propagation': AffinityPropagation(),
            'Spectral Clustering': SpectralClustering()
        }

        results = {}
        for name, model in algorithms.items():
            # Fit the model
            if name == 'Gaussian Mixture Models (GMM)':
                model = GaussianMixture(n_components=5)  # Example: You can specify the number of components
            model.fit(X)

            # Predict cluster labels
            labels = model.predict(X)

            # Calculate evaluation metrics
            silhouette = silhouette_score(X, labels)
            # Adjusted Rand Index can only be computed if true labels are available
            # adjusted_rand = adjusted_rand_score(true_labels, labels)

            # Store metrics in dictionary
            results[name] = {'Silhouette Score': silhouette}

            # Print results for this model
            print("\nClustering Model:", name)
            print("Silhouette Score:", silhouette)

        # Choose the best model based on silhouette score
        best_model = max(results, key=lambda x: results[x]['Silhouette Score'])

        # Print the reason for selecting the best model
        print("\nBest Clustering Model:", best_model)
        print("Reason: This model has the highest Silhouette Score among all models.")

        return best_model, results[best_model]
