import os
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer

from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


# ==========================================
# PATHS
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "road_accident_data.csv"
)

MODEL_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


# ==========================================
# LOAD DATA
# ==========================================

def load_data():

    df = pd.read_csv(DATA_PATH)

    df.columns = df.columns.str.strip()

    df = df.replace("?", np.nan)

    df = df.drop_duplicates()

    return df


# ==========================================
# PREPARE DATA
# ==========================================

def prepare_data(df):

    target_column = "Accident_severity"

    if target_column not in df.columns:

        raise ValueError(
            "Accident_severity column not found."
        )

    df = df.dropna(
        subset=[target_column]
    )

    y = df[target_column].astype(str)

    X = df.drop(
        columns=[target_column]
    )


    # ======================================
    # REMOVE IDENTIFIER COLUMNS
    # ======================================

    identifier_columns = [
        "Accident_Index",
        "Accident index",
        "accident_index",
        "ID",
        "id"
    ]

    identifier_columns = [
        column
        for column in identifier_columns
        if column in X.columns
    ]

    if identifier_columns:

        X = X.drop(
            columns=identifier_columns
        )


    # ======================================
    # REMOVE DATA LEAKAGE / POST-ACCIDENT
    # ======================================

    leakage_columns = [

        "Number_of_casualties",

        "Casualty_class",

        "Sex_of_casualty",

        "Age_band_of_casualty",

        "Casualty_severity",

        "Work_of_casuality",

        "Fitness_of_casuality",

        "Pedestrian_movement",

        "Cause_of_accident"
    ]


    leakage_columns = [
        column
        for column in leakage_columns
        if column in X.columns
    ]


    if leakage_columns:

        print(
            "\nRemoving leakage/post-accident columns:"
        )

        for column in leakage_columns:

            print(
                " -",
                column
            )

        X = X.drop(
            columns=leakage_columns
        )


    return X, y


# ==========================================
# PREPROCESSING
# ==========================================

def create_preprocessing_pipeline(X):

    numeric_columns = X.select_dtypes(
        include=["int64", "float64"]
    ).columns.tolist()


    categorical_columns = X.select_dtypes(
        include=[
            "object",
            "category",
            "bool"
        ]
    ).columns.tolist()


    print("\nNumeric columns:")

    print(
        numeric_columns
    )


    print("\nCategorical columns:")

    print(
        categorical_columns
    )


    # ======================================
    # NUMERIC PIPELINE
    # ======================================

    numeric_pipeline = Pipeline(
        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="median"
                )
            ),

            (
                "scaler",
                StandardScaler()
            )
        ]
    )


    # ======================================
    # CATEGORICAL PIPELINE
    # ======================================

    categorical_pipeline = Pipeline(
        steps=[

            (
                "imputer",
                SimpleImputer(
                    strategy="most_frequent"
                )
            ),

            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore"
                )
            )
        ]
    )


    # ======================================
    # COLUMN TRANSFORMER
    # ======================================

    preprocessing_pipeline = ColumnTransformer(

        transformers=[

            (
                "numeric",
                numeric_pipeline,
                numeric_columns
            ),

            (
                "categorical",
                categorical_pipeline,
                categorical_columns
            )
        ]
    )


    return preprocessing_pipeline


# ==========================================
# TRAIN MODELS
# ==========================================

