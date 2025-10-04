# AWS Lambda: Automatic EBS Snapshot and Cleanup

## Overview

This AWS Lambda function automates the creation of EBS snapshots for a specified volume and cleans up snapshots older than 30 days. It helps maintain backups while managing storage costs by removing aged snapshots.

---

## Step-by-Step Process

### 1. IAM Role Setup

- Created an IAM role named `LambdaEC2SnapshotRole` for Lambda.
- Attached the **AmazonEC2FullAccess** managed policy to allow snapshot creation and deletion.

### 2. Lambda Function Creation

- Created a Lambda function named `EC2SnapshotAndCleanup` with Python 3.x runtime.
- Assigned the IAM role `LambdaEC2SnapshotRole` to this function.
- Implemented Python code using Boto3 to:
  - Create a snapshot for a specific EBS volume.
  - List and delete snapshots older than 30 days.

### 3. Permissions and Configuration

- Increased Lambda timeout to at least 1 minute for sufficient execution time.
- Set memory to 128 MB (default) which was sufficient for this task.

### 4. Testing

- Replaced the placeholder `VOLUME_ID` with the actual volume ID from the AWS EC2 Console.
- Manually triggered Lambda function with an empty test event `{}`.
- Checked CloudWatch logs confirming snapshot creation and cleanup actions.
- Verified snapshots in the EC2 Console.

---

## Usage Instructions

1. Update `VOLUME_ID` in the code with your EBS volume ID.
2. Ensure Lambda has the appropriate IAM role with EC2 full access.
3. Deploy the function and configure timeout and memory if needed.
4. Trigger manually or schedule execution via CloudWatch Events.
5. Monitor CloudWatch logs for detailed processing messages.

---

## Code Snippet

snapshot = ec2.create_snapshot(
    VolumeId=VOLUME_ID,
    Description=f'Automated snapshot taken on {now.date()}'
)
snapshot_id = snapshot['SnapshotId']
print(f'Created snapshot ID: {snapshot_id}')

snapshots = ec2.describe_snapshots(
    Filters=[
        {'Name': 'volume-id', 'Values': [VOLUME_ID]},
        {'Name': 'owner-id', 'Values': ['self']}
    ]
)['Snapshots']

retention_days = 30
for snap in snapshots:
    start_time = snap['StartTime']
    age = (now - start_time).days
    snap_id = snap['SnapshotId']
    if age > retention_days:
        ec2.delete_snapshot(SnapshotId=snap_id)
        print(f'Deleted snapshot {snap_id} aged {age} days')

return {
    'statusCode': 200,
    'body': f'Snapshot {snapshot_id} created and old snapshots cleaned up.'
}

---

## Screenshots

Attach screenshots of the following for documentation:

- Lambda function code in AWS Console.
- Execution logs from CloudWatch showing snapshot creation and deletion.
- EC2 Console snapshots page showing the recent snapshot.

---

## Summary

This automation ensures regular snapshots of critical EBS volumes are created and old backups are cleaned up, optimizing storage and backup policies using AWS Lambda and Boto3.

# AWS Lambda: Automatic EBS Snapshot and Cleanup

## Overview

This Lambda function automates creating snapshots of a specified EBS volume and deletes snapshots older than 30 days to manage backup retention and storage costs.

---

## Steps Followed

1. Created an IAM role (`LambdaEC2SnapshotRole`) with the **AmazonEC2FullAccess** policy attached.
2. Created a Lambda function (`EC2SnapshotAndCleanup`) with the Python 3.x runtime, assigned the above role.
3. Replaced `VOLUME_ID` in the code with the actual EBS volume ID.
4. Increased Lambda timeout to at least 1 minute.
5. Tested the Lambda function with a manual test event `{}` and verified snapshot creation and cleanup.
6. Checked CloudWatch logs and EC2 console snapshots for verification.

---

## How to Use

- Update the `VOLUME_ID` variable in the code.
- Assign a role with EC2 full access permissions.
- Deploy and invoke manually or attach a schedule with CloudWatch Events.
- Monitor logs and snapshot states regularly.

---

## Lambda Code Snippet

snapshot = ec2.create_snapshot(
    VolumeId=VOLUME_ID,
    Description=f'Automated snapshot taken on {now.date()}'
)
snapshot_id = snapshot['SnapshotId']
print(f'Created snapshot ID: {snapshot_id}')

snapshots = ec2.describe_snapshots(
    Filters=[
        {'Name': 'volume-id', 'Values': [VOLUME_ID]},
        {'Name': 'owner-id', 'Values': ['self']}
    ]
)['Snapshots']

retention_days = 30
for snap in snapshots:
    start_time = snap['StartTime']
    age = (now - start_time).days
    snap_id = snap['SnapshotId']
    if age > retention_days:
        ec2.delete_snapshot(SnapshotId=snap_id)
        print(f'Deleted snapshot {snap_id} aged {age} days')

return {
    'statusCode': 200,
    'body': f'Snapshot {snapshot_id} created and old snapshots cleaned up.'
}

---

## Screenshots

Add screenshots showing:

- Lambda function code in AWS Console.
- CloudWatch logs showing snapshot creation and deletion.
- EC2 snapshots dashboard showing your snapshots.

---

## Summary

This function helps automate the backup of EC2 volumes and manages retention by deleting old snapshots automatically, which saves storage cost and improves operational efficiency.
s