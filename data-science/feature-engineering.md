# Feature Engineering Techniques

## Purpose
Create new features or transform existing ones to improve model performance and capture domain knowledge.

## When to Use
- After EDA when you understand the data
- When domain knowledge suggests derived features
- When baseline model performance is insufficient
- Before final model training

## Core Principles

1. **Start Simple**: Test features incrementally
2. **Domain Knowledge**: Leverage what you know about the problem
3. **Validate Impact**: Measure if feature improves model
4. **Avoid Leakage**: Only use information available at prediction time

## Common Techniques

### 1. Handling Missing Values

```python
import pandas as pd
import numpy as np

# Strategy A: Simple Imputation
df['age'].fillna(df['age'].median(), inplace=True)

# Strategy B: Create Missing Indicator
df['age_missing'] = df['age'].isnull().astype(int)
df['age'].fillna(df['age'].median(), inplace=True)

# Strategy C: Forward/Backward Fill (time series)
df['value'].fillna(method='ffill', inplace=True)

# Strategy D: Model-based Imputation
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

imputer = IterativeImputer(random_state=42)
df_imputed = pd.DataFrame(
    imputer.fit_transform(df),
    columns=df.columns
)
```

### 2. Encoding Categorical Variables

```python
# Technique A: One-Hot Encoding (nominal categories)
df_encoded = pd.get_dummies(
    df,
    columns=['color', 'size'],
    prefix=['color', 'size'],
    drop_first=True  # Avoid multicollinearity
)

# Technique B: Label Encoding (ordinal categories)
from sklearn.preprocessing import LabelEncoder

education_order = ['high_school', 'bachelors', 'masters', 'phd']
df['education_encoded'] = df['education'].map({
    val: i for i, val in enumerate(education_order)
})

# Technique C: Target Encoding (high cardinality)
def target_encode(train_df, test_df, column, target):
    """Encode categorical variable by target mean."""
    # Calculate means on training data
    means = train_df.groupby(column)[target].mean()
    global_mean = train_df[target].mean()

    # Apply to both sets
    train_df[f'{column}_encoded'] = train_df[column].map(means)
    test_df[f'{column}_encoded'] = test_df[column].map(means).fillna(global_mean)

    return train_df, test_df

# Technique D: Frequency Encoding
freq = df['city'].value_counts(normalize=True)
df['city_freq'] = df['city'].map(freq)
```

### 3. Numerical Transformations

```python
# Log Transform (for right-skewed data)
df['price_log'] = np.log1p(df['price'])  # log1p handles zeros

# Square Root Transform
df['area_sqrt'] = np.sqrt(df['area'])

# Box-Cox Transform (requires positive values)
from scipy import stats
df['income_boxcox'], lambda_param = stats.boxcox(df['income'])

# Binning (discretization)
df['age_bin'] = pd.cut(
    df['age'],
    bins=[0, 18, 35, 50, 65, 100],
    labels=['child', 'young_adult', 'middle_age', 'senior', 'elderly']
)

# Quantile Binning (equal-sized bins)
df['income_quantile'] = pd.qcut(
    df['income'],
    q=4,
    labels=['Q1', 'Q2', 'Q3', 'Q4']
)
```

### 4. Feature Scaling

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler

# Standard Scaling (mean=0, std=1)
scaler = StandardScaler()
df[['age', 'income']] = scaler.fit_transform(df[['age', 'income']])

# Min-Max Scaling (range 0-1)
scaler = MinMaxScaler()
df[['age', 'income']] = scaler.fit_transform(df[['age', 'income']])

# Robust Scaling (robust to outliers)
scaler = RobustScaler()
df[['age', 'income']] = scaler.fit_transform(df[['age', 'income']])
```

### 5. Interaction Features

```python
# Multiplication
df['area_per_room'] = df['total_area'] / df['num_rooms']
df['price_per_sqft'] = df['price'] / df['sqft']

# Polynomial Features
from sklearn.preprocessing import PolynomialFeatures

poly = PolynomialFeatures(degree=2, include_bias=False)
features = ['age', 'income']
poly_features = poly.fit_transform(df[features])

