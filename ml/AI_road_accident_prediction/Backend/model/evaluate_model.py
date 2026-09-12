import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)


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

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "severity_model.pkl"
)


def find_target_column(df):

    for column in df.columns:

        if "severity" in column.lower():

            return column

    raise ValueError(
        "Severity column not found."
    )


def evaluate():

    print(
        "Loading dataset..."
    )

    df = pd.read_csv(
        DATA_PATH
    )

    df = df.replace(
        "?",
        pd.NA
    )

    df.columns = df.columns.str.strip()

    target_column = find_target_column(df)

    print(
        "Target:",
        target_column
    )

    df = df.dropna(
        subset=[target_column]
    )

    y = df[target_column].astype(str)

    X = df.drop(
        columns=[target_column]
    )

    columns_to_remove = [
        "Accident_Index",
        "Accident index",
        "accident_index",
        "ID",
        "id",
        "Number_of_casualties",
        "Number_of_Casualties",
        "Casualty_class",
        "Sex_of_casualty",
        "Age_band_of_casualty",
        "Casualty_severity"
    ]

    columns_to_remove = [
        column
        for column in columns_to_remove
        if column in X.columns
    ]

    X = X.drop(
        columns=columns_to_remove
    )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print(
        "\nLoading saved model..."
    )

    model = joblib.load(
        MODEL_PATH
    )

    predictions = model.predict(
        X_test
    )

    print(
        "\n=============================="
    )

    print(
        "MODEL EVALUATION"
    )

    print(
        "=============================="
    )

    print(
        "\nAccuracy:",
        round(
            accuracy_score(
                y_test,
                predictions
            ),
            4
        )
    )

    print(
        "Precision:",
        round(
            precision_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            ),
            4
        )
    )

    print(
        "Recall:",
        round(
            recall_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            ),
            4
        )
    )

    print(
        "F1 Score:",
        round(
            f1_score(
                y_test,
                predictions,
                average="weighted",
                zero_division=0
            ),
            4
        )
    )

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    print(
        "\nConfusion Matrix:"
    )

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )


if __name__ == "__main__":

    evaluate()
