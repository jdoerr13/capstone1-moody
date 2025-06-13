import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Load & clean Loads your dataset and drops any rows with missing values. STEP 4: Preprocessing CLEANING THE DATA
df = pd.read_csv("ml/weather_mood_dataset.csv").dropna()

# STEP 3: Feature Engineering- choosing only the inputs that showed meaningful trends in your earlier scatterplots. Select which columns are useful 
X = df[['temperature_f', 'air_pressure_hpa']]
y = df['mood_score']

# STEP 4:  Scale features : Each column has a mean of 0 and a standard deviation of 1. This is important because many ML models (like linear regression, neural networks) are sensitive to feature scale
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# STEP 4: Train/test split  You split into training and test sets:
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)
