def waiter_for_replication_task_status(replication_task_arn :'str', Region_name: 'str'):
    # "operation": "DescribeReplicationTasks(Filters=[{'Name': 'replication-task-arn','Values': [replication_task_arn]}])",
    logger.info('inside waiter_for_replication_task_status')
    dms = boto3.client("dms", Region_name)
    waiter_name = "ReplicationTaskReadyStopped"
    delay = 5
    max_attempts = 12
    waiter_config = {
        "version": 2,
        "waiters": {
            "ReplicationTaskReadyStopped": {
                "operation": "DescribeReplicationTasks",
                "delay": delay,
                "maxAttempts": max_attempts,
                "acceptors": [
                    {
                        "matcher": "pathAll",
                        "expected": "stopped",
                        "argument": "ReplicationTasks[].Status",
                        "state": "success"
                    }
                ],
            },
        },
    }
    waiter_model = WaiterModel(waiter_config)
    custom_waiter = create_waiter_with_client(waiter_name, waiter_model, dms)
    logger.info("Inside WAITER CLASS DEFINITION")
    try:
        logger.info(replication_task_arn)
        # logger.info(f"custom_waiter.wait(Filters=[{'Name': 'replication-task-arn','Values': [{replication_task_arn}]}])")
        custom_waiter.wait(Filters=[{'Name': 'replication-task-arn','Values': [replication_task_arn]}])
        logger.info("Wait Successful")
    except Exception as e:
        print(e)

def waiter_for_instance_task_status(cluster_id :'str', Region_name: 'str'):
    logger.info('inside waiter_for_replication_task_status')
    dms = boto3.client("rds", Region_name)
    waiter_name = "DBInstanceStatus"
    delay = 2
    max_attempts = 1
    waiter_config = {
        "version": 2,
        "waiters": {
            "DBInstanceStatus": {
                "operation": "DescribeDBInstances",
                "delay": delay,
                "maxAttempts": max_attempts,
                "acceptors": [
                    {
                        "matcher": "pathAll",
                        "expected": "available",
                        "argument": "DBInstances[].DBInstanceStatus",
                        "state": "success"
                    }
                ],
            },
        },
    }
    waiter_model = WaiterModel(waiter_config)
    custom_waiter = create_waiter_with_client(waiter_name, waiter_model, dms)
    logger.info("Inside WAITER CLASS DEFINITION")
    try:
        inst_id="a200333-drcoreservicepg0657-dev-pg-cluster-us-east-1-inst"
        logger.info(inst_id)
        # custom_waiter.wait(DBInstanceIdentifier=inst_id)
        custom_waiter.wait(Filters = [{'Name': 'db-instance-id','Values': [inst_id]}])
        logger.info("Wait Successful")
    except Exception as e:
        print(e)
