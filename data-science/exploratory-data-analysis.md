# Exploratory Data Analysis (EDA) Workflow

## Purpose
Systematic approach to understanding datasets through statistical analysis and visualization before modeling.

## When to Use
- Starting a new data science project
- Understanding data quality and distributions
- Identifying patterns, outliers, and relationships
- Formulating hypotheses for modeling

## Step-by-Step Workflow

### 1. Initial Data Inspection
```python
import pandas as pd
import numpy as np

# Load data
df = pd.read_csv('data.csv')

# Basic information
print(f"Shape: {df.shape}")
print(f"\\nColumn Types:\\n{df.dtypes}")
print(f"\\nMemory Usage:\\n{df.memory_usage(deep=True)}")
print(f"\\nMissing Values:\\n{df.isnull().sum()}")
print(f"\\nDuplicate Rows: {df.duplicated().sum()}")
```

### 2. Descriptive Statistics
```python
# Numerical columns
print(df.describe())

# Include percentiles
print(df.describe(percentiles=[.01, .05, .25, .5, .75, .95, .99]))

# Categorical columns
for col in df.select_dtypes(include=['object']).columns:
    print(f"\\n{col}:")
    print(df[col].value_counts())
    print(f"Unique values: {df[col].nunique()}")
```

### 3. Distribution Analysis
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Histograms for numerical features
df.select_dtypes(include=[np.number]).hist(
    bins=30, figsize=(15, 10), edgecolor='black'
)
plt.tight_layout()
plt.show()

# Box plots for outlier detection
numeric_cols = df.select_dtypes(include=[np.number]).columns
n_cols = 3
n_rows = (len(numeric_cols) + n_cols - 1) // n_cols

fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, n_rows * 4))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    df.boxplot(column=col, ax=axes[i])
    axes[i].set_title(f'{col} Distribution')

plt.tight_layout()
plt.show()
```

### 4. Correlation Analysis
```python
# Correlation matrix
corr_matrix = df.select_dtypes(include=[np.number]).corr()

# Heatmap
plt.figure(figsize=(12, 10))
sns.heatmap(
    corr_matrix,
    annot=True,
    fmt='.2f',
    cmap='coolwarm',
    center=0,
    square=True,
    linewidths=1
)
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.show()

# High correlations (excluding diagonal)
high_corr = []
for i in range(len(corr_matrix.columns)):
    for j in range(i+1, len(corr_matrix.columns)):
        if abs(corr_matrix.iloc[i, j]) > 0.7:
            high_corr.append({
                'feature1': corr_matrix.columns[i],
                'feature2': corr_matrix.columns[j],
                'correlation': corr_matrix.iloc[i, j]
            })

print("\\nHigh Correlations (|r| > 0.7):")
for item in high_corr:
    print(f"{item['feature1']} <-> {item['feature2']}: {item['correlation']:.3f}")
```

### 5. Categorical vs Target Analysis
```python
def analyze_categorical_vs_target(df, cat_col, target_col):
    """Analyze relationship between categorical feature and target."""
    # Count plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

    # Distribution
    df[cat_col].value_counts().plot(kind='bar', ax=ax1)
    ax1.set_title(f'{cat_col} Distribution')
    ax1.set_xlabel(cat_col)
    ax1.set_ylabel('Count')

    # vs Target
    pd.crosstab(df[cat_col], df[target_col], normalize='index').plot(
        kind='bar', stacked=True, ax=ax2
    )
    ax2.set_title(f'{cat_col} vs {target_col}')
    ax2.set_xlabel(cat_col)
    ax2.set_ylabel('Proportion')
    ax2.legend(title=target_col)

    plt.tight_layout()
    plt.show()

    # Chi-square test
    from scipy.stats import chi2_contingency
    contingency_table = pd.crosstab(df[cat_col], df[target_col])
    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    print(f"Chi-square test: χ² = {chi2:.3f}, p-value = {p_value:.4f}")

# Example usage
# for col in df.select_dtypes(include=['object']).columns:
#     analyze_categorical_vs_target(df, col, 'target')
```

### 6. Missing Data Analysis
```python
def analyze_missing_data(df):
    """Comprehensive missing data analysis."""
    missing = df.isnull().sum()
    missing_pct = (missing / len(df)) * 100

    missing_df = pd.DataFrame({
        'Column': missing.index,
        'Missing_Count': missing.values,
        'Missing_Percentage': missing_pct.values
    })
    missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values(
        'Missing_Count', ascending=False
    )

    print("Missing Data Summary:")
    print(missing_df.to_string(index=False))

    # Visualize
    if not missing_df.empty:
        plt.figure(figsize=(12, 6))
        plt.barh(missing_df['Column'], missing_df['Missing_Percentage'])
        plt.xlabel('Missing Percentage (%)')
        plt.title('Missing Data by Feature')
        plt.tight_layout()
        plt.show()

    return missing_df

missing_analysis = analyze_missing_data(df)
```

### 7. Outlier Detection
```python
def detect_outliers_iqr(df, column):
    """Detect outliers using IQR method."""
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]

    print(f"\\n{column}:")
    print(f"  Lower bound: {lower_bound:.2f}")
    print(f"  Upper bound: {upper_bound:.2f}")
    print(f"  Outliers: {len(outliers)} ({len(outliers)/len(df)*100:.2f}%)")

    return outliers

# Check all numeric columns
for col in df.select_dtypes(include=[np.number]).columns:
    outliers = detect_outliers_iqr(df, col)
```

## EDA Checklist

- [ ] Load data and check shape
- [ ] Check data types and memory usage
- [ ] Identify missing values
- [ ] Check for duplicates
- [ ] Descriptive statistics (mean, median, std, etc.)
- [ ] Distribution plots (histograms, KDE)
- [ ] Outlier detection (box plots, IQR)
- [ ] Correlation analysis
- [ ] Categorical feature analysis
- [ ] Target variable distribution
- [ ] Feature vs target relationships
- [ ] Document data quality issues
- [ ] Identify features for engineering
- [ ] Note assumptions and limitations

## Common Insights to Look For

1. **Data Quality**
   - Missing data patterns
   - Duplicate records
   - Data type inconsistencies
   - Invalid values

2. **Distributions**
   - Skewness (may need transformation)
   - Outliers (may need handling)
   - Multimodal distributions (potential subgroups)

3. **Relationships**
   - Strong correlations (feature selection)
   - Non-linear relationships (feature engineering)
   - Categorical associations (chi-square)

4. **Target Variable**
   - Class balance (classification)
   - Range and scale (regression)
   - Separability from features

## Next Steps After EDA

1. **Data Cleaning**
   - Handle missing values
   - Remove or cap outliers
   - Fix data type issues

2. **Feature Engineering**
   - Create derived features
   - Transform skewed features
   - Encode categorical variables
   - Scale numerical features

3. **Feature Selection**
   - Remove highly correlated features
   - Keep most informative features
   - Consider domain knowledge

4. **Modeling**
   - Choose appropriate algorithms
   - Set up validation strategy
   - Define evaluation metrics
