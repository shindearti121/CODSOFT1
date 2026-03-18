import pandas as pd
import sys

def main():
    file_path = 'IMDb Movies India.csv'
    try:
        # Load the dataset
        print(f"Loading {file_path}...")
        df = pd.read_csv(file_path, encoding='iso-8859-1')
        print(f"Original Shape: {df.shape}")
        
        # 1. Clean Year
        df['Year'] = df['Year'].astype(str).str.extract(r'(\d{4})').astype(float)
        
        # 2. Clean Duration
        df['Duration'] = df['Duration'].astype(str).str.extract(r'(\d+)').astype(float)
        
        # 3. Clean Votes
        df['Votes'] = df['Votes'].astype(str).str.replace(',', '', regex=False)
        df['Votes'] = pd.to_numeric(df['Votes'], errors='coerce')
        
        # 4. Handle Missing Values
        print("Missing values before cleaning:")
        print(df.isnull().sum())
        
        # Drop rows where 'Name', 'Year', or 'Rating' is missing, as these are critical
        df.dropna(subset=['Name', 'Year', 'Rating'], inplace=True)
        
        print("Missing values after dropping critical NaNs:")
        print(df.isnull().sum())
        print(f"New Shape: {df.shape}")
        
        # Save the dataset
        out_path = 'IMDb Movies India_cleaned.csv'
        df.to_csv(out_path, index=False)
        print(f"Cleaned dataset saved to {out_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
