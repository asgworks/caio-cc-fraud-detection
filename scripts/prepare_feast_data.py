"""
Reprocess fraud detection data while preserving timestamps for Feast
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load raw data
print("Loading raw data...")
train_df = pd.read_csv('../data/raw/fraudTrain.csv', index_col=0)
test_df = pd.read_csv('../data/raw/fraudTest.csv', index_col=0)

print(f"Train shape: {train_df.shape}")
print(f"Test shape: {test_df.shape}")

# Convert timestamp to datetime
train_df['timestamp'] = pd.to_datetime(train_df['trans_date_trans_time'])
test_df['timestamp'] = pd.to_datetime(test_df['trans_date_trans_time'])

# Select features to keep
feature_cols = ['amt', 'city_pop', 'category', 'gender', 'state']
timestamp_cols = ['timestamp', 'trans_num', 'cc_num', 'merchant']
target_col = 'is_fraud'

# Encode categorical variables
print("\nEncoding categorical variables...")
le_category = LabelEncoder()
le_gender = LabelEncoder()
le_state = LabelEncoder()

train_df['category_encoded'] = le_category.fit_transform(train_df['category'])
train_df['gender_encoded'] = le_gender.fit_transform(train_df['gender'])
train_df['state_encoded'] = le_state.fit_transform(train_df['state'])

test_df['category_encoded'] = le_category.transform(test_df['category'])
test_df['gender_encoded'] = le_gender.transform(test_df['gender'])
test_df['state_encoded'] = le_state.transform(test_df['state'])

# Prepare feature columns (with timestamps)
encoded_features = ['amt', 'city_pop', 'category_encoded', 'gender_encoded', 'state_encoded']
all_cols = timestamp_cols + encoded_features

# Create train/test splits WITH timestamps and entity keys
X_train = train_df[all_cols]
y_train = train_df[target_col]

X_test = test_df[all_cols]
y_test = test_df[target_col]

# Save processed data
print("\nSaving processed data with timestamps...")
X_train.to_csv('../data/processed/X_train_with_timestamps.csv', index=False)
y_train.to_csv('../data/processed/y_train.csv', index=False)

X_test.to_csv('../data/processed/X_test_with_timestamps.csv', index=False)
y_test.to_csv('../data/processed/y_test.csv', index=False)

print(f"\n✅ Done! Created files with {len(all_cols)} columns:")
print(f"   - Timestamps: {timestamp_cols}")
print(f"   - Features: {encoded_features}")
print(f"\nX_train shape: {X_train.shape}")
print(f"X_test shape: {X_test.shape}")
print(f"\nFirst few rows:")
print(X_train.head())
