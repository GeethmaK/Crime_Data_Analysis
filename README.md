LAPD Crime Data Analysis

1. Overview 

This project analyses a large Los Angeles crime dataset using Python. The dataset contains more than 1 million crime records and 28 original columns.

The project focuses on:

- Data inspection and understanding
- Missing-value analysis and handling
- Feature engineering
- Date and time analysis
- Categorical encoding
- Exploratory data analysis (EDA)
- Crime frequency visualization
- Monthly crime trends
- Crime patterns by hour and day of the week
- Crime areas



2. Dataset

This project uses the Los Angeles Police Department Crime Data from 2020 to Present dataset. The dataset contains reported crime incidents in Los Angeles including information about crime type, date and time of occurrence, location, victim characteristics, weapon information and other incident details.

The dataset was preprocessed before analysis by handling missing values, removing columns with excessive missing data and converting date and time fields into useful analytical features.

Note: The original dataset is not included in this repository due to its size. Please download the dataset separately and place it inside the data/ folder using the expected filename.



3. Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn



4. Project Workflow

### 1. Data Loading and Inspection

The dataset is loaded with Pandas and inspected using functions such as `head()`, `tail()`, `info()`, `nunique()`, and `describe()`.

The original dataset contains **1,004,991 records and 28 columns**.

### 2. Missing Value Handling

Missing values were analyzed as percentages before deciding how to handle them.

The project uses the following approach:

- `Crm Cd 2`, `Crm Cd 3`, and `Crm Cd 4` are removed because of their very high percentage of missing values.
- Missing weapon values are represented as `0` and `"No Weapon"`.
- Missing victim sex and descent values are represented as `"Unknown"`.
- Missing Mocode values are represented as `"None"`.
- Missing premise values are filled using the mode.
- `Cross Street` is removed because of its high percentage of missing values.

### 3. Feature Engineering

Date related features are created from both the reported date and occurrence date.

The project creates features including:

- Day
- Month
- Year
- Time
- AM/PM
- Occurrence day
- Occurrence month
- Occurrence year
- Occurrence time
- Occurrence AM/PM
- Hour
- Day of week
- Part of day

The part of day is divided into:

- Morning
- Afternoon
- Evening
- Night

### 4. Encoding

`AREA NAME` and `Vict Sex` are converted into numerical indicator columns using Pandas one-hot encoding with `drop_first=True`.

### 5. Exploratory Data Analysis

The analysis includes:

- Top 10 crime types by frequency
- Monthly crime trends
- Crime frequency by hour and day of the week using a heatmap
_ Top 10 crime areas




5. Visualization

The project uses data visualization to explore crime patterns and trends across different dimensions.

The main visualizations include

Top 10 Crime Types by Frequency – identifies the most frequently reported crime types.
Top 10 Areas by Crime Count – shows the areas with the highest number of reported incidents.
Monthly Crime Trends – examines how crime frequency changes over time.
Crime Heatmap by Hour and Day of Week – visualizes the distribution of crime incidents across different hours and days.




6. Crime Categorization 

The original dataset contains a large number of individual crime descriptions, which can make broader analysis more difficult. To simplify the analysis, the individual crime descriptions were grouped into broader categories based on relevant keywords.

The project creates the following categories:

Theft
Assault
Burglary / Robbery
Vandalism / Property Damage
Firearms / Weapons
Sex Crimes / Exploitation
Fraud / White Collar
Other / Miscellaneous

A custom Python function was developed to assign each original crime description to one of these broader categories. These categories were then used for further filtering and frequency analysis.




7. How to Run

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd LAPD-Crime-Data-Analysis
```

### 2. Install the required libraries

```bash
pip install -r requirements.txt
```

### 3. Add the dataset

Place the CSV dataset inside:

```text
data/
```

### 4. Run the analysis

```bash
python LAPD_Crime_Analysis.py
```



8. Repository Structure

```text
LAPD-Crime-Data-Analysis/
│
├── data/
│   └── README.md
│
├── images/
│   └── Top 10 crime types by frequency
│   └── Monthly crime trends
│   └── Heatmap of crime frequency by hour and day of week
│   └── Top 10 crime areas
│
├── LAPD_Crime_Analysis.py
├── README.md
├── requirements.txt
│   └── matplotlib
│   └── pandas
│   └── seaborn
│   └── numpy
└── .gitignore
```



9. Skills Demonstrated

This project demonstrates practical experience with:

- Python programming
- Pandas
- NumPy
- Data cleaning
- Missing-value handling
- Feature engineering
- Date/time processing
- Categorical encoding
- Exploratory data analysis
- Data visualisation
- Large dataset handling




Note

This repository presents the analysis approach used for the academic project while cleaning the original working code into a reproducible format.
