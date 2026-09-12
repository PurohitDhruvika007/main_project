import os
import joblib
import pandas as pd


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# ============================================================
# MODEL PATH
# ============================================================

MODEL_PATH = os.path.join(
    BASE_DIR,
    "model",
    "severity_model.pkl"
)


# ============================================================
# EXPECTED FEATURES
# ============================================================

EXPECTED_FEATURES = [

    "Time",

    "Day_of_week",

    "Age_band_of_driver",

    "Sex_of_driver",

    "Educational_level",

    "Vehicle_driver_relation",

    "Driving_experience",

    "Type_of_vehicle",

    "Owner_of_vehicle",

    "Service_year_of_vehicle",

    "Defect_of_vehicle",

    "Area_accident_occured",

    "Lanes_or_Medians",

    "Road_allignment",

    "Types_of_Junction",

    "Road_surface_type",

    "Road_surface_conditions",

    "Light_conditions",

    "Weather_conditions",

    "Type_of_collision",

    "Number_of_vehicles_involved",

    "Vehicle_movement"
]


# ============================================================
# LOAD MODEL
# ============================================================

def load_model():

    if not os.path.exists(MODEL_PATH):

        raise FileNotFoundError(
            "Trained model not found. "
            "Please run train_model.py first."
        )

    return joblib.load(MODEL_PATH)


# ============================================================
# RISK LEVEL
# ============================================================

def calculate_risk_level(
    predicted_class,
    risk_score
):

    class_text = str(
        predicted_class
    ).lower()

    # Fatal injury
    if (
        "fatal" in class_text
        or "death" in class_text
    ):

        return "HIGH"

    # Serious injury
    if (
        "serious" in class_text
        or "severe" in class_text
    ):

        return "MEDIUM"

    # Risk score based classification
    if risk_score >= 75:

        return "HIGH"

    elif risk_score >= 50:

        return "MEDIUM"

    else:

        return "LOW"


# ============================================================
# SAFETY RECOMMENDATIONS
# ============================================================

def generate_recommendations(
    data,
    risk_level
):

    recommendations = []

    # --------------------------------------------------------
    # GET INPUT VALUES
    # --------------------------------------------------------

    weather = str(
        data.get(
            "Weather_conditions",
            ""
        )
    ).lower()

    road_condition = str(
        data.get(
            "Road_surface_conditions",
            ""
        )
    ).lower()

    light = str(
        data.get(
            "Light_conditions",
            ""
        )
    ).lower()

    driving_experience = str(
        data.get(
            "Driving_experience",
            ""
        )
    ).lower()

    vehicle_movement = str(
        data.get(
            "Vehicle_movement",
            ""
        )
    ).lower()

    defect = str(
        data.get(
            "Defect_of_vehicle",
            ""
        )
    ).lower()

    junction = str(
        data.get(
            "Types_of_Junction",
            ""
        )
    ).lower()

    collision = str(
        data.get(
            "Type_of_collision",
            ""
        )
    ).lower()

    road_surface = str(
        data.get(
            "Road_surface_type",
            ""
        )
    ).lower()

    vehicles = data.get(
        "Number_of_vehicles_involved"
    )

    # ========================================================
    # WEATHER RECOMMENDATIONS
    # ========================================================

    if (
        "rain" in weather
        or "wet" in road_condition
    ):

        recommendations.append(
            "Drive slowly because rain and wet road conditions "
            "can reduce tyre grip and visibility."
        )

        recommendations.append(
            "Maintain a longer following distance and avoid "
            "sudden braking or sharp turns."
        )

    elif (
        "fog" in weather
        or "mist" in weather
    ):

        recommendations.append(
            "Reduce your speed in foggy or misty conditions "
            "and maintain sufficient visibility distance."
        )

        recommendations.append(
            "Use appropriate headlights and avoid sudden "
            "lane changes."
        )

    elif (
        "cloudy" in weather
        or "overcast" in weather
    ):

        recommendations.append(
            "Maintain a safe speed and remain alert because "
            "visibility may be reduced."
        )

    # ========================================================
    # ROAD SURFACE
    # ========================================================

    if (
        "wet" in road_condition
        or "damp" in road_condition
    ):

        recommendations.append(
            "Increase the distance from the vehicle ahead "
            "because wet roads require more braking distance."
        )

    if (
        "earth" in road_surface
        or "gravel" in road_surface
    ):

        recommendations.append(
            "Drive carefully on uneven or unpaved surfaces "
            "and reduce speed when necessary."
        )

    # ========================================================
    # DARKNESS / LOW LIGHT
    # ========================================================

    if (
        "darkness" in light
        or "night" in light
    ):

        recommendations.append(
            "Reduce speed in low-light conditions and use "
            "headlights appropriately."
        )

        recommendations.append(
            "Stay alert for pedestrians, motorcycles and "
            "vehicles that may be difficult to see."
        )

    # ========================================================
    # DRIVING EXPERIENCE
    # ========================================================

    if (
        "no licence" in driving_experience
        or "no license" in driving_experience
    ):

        recommendations.append(
            "Do not drive without a valid driving licence. "
            "Ensure the driver is legally authorised to operate the vehicle."
        )

    elif (
        "below 1yr" in driving_experience
        or "below 1" in driving_experience
        or "1-2yr" in driving_experience
    ):

        recommendations.append(
            "Drivers with limited experience should maintain "
            "a lower speed and avoid risky manoeuvres."
        )

    # ========================================================
    # VEHICLE DEFECT
    # ========================================================

    if (
        defect
        and defect not in [
            "nan",
            "no defect",
            "none",
            ""
        ]
    ):

        recommendations.append(
            "Get the vehicle inspected before travelling "
            "because a reported vehicle defect may increase risk."
        )

    # ========================================================
    # JUNCTION
    # ========================================================

    if (
        junction
        and junction != "no junction"
        and junction != "nan"
    ):

        recommendations.append(
            "Approach the junction carefully, reduce speed "
            "and check surrounding traffic before proceeding."
        )

    # ========================================================
    # VEHICLE MOVEMENT
    # ========================================================

    if "overtak" in vehicle_movement:

        recommendations.append(
            "Avoid unnecessary overtaking, especially when "
            "visibility or road conditions are poor."
        )

    if (
        "turn" in vehicle_movement
        or "right" in vehicle_movement
        or "left" in vehicle_movement
    ):

        recommendations.append(
            "Signal early and check surrounding traffic "
            "carefully before changing direction."
        )

    # ========================================================
    # NUMBER OF VEHICLES
    # ========================================================

    try:

        if (
            vehicles is not None
            and float(vehicles) >= 3
        ):

            recommendations.append(
                "Maintain extra space around your vehicle "
                "because multiple vehicles are involved in this scenario."
            )

    except (ValueError, TypeError):

        pass

    # ========================================================
    # COLLISION CONDITION
    # ========================================================

    if (
        "vehicle with vehicle" in collision
        or "collision" in collision
    ):

        recommendations.append(
            "Maintain a safe following distance and stay "
            "alert to sudden movements from nearby vehicles."
        )

    # ========================================================
    # GENERAL RISK RECOMMENDATION
    # ========================================================

    if risk_level == "HIGH":

        recommendations.append(
            "High-risk conditions detected. Reduce speed, "
            "stay focused and follow all traffic rules."
        )

    elif risk_level == "MEDIUM":

        recommendations.append(
            "Moderate-risk conditions detected. Drive defensively "
            "and maintain a safe distance from other vehicles."
        )

    else:

        recommendations.append(
            "Continue following speed limits, traffic rules "
            "and safe-driving practices."
        )

    # ========================================================
    # REMOVE DUPLICATES
    # ========================================================

    unique_recommendations = []

    for recommendation in recommendations:

        if recommendation not in unique_recommendations:

            unique_recommendations.append(
                recommendation
            )

    return unique_recommendations


