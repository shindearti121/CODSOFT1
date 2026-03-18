import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import TargetEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
import joblib

def main():
    print("Loading data...")
    df = pd.read_csv('IMDb Movies India_cleaned.csv')
    
    # Drop rows without rating just in case
    df = df.dropna(subset=['Rating'])
    
    # Features and Target
    X = df[['Year', 'Duration', 'Genre', 'Votes', 'Director', 'Actor 1', 'Actor 2', 'Actor 3']]
    y = df['Rating']
    
    # Preprocessing
    cat_features = ['Genre', 'Director', 'Actor 1', 'Actor 2', 'Actor 3']
    num_features = ['Year', 'Duration', 'Votes']
    
    cat_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
        ('encoder', TargetEncoder(target_type='continuous', smooth="auto"))
    ])
    
    num_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median'))
    ])
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, num_features),
            ('cat', cat_transformer, cat_features)
        ])
    
    # Model
    model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, max_depth=15, random_state=42, n_jobs=-1))
    ])
    
    print("Training model...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model.fit(X_train, y_train)
    
    # Evaluate
    score = model.score(X_test, y_test)
    print(f"R^2 Score on Test Set: {score:.4f}")
    
    # Save
    print("Saving model to model.pkl...")
    joblib.dump(model, 'model.pkl')
    print("Done!")

if __name__ == "__main__":
    main()