# Get feature names
feature_names = poly.get_feature_names_out(features)
df_poly = pd.DataFrame(poly_features, columns=feature_names)

# Ratio Features
df['debt_to_income'] = df['debt'] / df['income']
df['dependents_ratio'] = df['num_dependents'] / df['household_size']
```

### 6. Date/Time Features

```python
# Convert to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract components
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['dayofweek'] = df['date'].dt.dayofweek
df['quarter'] = df['date'].dt.quarter
df['is_weekend'] = df['dayofweek'].isin([5, 6]).astype(int)

# Time-based features
df['hour'] = df['timestamp'].dt.hour
df['is_business_hours'] = df['hour'].between(9, 17).astype(int)

# Time since event
df['days_since_registration'] = (df['current_date'] - df['registration_date']).dt.days

# Cyclical encoding (for periodic features)
df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12)
df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12)
```

### 7. Text Features

```python
# String length
df['name_length'] = df['name'].str.len()
df['description_length'] = df['description'].str.len()

# Word count
df['description_words'] = df['description'].str.split().str.len()

# Contains pattern
df['has_special_chars'] = df['name'].str.contains('[^a-zA-Z0-9]').astype(int)

# TF-IDF (for text data)
from sklearn.feature_extraction.text import TfidfVectorizer

tfidf = TfidfVectorizer(max_features=100)
tfidf_features = tfidf.fit_transform(df['description'])
tfidf_df = pd.DataFrame(
    tfidf_features.toarray(),
    columns=tfidf.get_feature_names_out()
)
```

### 8. Aggregation Features

```python
# Group statistics
df['avg_price_by_category'] = df.groupby('category')['price'].transform('mean')
df['count_by_category'] = df.groupby('category')['id'].transform('count')

# Rolling statistics (time series)
df['price_rolling_mean_7d'] = df['price'].rolling(window=7).mean()
df['price_rolling_std_7d'] = df['price'].rolling(window=7).std()

# Expanding statistics
df['cumulative_sales'] = df.groupby('customer_id')['sales'].transform('cumsum')
df['transaction_count'] = df.groupby('customer_id').cumcount() + 1
```

### 9. Domain-Specific Features

```python
# E-commerce example
df['cart_value_per_item'] = df['cart_value'] / df['num_items']
df['avg_item_price'] = df['total_price'] / df['quantity']
df['is_bulk_order'] = (df['quantity'] > 10).astype(int)

# Finance example
df['credit_utilization'] = df['credit_used'] / df['credit_limit']
df['debt_service_ratio'] = df['monthly_debt_payment'] / df['monthly_income']
df['liquidity_ratio'] = df['liquid_assets'] / df['current_liabilities']

# Healthcare example
df['bmi'] = df['weight'] / (df['height'] / 100) ** 2
df['is_obese'] = (df['bmi'] >= 30).astype(int)
df['age_bmi_interaction'] = df['age'] * df['bmi']
```

## Feature Selection

### 1. Remove Low Variance Features

```python
from sklearn.feature_selection import VarianceThreshold

# Remove features with < 1% variance
selector = VarianceThreshold(threshold=0.01)
X_selected = selector.fit_transform(X)

# Get selected feature names
selected_features = X.columns[selector.get_support()]
```

### 2. Remove Correlated Features

```python
def remove_correlated_features(df, threshold=0.95):
    """Remove features with correlation above threshold."""
    corr_matrix = df.corr().abs()

    # Upper triangle of correlations
    upper = corr_matrix.where(
        np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
    )

    # Find features with correlation > threshold
    to_drop = [column for column in upper.columns
               if any(upper[column] > threshold)]

    print(f"Removing {len(to_drop)} correlated features: {to_drop}")
    return df.drop(columns=to_drop)

df_reduced = remove_correlated_features(df, threshold=0.95)
```

### 3. Feature Importance (Tree-based)

```python
from sklearn.ensemble import RandomForestClassifier

# Train model
rf = RandomForestClassifier(random_state=42)
rf.fit(X_train, y_train)

