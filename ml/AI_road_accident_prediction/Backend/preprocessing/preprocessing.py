import pandas as pd
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAW_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "road_accident_data.csv"
)

PROCESSED_DATA_PATH = os.path.join(
    BASE_DIR,
    "data",
    "processed",
    "processed_accident_data.csv"
)


def load_dataset():

    if not os.path.exists(RAW_DATA_PATH):
        raise FileNotFoundError(
            f"Dataset not found at: {RAW_DATA_PATH}"
        )

    df = pd.read_csv(RAW_DATA_PATH)

    return df


def clean_dataset(df):

    # Clean column names
    df.columns = df.columns.str.strip()

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Clean string values
    object_columns = df.select_dtypes(
        include=["object"]
    ).columns

    for column in object_columns:

        df[column] = df[column].apply(
            lambda value:
            value.strip()
            if isinstance(value, str)
            else value
        )

    # Replace '?' with NaN
    df = df.replace("?", pd.NA)

    return df


def save_processed_dataset(df):

    os.makedirs(
        os.path.dirname(PROCESSED_DATA_PATH),
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )


def preprocess_dataset():

    print("Loading dataset...")

    df = load_dataset()

    print("Original dataset shape:", df.shape)

    df = clean_dataset(df)

    print("Cleaned dataset shape:", df.shape)

    print("\nMissing values:")
    print(df.isnull().sum())

    save_processed_dataset(df)

    print(
        "\nProcessed dataset saved successfully at:"
    )

    print(PROCESSED_DATA_PATH)

    return df


if __name__ == "__main__":

    preprocess_dataset()
