# Machine Learning Pipeline Development

## Purpose
Build reproducible, maintainable ML pipelines using scikit-learn's Pipeline and best practices for model development.

## When to Use
- Training production ML models
- Ensuring reproducibility
- Avoiding data leakage
- Simplifying model deployment
- Enabling hyperparameter tuning

## Core Concepts

### Why Pipelines?
1. **Prevents Data Leakage**: Preprocessing fitted only on training data
2. **Reproducibility**: Same transformations applied consistently
3. **Maintainability**: Single object encapsulates all steps
4. **Deployment**: Easier to serialize and deploy
5. **Hyperparameter Tuning**: Grid/random search across all steps

## Basic Pipeline Structure

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Create pipeline
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Fit (scales training data, then trains model)
pipeline.fit(X_train, y_train)

# Predict (applies same scaling to new data)
y_pred = pipeline.predict(X_test)
```

## Complete ML Pipeline Template

### 1. Imports and Setup
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    roc_curve
)
import joblib

# Set random seed for reproducibility
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
```

### 2. Data Splitting (FIRST STEP!)
```python
# Load data
df = pd.read_csv('data.csv')
X = df.drop('target', axis=1)
y = df['target']

# Split BEFORE any preprocessing
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=RANDOM_SEED,
    stratify=y  # For classification with imbalanced classes
)

print(f"Training set: {X_train.shape[0]} samples")
print(f"Test set: {X_test.shape[0]} samples")
print(f"\\nClass distribution (train):\\n{y_train.value_counts(normalize=True)}")
```

### 3. Feature Engineering (Separate Numeric and Categorical)
```python
# Identify feature types
numeric_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_features = X_train.select_dtypes(include=['object']).columns.tolist()

print(f"Numeric features ({len(numeric_features)}): {numeric_features}")
print(f"Categorical features ({len(categorical_features)}): {categorical_features}")

# Numeric pipeline
numeric_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

# Categorical pipeline
categorical_pipeline = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combine pipelines
preprocessor = ColumnTransformer([
    ('numeric', numeric_pipeline, numeric_features),
    ('categorical', categorical_pipeline, categorical_features)
])
```

### 4. Complete Pipeline with Model
```python
# Full pipeline
full_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=RANDOM_SEED))
])

# Train
full_pipeline.fit(X_train, y_train)

# Predict
y_train_pred = full_pipeline.predict(X_train)
y_test_pred = full_pipeline.predict(X_test)
y_test_proba = full_pipeline.predict_proba(X_test)[:, 1]  # For ROC AUC
```

### 5. Model Evaluation
```python
def evaluate_model(y_true, y_pred, y_proba=None, dataset_name='Test'):
    """Comprehensive model evaluation."""
    print(f"\\n{'='*60}")
    print(f"{dataset_name} Set Evaluation")
    print('='*60)

    # Classification report
    print("\\nClassification Report:")
    print(classification_report(y_true, y_pred))

    # Confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title(f'Confusion Matrix - {dataset_name} Set')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.show()

    # ROC AUC (for binary classification)
    if y_proba is not None and len(np.unique(y_true)) == 2:
        auc = roc_auc_score(y_true, y_proba)
        print(f"\\nROC AUC Score: {auc:.4f}")

        # ROC Curve
        fpr, tpr, thresholds = roc_curve(y_true, y_proba)
        plt.figure(figsize=(8, 6))
        plt.plot(fpr, tpr, label=f'ROC Curve (AUC = {auc:.2f})')
        plt.plot([0, 1], [0, 1], 'k--', label='Random Classifier')
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title(f'ROC Curve - {dataset_name} Set')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

# Evaluate on both sets
evaluate_model(y_train, y_train_pred,
               full_pipeline.predict_proba(X_train)[:, 1],
               'Training')
evaluate_model(y_test, y_test_pred, y_test_proba, 'Test')
```

### 6. Cross-Validation
```python
# K-fold cross-validation
from sklearn.model_selection import cross_validate

scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']

cv_results = cross_validate(
    full_pipeline,
    X_train, y_train,
    cv=5,
    scoring=scoring,
    return_train_score=True,
    n_jobs=-1
)

print("\\nCross-Validation Results:")
for metric in scoring:
    train_scores = cv_results[f'train_{metric}']
    test_scores = cv_results[f'test_{metric}']
    print(f"{metric.upper()}:")
    print(f"  Train: {train_scores.mean():.4f} (+/- {train_scores.std()*2:.4f})")
    print(f"  Val:   {test_scores.mean():.4f} (+/- {test_scores.std()*2:.4f})")
```

### 7. Hyperparameter Tuning
```python
# Define parameter grid
param_grid = {
    'classifier__n_estimators': [100, 200, 300],
    'classifier__max_depth': [10, 20, 30, None],
    'classifier__min_samples_split': [2, 5, 10],
    'classifier__min_samples_leaf': [1, 2, 4]
}

# Grid search with cross-validation
grid_search = GridSearchCV(
    full_pipeline,
    param_grid,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)

print("\\nBest Parameters:")
print(grid_search.best_params_)
print(f"\\nBest CV Score: {grid_search.best_score_:.4f}")

# Evaluate best model
best_pipeline = grid_search.best_estimator_
y_test_pred_tuned = best_pipeline.predict(X_test)
y_test_proba_tuned = best_pipeline.predict_proba(X_test)[:, 1]

evaluate_model(y_test, y_test_pred_tuned, y_test_proba_tuned, 'Test (Tuned)')
```