# Get importances
importances = pd.DataFrame({
    'feature': X_train.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

# Select top features
threshold = 0.01  # Keep features with > 1% importance
important_features = importances[importances['importance'] > threshold]['feature']
X_train_selected = X_train[important_features]
```

### 4. Recursive Feature Elimination

```python
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression

# Select top 10 features
rfe = RFE(LogisticRegression(), n_features_to_select=10)
rfe.fit(X_train, y_train)

# Get selected features
selected_features = X_train.columns[rfe.support_]
print(f"Selected features: {list(selected_features)}")
```

## Feature Engineering Workflow

```python
def create_features(df, is_training=True):
    """Complete feature engineering pipeline."""
    df = df.copy()

    # 1. Handle missing values
    df['age'] = df['age'].fillna(df['age'].median())

    # 2. Create datetime features
    df['date'] = pd.to_datetime(df['date'])
    df['month'] = df['date'].dt.month
    df['is_weekend'] = df['date'].dt.dayofweek.isin([5, 6]).astype(int)

    # 3. Create interaction features
    df['price_per_unit'] = df['price'] / df['quantity']

    # 4. Encode categorical variables
    df = pd.get_dummies(df, columns=['category'], drop_first=True)

    # 5. Scale numerical features (only fit on training)
    if is_training:
        global scaler
        scaler = StandardScaler()
        df[['age', 'income']] = scaler.fit_transform(df[['age', 'income']])
    else:
        df[['age', 'income']] = scaler.transform(df[['age', 'income']])

    return df

# Usage
X_train_eng = create_features(X_train, is_training=True)
X_test_eng = create_features(X_test, is_training=False)
```

## Best Practices

1. **Document Features**
   - Keep track of feature definitions
   - Document rationale and domain logic

2. **Validate Impact**
   - Test each feature's contribution
   - Use cross-validation

3. **Avoid Leakage**
   - No future information
   - Fit transformers on training data only

4. **Start Simple**
   - Add complexity incrementally
   - Measure improvement at each step

5. **Domain Knowledge**
   - Leverage expert knowledge
   - Create meaningful interactions

## Common Mistakes

1. **Data Leakage**
   - ❌ Fit on full dataset
   - ✅ Fit on training set only

2. **Too Many Features**
   - Can lead to overfitting
   - Use feature selection

3. **Ignoring Feature Correlation**
   - Multicollinearity issues
   - Remove highly correlated features

4. **Not Handling Outliers**
   - Can skew transformations
   - Use robust methods or cap values

5. **Forgetting to Scale**
   - Important for distance-based models
   - Use appropriate scaling method

## Checklist

- [ ] Handle missing values appropriately
- [ ] Encode categorical variables
- [ ] Transform skewed numerical features
- [ ] Create interaction features
- [ ] Extract datetime components
- [ ] Add domain-specific features
- [ ] Scale numerical features
- [ ] Remove low-variance features
- [ ] Remove highly correlated features
- [ ] Validate feature impact
- [ ] Document all transformations
- [ ] Ensure no data leakage

## Measuring Feature Impact

```python
from sklearn.model_selection import cross_val_score

def evaluate_feature_impact(X, y, feature_name, cv=5):
    """Measure impact of adding a feature."""
    # Without feature
    X_without = X.drop(columns=[feature_name])
    scores_without = cross_val_score(
        RandomForestClassifier(),
        X_without, y,
        cv=cv,
        scoring='f1'
    )

    # With feature
    scores_with = cross_val_score(
        RandomForestClassifier(),
        X, y,
        cv=cv,
        scoring='f1'
    )

    print(f"Feature: {feature_name}")
    print(f"Without: {scores_without.mean():.4f} (+/- {scores_without.std()*2:.4f})")
    print(f"With:    {scores_with.mean():.4f} (+/- {scores_with.std()*2:.4f})")
    print(f"Improvement: {(scores_with.mean() - scores_without.mean()):.4f}")

# Test each new feature
evaluate_feature_impact(X_train_eng, y_train, 'price_per_unit')
```
