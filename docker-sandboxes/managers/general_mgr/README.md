# General Sandbox Manager
Basic sandbox manager. Responsibilities:
* Inject AWS credentials for all sandboxes and keep current.

Periodically:
* Lists sandboxes using `sbx ls --json` and injects AWS creds into each sandbox with
  `sbx exec <sbx_name> bash -c "mkdir -p /home/agent/.aws && echo <creds_str> > /home/agent/.aws/credentials"`
  * Refreshes AWS credentials if <5min from expiry. Stores creds locally.
    * Checks for AWS access with `aws sts get-caller-identity`, exits if no AWS access
    * Uses `aws configure export-credentials --profile <profile>`

CLI options: -v (verbose), --profile (AWS profile, allows repeat)