### 8. Feature Importance
```python
# Get feature importance (for tree-based models)
if hasattr(best_pipeline.named_steps['classifier'], 'feature_importances_'):
    # Get feature names after preprocessing
    numeric_feature_names = numeric_features
    categorical_feature_names = best_pipeline.named_steps['preprocessor'] \\
        .named_transformers_['categorical'] \\
        .named_steps['encoder'] \\
        .get_feature_names_out(categorical_features)

    all_feature_names = list(numeric_feature_names) + list(categorical_feature_names)

    # Get importances
    importances = best_pipeline.named_steps['classifier'].feature_importances_
    feature_importance_df = pd.DataFrame({
        'feature': all_feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)

    # Plot top 20
    plt.figure(figsize=(10, 8))
    top_features = feature_importance_df.head(20)
    plt.barh(top_features['feature'], top_features['importance'])
    plt.xlabel('Importance')
    plt.title('Top 20 Feature Importances')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    print("\\nTop 10 Most Important Features:")
    print(feature_importance_df.head(10).to_string(index=False))
```

### 9. Save Pipeline
```python
# Save the entire pipeline
joblib.dump(best_pipeline, 'model_pipeline.pkl')
print("\\nPipeline saved to 'model_pipeline.pkl'")

# Save feature names and metadata
metadata = {
    'numeric_features': numeric_features,
    'categorical_features': categorical_features,
    'best_params': grid_search.best_params_,
    'cv_score': grid_search.best_score_,
    'test_score': evaluate_model.__code__,  # Replace with actual test scores
    'random_seed': RANDOM_SEED
}
joblib.dump(metadata, 'model_metadata.pkl')
```

### 10. Load and Use Pipeline
```python
# Load pipeline
loaded_pipeline = joblib.load('model_pipeline.pkl')

# Make predictions on new data
new_data = pd.read_csv('new_data.csv')
predictions = loaded_pipeline.predict(new_data)
probabilities = loaded_pipeline.predict_proba(new_data)

print(f"Predictions: {predictions}")
```

## Advanced Pipeline Patterns

### Custom Transformers
```python
from sklearn.base import BaseEstimator, TransformerMixin

class OutlierRemover(BaseEstimator, TransformerMixin):
    """Remove outliers using IQR method."""

    def __init__(self, factor=1.5):
        self.factor = factor

    def fit(self, X, y=None):
        Q1 = X.quantile(0.25)
        Q3 = X.quantile(0.75)
        IQR = Q3 - Q1
        self.lower_bound = Q1 - self.factor * IQR
        self.upper_bound = Q3 + self.factor * IQR
        return self

    def transform(self, X):
        return X.clip(lower=self.lower_bound, upper=self.upper_bound, axis=1)

# Use in pipeline
pipeline_with_outlier_removal = Pipeline([
    ('outlier_remover', OutlierRemover()),
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier())
])
```

## Pipeline Best Practices

1. **Always Split Data First**
   - Split before any preprocessing
   - Prevents data leakage

2. **Use Appropriate Imputation**
   - Median for numeric (robust to outliers)
   - Mode or constant for categorical
   - Consider creating "missing" indicator

3. **Scale After Splitting**
   - Fit scaler on training data only
   - Use pipeline to ensure consistency

4. **Handle Class Imbalance**
   - Stratified sampling
   - class_weight parameter
   - SMOTE (before model, in pipeline)

5. **Cross-Validation**
   - Use pipelines in CV
   - Prevents data leakage in folds

6. **Save Everything**
   - Pipeline (includes preprocessing)
   - Feature names
   - Metadata (params, scores)

## Common Pitfalls

1. **Fitting on Full Dataset**
   - ❌ `scaler.fit(X)`
   - ✅ `scaler.fit(X_train)`

2. **Separate Preprocessing**
   - ❌ Preprocess, then train
   - ✅ Include preprocessing in pipeline

3. **Not Using Stratified Sampling**
   - Can lead to class imbalance in splits

4. **Overfitting to Validation Set**
   - Use separate test set
   - Don't tune on test set

5. **Ignoring Feature Types**
   - Different preprocessing for numeric vs categorical

## Checklist

- [ ] Split data before any preprocessing
- [ ] Identify numeric and categorical features
- [ ] Create preprocessing pipelines
- [ ] Build full pipeline (preprocessing + model)
- [ ] Train on training set only
- [ ] Evaluate on both train and test sets
- [ ] Cross-validation for robust estimates
- [ ] Hyperparameter tuning
- [ ] Feature importance analysis
- [ ] Save pipeline and metadata
- [ ] Document assumptions and limitations

## Next Steps

1. **Model Comparison**: Try multiple algorithms
2. **Ensemble Methods**: Stack or vote models
3. **Feature Selection**: Remove low-importance features
4. **Model Monitoring**: Track performance over time
5. **Deployment**: API endpoint or batch prediction
