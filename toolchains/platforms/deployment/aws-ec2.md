# EC2 Instance Management

Common EC2 operations and patterns for managing AWS instances.

## Launch Instance

```bash
# Launch from AMI
aws ec2 run-instances \
  --image-id ami-xxx \
  --instance-type t3.micro \
  --key-name my-key \
  --security-group-ids sg-xxx \
  --subnet-id subnet-xxx \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=MyServer}]'
```

## Instance States

```bash
# List instances with state
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,Tags[?Key==`Name`].Value|[0]]' --output table

# Start/stop/terminate
aws ec2 start-instances --instance-ids i-xxx
aws ec2 stop-instances --instance-ids i-xxx
aws ec2 terminate-instances --instance-ids i-xxx
```

## Security Groups

```bash
# List security groups
aws ec2 describe-security-groups

# Add inbound rule
aws ec2 authorize-security-group-ingress \
  --group-id sg-xxx \
  --protocol tcp \
  --port 22 \
  --cidr 10.0.0.0/8
```

## Instance Connect

```bash
# SSH via Systems Manager (no key needed)
aws ssm start-session --target i-xxx

# Traditional SSH
ssh -i my-key.pem ec2-user@instance-ip
```
