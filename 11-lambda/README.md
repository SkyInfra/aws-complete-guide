# Stale EBS Snapshot Cleaner

## Purpose

This Lambda function identifies EBS snapshots whose original EBS volumes no longer exist.

It is designed as a starting point for AWS cost-optimization automation.

## Logic

The function:

1. Retrieves EBS snapshots owned by the AWS account.
2. Reads the `VolumeId` associated with each snapshot.
3. Checks whether that EBS volume still exists.
4. If AWS returns `InvalidVolume.NotFound`, the snapshot is considered stale.
5. The stale snapshot information is returned and printed to CloudWatch Logs.

## Important

This version only **detects** stale snapshots.

It does not automatically delete them.

Automatic deletion should be implemented carefully because a snapshot may still be required for backup, recovery, compliance, or other operational purposes.

## AWS Services

- AWS Lambda
- Amazon EC2
- Amazon EBS
- Amazon CloudWatch
- IAM

## Python SDK

The function uses `boto3` to communicate with AWS services.