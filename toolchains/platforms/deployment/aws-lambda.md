# Lambda Function Deployment

Patterns for deploying and managing AWS Lambda functions.

## Create Function

```bash
# Create function from zip
aws lambda create-function \
  --function-name MyFunction \
  --runtime python3.11 \
  --role arn:aws:iam::123456789:role/lambda-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 30 \
  --memory-size 256
```

## Update Function

```bash
# Update code
aws lambda update-function-code \
  --function-name MyFunction \
  --zip-file fileb://function.zip

# Update configuration
aws lambda update-function-configuration \
  --function-name MyFunction \
  --timeout 60 \
  --environment Variables={KEY1=value1,KEY2=value2}
```

## Invoke Function

```bash
# Synchronous invoke
aws lambda invoke \
  --function-name MyFunction \
  --payload '{"key":"value"}' \
  response.json

# View logs
aws logs tail /aws/lambda/MyFunction --follow
```

## Environment Variables

```bash
# Set environment variables
aws lambda update-function-configuration \
  --function-name MyFunction \
  --environment Variables={DB_HOST=localhost,DB_PORT=5432}
```

## Layers

```bash
# Create layer
aws lambda publish-layer-version \
  --layer-name my-layer \
  --zip-file fileb://layer.zip \
  --compatible-runtimes python3.11

# Add layer to function
aws lambda update-function-configuration \
  --function-name MyFunction \
  --layers arn:aws:lambda:region:account:layer:my-layer:1
```
