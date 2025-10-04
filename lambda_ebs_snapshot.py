import boto3
import datetime

ec2 = boto3.client('ec2')

# Replace with your EBS Volume ID (you can find it in EC2 -> Volumes)
VOLUME_ID = 'vol-01ba32065156e3882'  # Example: vol-0a1b2c3d4e5f6g7h8

def lambda_handler(event, context):
    now = datetime.datetime.now(datetime.timezone.utc)

    # 1️⃣ Create a new snapshot
    snapshot = ec2.create_snapshot(
        VolumeId=VOLUME_ID,
        Description=f'Automated snapshot taken on {now.date()}'
    )
    snapshot_id = snapshot['SnapshotId']
    print(f'✅ Created snapshot ID: {snapshot_id}')

    # 2️⃣ Describe all snapshots of this volume
    snapshots = ec2.describe_snapshots(
        Filters=[
            {'Name': 'volume-id', 'Values': [VOLUME_ID]},
            {'Name': 'owner-id', 'Values': ['self']}
        ]
    )['Snapshots']

    # 3️⃣ Delete snapshots older than 30 days
    retention_days = 30
    deleted_count = 0
    for snap in snapshots:
        start_time = snap['StartTime']
        snap_id = snap['SnapshotId']
        age_days = (now - start_time).days

        if age_days > retention_days:
            ec2.delete_snapshot(SnapshotId=snap_id)
            print(f'🗑️ Deleted snapshot {snap_id} ({age_days} days old)')
            deleted_count += 1

    return {
        'statusCode': 200,
        'body': f'Snapshot {snapshot_id} created. Deleted {deleted_count} old snapshots.'
    }
