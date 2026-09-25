# LAPD Crime Data Analysis
# Data preprocessing, feature engineering, encoding, and exploratory data analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")


# LOAD DATASET
# ============================================================

# Place the dataset inside the data folder before running this script
data = pd.read_csv(r"data/Crime_Data_from_2020_to_Present.csv")



# INITIAL DATA INSPECTION
# ==========================================================

data.head()
data.tail()
data.info()

# Check unique values
data.nunique()



# MISSING VALUE ANALYSIS
# ============================================================

data.isnull().sum()
(data.isnull().sum()/(len(data)))*100




# HANDLE MISSING VALUES
# ============================================================

# Crm Cd 2, 3 and 4 contain more than 90% missing values,
# so these columns are dropped.
data = data.drop(columns=["Crm Cd 2", "Crm Cd 3", "Crm Cd 4"])

# Missing weapon values are treated as incidents where no weapon was recorded
data["Weapon Used Cd"] = data["Weapon Used Cd"].fillna(0)
data["Weapon Desc"] = data["Weapon Desc"].fillna("No Weapon")

# Replace missing victim information with "Unknown".
data["Vict Sex"] = data["Vict Sex"].fillna("Unknown")
data["Vict Descent"] = data["Vict Descent"].fillna("Unknown")

# Replace missing Mocode values with "None"
data["Mocodes"] = data["Mocodes"].fillna("None")

# Fill missing premise information with the mode.
data["Premis Cd"] = data["Premis Cd"].fillna(data["Premis Cd"].mode()[0])
data["Premis Desc"] = data["Premis Desc"].fillna(data["Premis Desc"].mode()[0])

# Cross Street contains a large percentage of missing values,
# so the column is dropped
data = data.drop(columns=["Cross Street"])

# Recheck missing values
(data.isnull().sum() / len(data)) * 100

# Descriptive statistics
data.describe()



# FEATURE ENGINEERING of DATE REPORTED
# ============================================================

data["Date Rptd"] = pd.to_datetime(data["Date Rptd"])

data["Day"] = data["Date Rptd"].dt.day
data["Month"] = data["Date Rptd"].dt.month
data["Year"] = data["Date Rptd"].dt.year
data["Time"] = data["Date Rptd"].dt.strftime("%I:%M:%S")
data["AM_PM"] = data["Date Rptd"].dt.strftime("%p")



# FEATURE ENGINEERING of DATE OCCURRED
# ============================================================

data["DATE OCC"] = pd.to_datetime(data["DATE OCC"])

data["OCC_Day"] = data["DATE OCC"].dt.day
data["OCC_Month"] = data["DATE OCC"].dt.month
data["OCC_Year"] = data["DATE OCC"].dt.year
data["OCC_Time"] = data["DATE OCC"].dt.strftime("%I:%M:%S")
data["OCC_AM_PM"] = data["DATE OCC"].dt.strftime("%p")



# FEATURE ENGINEERING of TIME OF OCCURRENCE
# ============================================================

# TIME OCC convert it to a four digit
# so values such as 900 become 0900.
data["TIME OCC"] = data["TIME OCC"].astype(str).str.zfill(4)

time_values = pd.to_datetime(
    data["TIME OCC"],
    format="%H%M",
    errors="coerce"
)


# Creating day of week
data["day_of_week"] = data["DATE OCC"].dt.day_name()

#Create Hour
# here we use the already cleaned TIME OCC values to obtain the hour.
data["Hour"] = pd.to_datetime(
    data["TIME OCC"],
    format="%H%M",
    errors="coerce"
).dt.hour



# CREATE PART OF DAY
# ============================================================

