from pydantic import BaseModel
from typing import Optional


class PredictionRequest(BaseModel):

    Time: Optional[str] = None

    Day_of_week: Optional[str] = None

    Age_band_of_driver: Optional[str] = None

    Sex_of_driver: Optional[str] = None

    Educational_level: Optional[str] = None

    Vehicle_driver_relation: Optional[str] = None

    Driving_experience: Optional[str] = None

    Type_of_vehicle: Optional[str] = None

    Owner_of_vehicle: Optional[str] = None

    Service_year_of_vehicle: Optional[str] = None

    Defect_of_vehicle: Optional[str] = None

    Area_accident_occured: Optional[str] = None

    Lanes_or_Medians: Optional[str] = None

    Road_allignment: Optional[str] = None

    Types_of_Junction: Optional[str] = None

    Road_surface_type: Optional[str] = None

    Road_surface_conditions: Optional[str] = None

    Light_conditions: Optional[str] = None

    Weather_conditions: Optional[str] = None

    Type_of_collision: Optional[str] = None

    Number_of_vehicles_involved: Optional[float] = None

    Vehicle_movement: Optional[str] = None
