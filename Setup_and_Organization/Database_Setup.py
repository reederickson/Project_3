## Importing Stuff to help with splitting initial CSV
import pandas as pd
import numpy as np

## Importing Stuff to help create datbase
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text, inspect, func
from sqlalchemy import Column, Integer, String, Float, ForeignKey

from sqlalchemy.orm import declarative_base
Base = declarative_base()

## Initial Database tables setup

## Creating the database
engine = create_engine('sqlite:///Resources/database.sqlite')



class Sleep(Base):
    __tablename__ = 'sleep'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id))
    sleep_duration = Column(Float)
    sleep_quality = Column(Integer)
    sleep_disorder_id = Column(Integer)

class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id))
    activity_level = Column(Integer)
    daily_steps = Column(Integer)

class Gender(Base):
    __tablename__ = 'gender'
    id = Column(Integer, primary_key=True)
    gender_name = Column(String(12))

class Occupation(Base):
    __tablename__ = 'occupation'
    id = Column(Integer, primary_key=True)
    occupation_name = Column(String(30))

class BMI(Base):
    __tablename__ = 'bmi'
    id = Column(Integer, primary_key=True)
    bmi_name = Column(String(20))

class Health(Base):
    __tablename__ = 'health'
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey(Person.id))
    blood_pressure = Column(String(12))
    stress_level = Column(Integer)
    heart_rate = Column(Integer)
    systolic = Column(Integer)
    diastolic = Column(Integer)
    bmi_id = Column(Integer, ForeignKey(BMI.id))

class SleepDisorder(Base):
    __tablename__ = 'sleep_disorder'
    id = Column(Integer, primary_key=True)
    sleep_disorder_name = Column(String(20))

## Working with pandas to split the initial CSV into their respective tables
df = pd.read_csv("Resources/Sleep_health_and_lifestyle_dataset.csv")

## Creating what the person table will look like before transforming
person = df[["Person ID", "Gender", "Age", "Occupation"]]

## Creating the gender table csv and table in SQL
gender_list = list(df["Gender"].unique())
gender_dict = {"id": [i for i in range(len(gender_list))], "gender_name": [i for i in gender_list]}
gender = pd.DataFrame(gender_dict)
gender.to_csv("Resources/Database_CSVs/gender.csv", index = False)
gender.to_sql(name = "gender", con = engine, if_exists= "replace")

## Creating the occupation table csv and table in SQL
occupation_list = list(df["Occupation"].unique())
occupation_dict = {"id": [i for i in range(len(occupation_list))], "occupation_name": [i for i in occupation_list]}
occupation = pd.DataFrame(occupation_dict)
occupation.to_csv("Resources/Database_CSVs/occupation.csv", index = False)
occupation.to_sql(name = "occupation", con = engine, if_exists = "replace")

## Creating the person table csv and table in SQL
person_gender_occupation = person.merge(gender, left_on = "Gender",right_on = "gender_name", how = "inner")\
    .merge(occupation, left_on = "Occupation", right_on = "occupation_name", how = "inner")
person_cleaned = person_gender_occupation[["Person ID", "id_x", "Age", "id_y"]]\
    .rename(columns = {"Person ID": "id", "id_x": "gender_id", "Age": "age", "id_y": "occupation_id"})
person_cleaned.to_csv("Resources/Database_CSVs/person.csv", index = False)
person_cleaned.to_sql(name = "person", con = engine, if_exists= "replace")

## Creating the sleep_disorder table csv and table in SQL
df["Sleep Disorder"].fillna(value = "None", axis = 0, inplace = True)
sleep_disorder_list = list(df["Sleep Disorder"].unique())
sleep_disorder_dict = {"id": [i for i in range(len(sleep_disorder_list))], "sleep_disorder_name": [i for i in sleep_disorder_list]}
sleep_disorder = pd.DataFrame(sleep_disorder_dict)
sleep_disorder.to_csv("Resources/Database_CSVs/sleep_disorder.csv", index = False)
sleep_disorder.to_sql(name = "sleep_disorder", con = engine, if_exists = "replace")

## Creating the sleep table csv and table in SQL
sleep_df = df[["Person ID", "Sleep Duration", "Quality of Sleep", "Sleep Disorder"]]
sleep_cleaned = sleep_df.merge(sleep_disorder, left_on = "Sleep Disorder", right_on = "sleep_disorder_name", how = "inner")
sleep = sleep_cleaned[["Person ID", "Sleep Duration", "Quality of Sleep", "id"]].reset_index()\
    .rename(columns = {"index": "id", "Person ID": "person_id", "Sleep Duration": "sleep_duration", "Quality of Sleep": "sleep_quality", "id": "sleep_disorder_id"})
sleep.to_csv("Resources/Database_CSVs/sleep.csv", index = False)
sleep.to_sql(name = "sleep", con = engine, if_exists = "replace")

## Creating the activity table csv and table in SQL
activity_df = df[["Person ID", "Physical Activity Level", "Daily Steps"]].reset_index()\
    .rename(columns = {"index": "id", "Person ID": "person_id", "Physical Activity Level": "activity_level", "Daily Steps": "daily_steps"})
activity_df.to_csv("Resources/Database_CSVs/activity.csv", index = False)
activity_df.to_sql(name = "activity", con = engine, if_exists = "replace")

## Creating the bmi table csv and table in SQL
df["BMI Category"] = np.where(df["BMI Category"] == "Normal Weight", "Normal", df["BMI Category"])
bmi_list = list(df["BMI Category"].unique())
bmi_dict = {"id": [i for i in range(len(bmi_list))], "bmi_name": [i for i in bmi_list]}
bmi_df = pd.DataFrame(bmi_dict)
bmi_df.to_csv("Resources/Database_CSVs/bmi.csv", index = False)
bmi_df.to_sql(name = "bmi", con = engine, if_exists = "replace")

## Creating the health table csv and table in SQL
df[["Systolic", "Diastolic"]] = df["Blood Pressure"].str.split("/", expand = True)
df[["Systolic", "Diastolic"]] = df[["Systolic", "Diastolic"]].astype({"Systolic": "int64", "Diastolic": "int64"})
health_df = df[["Person ID", "BMI Category", "Blood Pressure", "Stress Level", "Heart Rate", "Systolic", "Diastolic"]]
health_cleaned = health_df.merge(bmi_df, left_on = "BMI Category", right_on = "bmi_name", how = "inner")
health = health_cleaned[["Person ID", "Blood Pressure", "Stress Level", "Heart Rate", "Systolic", "Diastolic", "id"]].reset_index()\
    .rename(columns = {"index": "id", 
                       "Person ID": "person_id",
                       "Blood Pressure": "blood_pressure",
                       "Stress Level": "stress_level",
                       "Heart Rate": "heart_rate",
                       "Systolic": "systolic",
                       "Diastolic": "diastolic",
                       "id": "bmi_id"
                       })    
health.to_csv("Resources/Database_CSVs/health.csv", index = False)
health.to_sql(name = "health", con = engine, if_exists = "replace")

## Closing the connection to the database
engine.dispose()