def part_of_day(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 21:
        return "Evening"
    else:
        return "Night"


data["Part_of_Day"] = data["Hour"].apply(part_of_day)


# ENCODING
# ============================================================

# Encode area name and victim sex for better ML
data = pd.get_dummies(
    data,
    columns=["Vict Sex"],
    drop_first=True
)

data.info()



# EXPLORATORY DATA ANALYSIS
# ============================================================

# TOP 10 CRIME TYPES BY FREQUENCY
# ============================================================
top_crimes = data["Crm Cd Desc"].value_counts().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(
    x=top_crimes.values,
    y=top_crimes.index,
    palette="viridis"
)
plt.title("Top 10 Crime Types by Frequency")
plt.xlabel("Number of Incidents")
plt.ylabel("Crime Type")
plt.show()



# MONTHLY CRIME TRENDS
# ============================================================

monthly_trends = data.groupby(
    data["DATE OCC"].dt.to_period("M")
).size()

monthly_trends.plot(
    figsize=(12, 6),
    marker="o"
)

plt.title("Monthly Crime Trends")
plt.xlabel("Month")
plt.ylabel("Number of Crimes")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()



# CRIME HEATMAP BY HOUR AND DAY OF WEEK
# ============================================================

data["Day_of_Week_Num"] = data["DATE OCC"].dt.weekday

heatmap_data = data.pivot_table(
    index="Hour",
    columns="Day_of_Week_Num",
    aggfunc="size",
    fill_value=0
)

plt.figure(figsize=(12, 6))
sns.heatmap(heatmap_data, cmap="YlOrRd")
plt.title("Crime Heatmap by Hour and Day of Week")
plt.xlabel("Day of Week (0=Monday)")
plt.ylabel("Hour of Day")
plt.tight_layout()
plt.show()


# TOP 10 AREAS BY CRIME COUNT
# ============================================

area_counts = data["AREA NAME"].value_counts().head(10)

plt.figure(figsize=(10, 6))

sns.barplot(
    x=area_counts.values,
    y=area_counts.index
)

plt.title("Top 10 Crime Areas")
plt.xlabel("Crimes")
plt.ylabel("Area")
plt.show()


# FILTERING AND SORTING
# ============================================

def filter_crimes(
    df,
    start_hour=None, end_hour=None,
    months=None,
    victim_sex=None,
    age_range=None,
    crime_types=None
):
    filtered = df.copy()
    if start_hour is not None and end_hour is not None:
        filtered = filtered[(filtered['Hour'] >= start_hour) & (filtered['Hour'] <= end_hour)]
    if months is not None:
        filtered = filtered[filtered['Month'].isin(months)]
    if victim_sex is not None:
        sex_cols = [f'Vict Sex_{sex}' for sex in victim_sex if f'Vict Sex_{sex}' in filtered.columns]
        if sex_cols:
            filtered = filtered[filtered[sex_cols].any(axis=1)]
    if age_range is not None:
        filtered = filtered[
            (filtered['Vict Age'] >= age_range[0]) &
            (filtered['Vict Age'] <= age_range[1])
        ]
    if crime_types is not None:
        filtered = filtered[filtered['Crime_Category'].isin(crime_types)]
    return filtered




#there are 140 types of crimes. it is way too much and will complex this analysis. so we decided to create new crime categoris like whole summary of crime types turn to few categories.
                       
#here is how I create those new categories. 
def map_crime_category(crime):
    crime = crime.upper()
    if any(x in crime for x in ['THEFT', 'STOLEN', 'BURGLARY FROM VEHICLE', 'SHOPLIFTING', 'PURSE', 'EMBEZZLEMENT', 'TILL TAP', 'COIN MACHINE']):
        return 'Theft'
    elif any(x in crime for x in ['ASSAULT', 'BATTERY', 'RAPE', 'SEX', 'CHILD ABUSE', 'CRIMINAL THREATS']):
        return 'Assault'
    elif any(x in crime for x in ['BURGLARY', 'ROBBERY', 'ATTEMPTED ROBBERY', 'VEHICLE - ATTEMPT STOLEN']):
        return 'Burglary / Robbery'
    elif any(x in crime for x in ['VANDALISM', 'PROPERTY', 'ARSON', 'ILLEGAL DUMPING', 'DISRUPT SCHOOL']):
        return 'Vandalism / Property Damage'
    elif any(x in crime for x in ['FIREARMS', 'WEAPON', 'SHOTS FIRED', 'BRANDISH']):
        return 'Firearms / Weapons'
    elif any(x in crime for x in ['CHILD PORNOGRAPHY', 'HUMAN TRAFFICKING', 'PANDERING', 'INCEST', 'LEWD', 'SEXUAL']):
        return 'Sex Crimes / Exploitation'
    elif any(x in crime for x in ['FRAUD', 'EMBEZZLEMENT', 'FORGERY', 'COUNTERFEIT', 'DISHONEST EMPLOYEE', 'INSURANCE FRAUD']):
        return 'Fraud / White Collar'
    else:
        return 'Other / Miscellaneous'

    

# APPLY MAPPING
# =====================================================

data['Crime_Category'] = data['Crm Cd Desc'].apply(map_crime_category)
print(data['Crime_Category'].value_counts())



# APPLY FILTERS
# ======================================================

filtered_df = filter_crimes(
    data,
    start_hour=8,
    end_hour=18,
    months=[1, 2, 3],
    victim_sex=['F'],
    crime_types=['Assault', 'Theft']
)


# CRIME CATEGORY FREQUENCY
# ========================================================
crime_counts = filtered_df['Crime_Category'].value_counts()
print(crime_counts)