# ============================================================
# MAIN PREDICTION FUNCTION
# ============================================================

def make_prediction(input_data):

    # --------------------------------------------------------
    # LOAD MODEL
    # --------------------------------------------------------

    model = load_model()

    # --------------------------------------------------------
    # CREATE DATAFRAME
    # --------------------------------------------------------

    df = pd.DataFrame(
        [input_data]
    )

    # --------------------------------------------------------
    # ENSURE ALL FEATURES EXIST
    # --------------------------------------------------------

    for feature in EXPECTED_FEATURES:

        if feature not in df.columns:

            df[feature] = None

    # --------------------------------------------------------
    # KEEP ONLY EXPECTED FEATURES
    # --------------------------------------------------------

    df = df[
        EXPECTED_FEATURES
    ]

    # --------------------------------------------------------
    # REPLACE EMPTY VALUES
    # --------------------------------------------------------

    df = df.replace(
        "",
        None
    )

    # --------------------------------------------------------
    # CONVERT NUMBER OF VEHICLES
    # --------------------------------------------------------

    if (
        "Number_of_vehicles_involved"
        in df.columns
    ):

        df[
            "Number_of_vehicles_involved"
        ] = pd.to_numeric(
            df[
                "Number_of_vehicles_involved"
            ],
            errors="coerce"
        )

    # ========================================================
    # PREDICTION
    # ========================================================

    prediction = model.predict(
        df
    )[0]

    # ========================================================
    # PROBABILITY
    # ========================================================

    probability = model.predict_proba(
        df
    )[0]

    probability_list = (
        probability.tolist()
    )

    # --------------------------------------------------------
    # HIGHEST PROBABILITY
    # --------------------------------------------------------

    max_probability = max(
        probability_list
    )

    risk_score = round(
        max_probability * 100,
        2
    )

    # --------------------------------------------------------
    # PROBABILITY INDEX
    # --------------------------------------------------------

    predicted_class_index = (
        probability_list.index(
            max_probability
        )
    )

    predicted_class = (
        model.classes_[
            predicted_class_index
        ]
    )

    # ========================================================
    # RISK LEVEL
    # ========================================================

    risk_level = calculate_risk_level(
        predicted_class,
        risk_score
    )

    # ========================================================
    # SEVERITY PROBABILITIES
    # ========================================================

    probability_result = {}

    for (
        class_name,
        probability_value
    ) in zip(
        model.classes_,
        probability
    ):

        probability_result[
            str(class_name)
        ] = round(
            float(
                probability_value
            ) * 100,
            2
        )

    # ========================================================
    # RECOMMENDATIONS
    # ========================================================

    recommendations = (
        generate_recommendations(
            input_data,
            risk_level
        )
    )

    # ========================================================
    # FINAL RESPONSE
    # ========================================================

    return {

        "severity": str(
            prediction
        ),

        "risk_level": risk_level,

        "risk_score": risk_score,

        "probabilities":
            probability_result,

        "recommendations":
            recommendations
    }
