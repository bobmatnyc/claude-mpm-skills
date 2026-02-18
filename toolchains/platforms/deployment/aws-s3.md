# S3 Operations

Common S3 bucket and object operations.

## Bucket Management

```bash
# Create bucket
aws s3 mb s3://my-bucket --region us-east-1

# List buckets
aws s3 ls

# Delete bucket (must be empty)
aws s3 rb s3://my-bucket --force
```

## Object Operations

```bash
# Upload file
aws s3 cp file.txt s3://bucket/path/

# Download file
aws s3 cp s3://bucket/file.txt ./local/

# Sync directory
aws s3 sync ./local-dir s3://bucket/remote-dir/

# List objects
aws s3 ls s3://bucket/path/ --recursive
```

## Lifecycle Policies

```bash
# Create lifecycle policy (transition to Glacier after 90 days)
aws s3api put-bucket-lifecycle-configuration \
  --bucket my-bucket \
  --lifecycle-configuration '{
    "Rules": [{
      "Id": "archive-old-files",
      "Status": "Enabled",
      "Transitions": [{
        "Days": 90,
        "StorageClass": "GLACIER"
      }]
    }]
  }'
```

## Bucket Policies

```bash
# Make bucket public (be careful!)
aws s3api put-bucket-policy --bucket my-bucket --policy '{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": "*",
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::my-bucket/*"
  }]
}'

# Block all public access
aws s3api put-public-access-block \
  --bucket my-bucket \
  --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true
```
