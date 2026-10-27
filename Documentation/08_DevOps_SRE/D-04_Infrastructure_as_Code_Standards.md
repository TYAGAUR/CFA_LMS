# D-04 Infrastructure-as-Code Standards

| Field | Value |
|---|---|
| Document ID | D-04 |
| Version | 0.1 |
| Owner | DevOps lead |
| Last updated | 2026-10-23 |
| Related | A-05, D-01, D-02, S-03 |

## 1. Tooling
- **Terraform** ≥ 1.9 (pinned in `.terraform-version`), with the AWS provider pinned to a minor version.
- **State:** S3 backend in the `shared` account, one bucket per environment state, versioned, encrypted with KMS, using S3-native state locking (`use_lockfile = true`).
- **Linting and policy:** `terraform fmt -check`, `terraform validate`, `tflint` (AWS ruleset), `checkov` (merge blocking on High).
- **Docs:** `terraform-docs` generates a README for each module (checked in CI).

## 2. Repository layout

```
infra/terraform/
  modules/
    network/        VPC, subnets, NAT, endpoints, flow logs
    edge/           CloudFront, WAF, ACM, Route53 records
    ecs-service/    generic Fargate service (task def, service, autoscaling, alarms)
    ecs-cluster/
    rds-postgres/   RDS, parameter group, PITR, snapshots copy, alarms
    redis/
    s3-bucket/      secure defaults (BPA, TLS-only, KMS, lifecycle, optional object lock)
    kms/
    secrets/
    observability/  log groups, dashboards, SNS topics, synthetics canaries
    iam-oidc-github/
    budgets/
  envs/
    shared/         org-level: state buckets, ECR, GitHub OIDC, Identity Center assignments
    staging/        main.tf, variables.tf, staging.tfvars, backend.tf
    production/
```

**Rules:**
- Environments call modules. No raw resources in `envs/*` except glue (outputs, data sources).
- Modules have typed variables with `validation` blocks and descriptions, and outputs for everything others need.
- One state per environment. No cross-environment references, except through outputs read with `terraform_remote_state` from `shared`.

## 3. Naming and tagging
- **Name pattern:** `{project}-{env}-{component}[-{suffix}]`, e.g. `cfalms-prod-api`, `cfalms-staging-media`.
- **Mandatory tags** (provider `default_tags`): `project=cfalms`, `env`, `service`, `owner`, `data_class` (for storage: C1–C4), `managed_by=terraform`.
- CI fails if a resource that supports tags lacks the mandatory tags (checkov custom policy).

## 4. Secure defaults baked into modules
- S3: Block Public Access, `aws:SecureTransport` deny, SSE-KMS required, versioning on, access logging to the logs bucket.
- RDS: `storage_encrypted`, not publicly accessible, deletion protection in production, IAM authentication, `rds.force_ssl=1`, Performance Insights (KMS), backups 14 days.
- Security groups: no `0.0.0.0/0` ingress except the edge module; egress restricted where practical.
- ECS: read-only root filesystem where possible; no privileged containers; secrets from Secrets Manager only.
- CloudFront: TLS 1.2_2021 minimum, HSTS response headers policy, origin access control for S3.
- KMS: key rotation on; key policies scoped to roles.

## 5. Workflow
1. Change in a branch → PR → CI runs fmt, validate, tflint, checkov and `terraform plan` for staging and production (read-only role). The plan summary is posted to the PR.
2. Review: the DevOps lead plus one other engineer. Production-affecting changes are flagged in the PR title with `[prod-infra]`.
3. Merge → staging apply automatically from the saved plan.
4. Production apply runs from `terraform-apply.yml` with manual dispatch and environment approval, using the plan generated for the merged commit.
5. **No console changes.** An emergency console change must be back-ported to Terraform within 24 hours and logged as an incident action.

## 6. Drift detection
A nightly `terraform plan -detailed-exitcode` runs against staging and production. Drift opens an issue and notifies the DevOps channel. AWS Config rules give a second signal.

## 7. Secrets in IaC
Terraform creates **secret containers** (Secrets Manager entries) without values. Values are set by a rotation Lambda or by an operator through the CLI with MFA. Secret values never appear in tfvars, state outputs or plans. Use `sensitive = true` and avoid `aws_secretsmanager_secret_version` with literal values.

## 8. Cost controls
- `budgets` module: monthly budget per environment, with alerts at 80% and 100% to the PM and DevOps.
- Staging scheduled scale-down: ECS desired count 0 from 23:00 to 08:00 IST on weekdays and all weekend, unless UAT is running (flag variable). RDS staging stops on weekends.

## 9. Module versioning
Modules are internal and referenced by relative path in the monorepo. Breaking module changes are applied to staging first in the same PR, then to production in a follow-up PR after verification.