def train_models():

    print("\n")
    print("=" * 50)
    print("ROAD ACCIDENT SEVERITY ML TRAINING")
    print("=" * 50)


    # ======================================
    # LOAD DATA
    # ======================================

    df = load_data()


    print(
        "\nDataset shape:",
        df.shape
    )


    # ======================================
    # PREPARE DATA
    # ======================================

    X, y = prepare_data(df)


    print(
        "\nNumber of features:",
        X.shape[1]
    )


    print(
        "\nFinal features:"
    )

    for column in X.columns:

        print(
            " -",
            column
        )


    # ======================================
    # TARGET DISTRIBUTION
    # ======================================

    print(
        "\nTarget distribution:"
    )

    print(
        y.value_counts()
    )


    # ======================================
    # TRAIN TEST SPLIT
    # ======================================

    X_train, X_test, y_train, y_test = train_test_split(

        X,
        y,

        test_size=0.20,

        random_state=42,

        stratify=y
    )


    # ======================================
    # PREPROCESSING
    # ======================================

    preprocessing_pipeline = (
        create_preprocessing_pipeline(X)
    )


    # ======================================
    # MODELS
    # ======================================

    models = {

        "Logistic Regression":
            LogisticRegression(
                max_iter=2000
            ),

        "Decision Tree":
            DecisionTreeClassifier(
                random_state=42
            ),

        "Random Forest":
            RandomForestClassifier(
                n_estimators=200,

                random_state=42,

                n_jobs=-1
            )
    }


    results = {}


    best_model_name = None

    best_pipeline = None

    best_f1 = -1


    # ======================================
    # TRAIN EACH MODEL
    # ======================================

    for model_name, model in models.items():

        print(
            f"\nTraining {model_name}..."
        )


        pipeline = Pipeline(

            steps=[

                (
                    "preprocessing",
                    preprocessing_pipeline
                ),

                (
                    "model",
                    model
                )
            ]
        )


        pipeline.fit(
            X_train,
            y_train
        )


        predictions = pipeline.predict(
            X_test
        )


        # ==================================
        # METRICS
        # ==================================

        accuracy = accuracy_score(
            y_test,
            predictions
        )


        precision = precision_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0
        )


        recall = recall_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0
        )


        f1 = f1_score(

            y_test,

            predictions,

            average="weighted",

            zero_division=0
        )


        results[model_name] = {

            "accuracy": accuracy,

            "precision": precision,

            "recall": recall,

            "f1_score": f1
        }


        print(
            f"Accuracy  : {accuracy:.4f}"
        )

        print(
            f"Precision : {precision:.4f}"
        )

        print(
            f"Recall    : {recall:.4f}"
        )

        print(
            f"F1 Score  : {f1:.4f}"
        )


        # ==================================
        # BEST MODEL
        # ==================================

        if f1 > best_f1:

            best_f1 = f1

            best_model_name = model_name

            best_pipeline = pipeline


    # ======================================
    # MODEL COMPARISON
    # ======================================

    print("\n")

    print(
        "=" * 50
    )

    print(
        "MODEL COMPARISON"
    )

    print(
        "=" * 50
    )


    for model_name, metrics in results.items():

        print(
            f"\n{model_name}"
        )

        print(
            f"Accuracy  : "
            f"{metrics['accuracy']:.4f}"
        )

        print(
            f"Precision : "
            f"{metrics['precision']:.4f}"
        )

        print(
            f"Recall    : "
            f"{metrics['recall']:.4f}"
        )

        print(
            f"F1 Score  : "
            f"{metrics['f1_score']:.4f}"
        )


    print(
        "\nBest Model:",
        best_model_name
    )


    # ======================================
    # SAVE MODEL
    # ======================================

    model_path = os.path.join(

        MODEL_DIR,

        "severity_model.pkl"
    )


    joblib.dump(

        best_pipeline,

        model_path
    )


    print(
        "\nModel saved at:"
    )

    print(
        model_path
    )


    # ======================================
    # SAVE PREPROCESSING PIPELINE
    # ======================================

    preprocessing_path = os.path.join(

        MODEL_DIR,

        "preprocessing_pipeline.pkl"
    )


    joblib.dump(

        best_pipeline.named_steps[
            "preprocessing"
        ],

        preprocessing_path
    )


    print(
        "\nPreprocessing pipeline saved at:"
    )

    print(
        preprocessing_path
    )


    # ======================================
    # SAVE MODEL RESULTS
    # ======================================

    results_df = pd.DataFrame(
        results
    ).T


    results_path = os.path.join(

        BASE_DIR,

        "model_results.csv"
    )


    results_df.to_csv(

        results_path
    )


    print(
        "\nModel comparison saved at:"
    )

    print(
        results_path
    )


    return best_pipeline


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    train_models()