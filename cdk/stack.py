from aws_cdk import aws_batch, aws_ec2, aws_ecr_assets, aws_iam, aws_s3, core


class ChaosToolkitBatchExampleStack(core.Stack):
    def __init__(
        self, scope: core.Construct, construct_id: str, identifier: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        journal_bucket = aws_s3.Bucket(
            self,
            id=f"journal-bucket-{identifier}",
            removal_policy=core.RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        vpc = aws_ec2.Vpc(self, id=f"vpc-{identifier}")

        ec2_instance = aws_ec2.Instance(
            self,
            id=f"instance-{identifier}",
            instance_type=aws_ec2.InstanceType("t2.micro"),
            machine_image=aws_ec2.MachineImage.latest_amazon_linux(),
            vpc=vpc,
            allow_all_outbound=False,
            vpc_subnets=aws_ec2.SubnetSelection(subnet_type=aws_ec2.SubnetType.PRIVATE),
        )

        (
            batch_service_role,
            batch_execution_role,
            batch_job_role,
        ) = self.define_service_execution_and_job_roles(identifier)

        journal_bucket.grant_read_write(batch_job_role)

        compute_env = aws_batch.CfnComputeEnvironment(
            self,
            id=f"compute-env-{identifier}",
            type="MANAGED",
            service_role=batch_service_role.role_arn,
            compute_resources=aws_batch.CfnComputeEnvironment.ComputeResourcesProperty(
                type="FARGATE",
                maxv_cpus=1,
                subnets=[subnet.subnet_id for subnet in vpc.private_subnets],
                security_group_ids=[vpc.vpc_default_security_group],
            ),
        )

        _ = aws_batch.CfnJobQueue(
            self,
            id=f"job-queue-{identifier}",
            compute_environment_order=[
                aws_batch.CfnJobQueue.ComputeEnvironmentOrderProperty(
                    compute_environment=compute_env.ref, order=1
                )
            ],
            priority=1,
        )

        experiment_image = aws_ecr_assets.DockerImageAsset(
            self, id=f"container-image-{identifier}", directory="experiment_image"
        )

        _ = aws_batch.CfnJobDefinition(
            self,
            id=f"job-def-{identifier}",
            type="container",
            container_properties=aws_batch.CfnJobDefinition.ContainerPropertiesProperty(
                image=experiment_image.image_uri,
                fargate_platform_configuration=aws_batch.CfnJobDefinition.FargatePlatformConfigurationProperty(  # Noqa
                    platform_version="LATEST"
                ),
                resource_requirements=[
                    aws_batch.CfnJobDefinition.ResourceRequirementProperty(
                        type="MEMORY",
                        value="512",
                    ),
                    aws_batch.CfnJobDefinition.ResourceRequirementProperty(
                        type="VCPU",
                        value="0.25",
                    ),
                ],
                execution_role_arn=batch_execution_role.role_arn,
                job_role_arn=batch_job_role.role_arn,
                environment=[
                    aws_batch.CfnJobDefinition.EnvironmentProperty(
                        name="INSTANCE_ID", value=ec2_instance.instance_id
                    ),
                    aws_batch.CfnJobDefinition.EnvironmentProperty(
                        name="JOURNAL_BUCKET", value=journal_bucket.bucket_name
                    ),
                ],
                command=["experiment-1.json"],
            ),
            platform_capabilities=["FARGATE"],
        )

    def define_service_execution_and_job_roles(self, identifier):
        batch_service_role = aws_iam.Role(
            self,
            id=f"batch-service-role-{identifier}",
            assumed_by=aws_iam.ServicePrincipal("batch.amazonaws.com"),
        )

        batch_service_role.add_managed_policy(
            aws_iam.ManagedPolicy.from_aws_managed_policy_name(
                "service-role/AWSBatchServiceRole"
            )
        )

        batch_execution_role = aws_iam.Role(
            self,
            id=f"batch-execution-role-{identifier}",
            assumed_by=aws_iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        batch_execution_policy = aws_iam.Policy(
            self,
            id=f"batch-execution-policy-{identifier}",
            document=aws_iam.PolicyDocument.from_json(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": [
                                "ecr:GetAuthorizationToken",
                                "ecr:BatchCheckLayerAvailability",
                                "ecr:GetDownloadUrlForLayer",
                                "ecr:BatchGetImage",
                                "logs:CreateLogStream",
                                "logs:PutLogEvents",
                            ],
                            "Resource": "*",
                        }
                    ],
                }
            ),
        )

        batch_execution_policy.attach_to_role(batch_execution_role)

        batch_job_role = aws_iam.Role(
            self,
            id=f"batch-job-role-{identifier}",
            assumed_by=aws_iam.ServicePrincipal("ecs-tasks.amazonaws.com"),
        )

        batch_job_policy = aws_iam.Policy(
            self,
            id=f"batch-job-policy-{identifier}",
            document=aws_iam.PolicyDocument.from_json(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Action": ["ec2:DescribeInstance*"],
                            "Resource": "*",
                        }
                    ],
                }
            ),
        )

        batch_job_policy.attach_to_role(batch_job_role)

        return (batch_service_role, batch_execution_role, batch_job_role)
