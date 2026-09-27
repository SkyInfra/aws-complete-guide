import boto3
from datetime import datetime, timezone

DRY_RUN = True
MAX_AGE_DAYS = 30
PROTECTED_TAG_KEY = "Retention"
PROTECTED_TAG_VALUE = "Keep"


def lambda_handler(event, context):

    ec2 = boto3.client('ec2')

    response = ec2.describe_snapshots(
        OwnerIds=['self']
    )

    snapshots = response['Snapshots']

    stale_snapshots = []
    eligible_snapshots = []
    protected_snapshots = []

    print(f"Total snapshots found: {len(snapshots)}")

    for snapshot in snapshots:

        snapshot_id = snapshot['SnapshotId']
        volume_id = snapshot.get('VolumeId')
        start_time = snapshot['StartTime']
        tags = snapshot.get('Tags', [])

        snapshot_age = (
            datetime.now(timezone.utc) - start_time
        ).days

        print(f"\nChecking snapshot: {snapshot_id}")
        print(f"Source volume: {volume_id}")
        print(f"Snapshot age: {snapshot_age} days")

        # Check for protection tag
        is_protected = any(
            tag['Key'] == PROTECTED_TAG_KEY
            and tag['Value'] == PROTECTED_TAG_VALUE
            for tag in tags
        )

        if is_protected:

            protected_snapshots.append(snapshot_id)

            print(
                f"PROTECTED: Snapshot has "
                f"{PROTECTED_TAG_KEY}={PROTECTED_TAG_VALUE}"
            )

            continue

        if not volume_id:

            print("No source volume information found.")
            continue

        try:

            volume_response = ec2.describe_volumes(
                VolumeIds=[volume_id]
            )

            if volume_response['Volumes']:

                print(
                    f"ACTIVE: Source volume {volume_id} exists."
                )

        except ec2.exceptions.ClientError as e:

            if e.response['Error']['Code'] == 'InvalidVolume.NotFound':

                stale_snapshots.append(snapshot_id)

                print(
                    f"STALE: Source volume {volume_id} "
                    f"no longer exists."
                )

                if snapshot_age >= MAX_AGE_DAYS:

                    eligible_snapshots.append(snapshot_id)

                    print(
                        f"ELIGIBLE: Snapshot is older than "
                        f"{MAX_AGE_DAYS} days."
                    )

                    if not DRY_RUN:

                        ec2.delete_snapshot(
                            SnapshotId=snapshot_id
                        )

                        print(
                            f"DELETED: Snapshot {snapshot_id}"
                        )

                    else:

                        print(
                            f"DRY RUN: Would delete "
                            f"snapshot {snapshot_id}"
                        )

                else:

                    print(
                        f"KEEP: Snapshot is only "
                        f"{snapshot_age} days old."
                    )

            else:

                print(f"Error checking volume: {e}")

    print("\n========== SUMMARY ==========")

    print(f"Total snapshots: {len(snapshots)}")
    print(f"Stale snapshots: {len(stale_snapshots)}")
    print(f"Protected snapshots: {len(protected_snapshots)}")
    print(f"Eligible snapshots: {len(eligible_snapshots)}")
    print(f"Dry run: {DRY_RUN}")

    return {
        'statusCode': 200,
        'body': {
            'total_snapshots': len(snapshots),
            'stale_snapshots': len(stale_snapshots),
            'protected_snapshots': len(protected_snapshots),
            'eligible_snapshots': len(eligible_snapshots),
            'dry_run': DRY_RUN
        }
    }