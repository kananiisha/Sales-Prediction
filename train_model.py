import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import joblib

# Load dataset
df = pd.read_csv("big_market_sales_dataset.csv")

# Drop ID columns
df.drop(["Item_ID", "Outlet_ID"], axis=1, inplace=True)

# Separate features and target
X = df.drop("Units_Sold", axis=1)
y = df["Units_Sold"]

# Identify column types
cat_cols = X.select_dtypes(include="object").columns
num_cols = X.select_dtypes(exclude="object").columns

# Preprocessing
preprocessor = ColumnTransformer(
    transformers=[
        ("categorical", OneHotEncoder(drop="first"), cat_cols),
        ("numerical", StandardScaler(), num_cols)
    ]
)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Random Forest Model
rf_model = Pipeline([
    ("preprocessing", preprocessor),
    ("model", RandomForestRegressor(
        n_estimators=150,
        random_state=42,
        n_jobs=-1
    ))
])

# Fit the model
rf_model.fit(X_train, y_train)

# Save the model
joblib.dump(rf_model, "rf_model.pkl")

print("Model trained and saved as rf_model.pkl")