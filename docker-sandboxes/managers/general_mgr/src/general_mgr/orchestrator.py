import base64
import json
import subprocess
import sys
import time
from datetime import datetime, timezone

from general_mgr.model_types import AwsCreds


class Orchestrator:
    def __init__(self, *, profiles: list[str], logger):
        self.profiles = list(dict.fromkeys(profiles))
        self.logger = logger
        self._creds: dict[str, AwsCreds] = {}
        self._run()

    def _run(self):
        try:
            while True:
                self._refresh_all_creds()
                self.inject_all()
                sleep_for = self._seconds_until_next_refresh()
                self.logger.info(f"Sleeping {sleep_for:.0f}s until next credential refresh")
                time.sleep(sleep_for)
        except KeyboardInterrupt:
            self.logger.info("Shutting down")

    def _refresh_all_creds(self):
        now = datetime.now(timezone.utc)
        for profile in self.profiles:
            creds = self._creds.get(profile)
            if creds is None or now >= creds.refresh_at():
                self._creds[profile] = self._fetch_creds(profile)

    def _fetch_creds(self, profile: str) -> AwsCreds:
        identity = subprocess.run(
            ["aws", "sts", "get-caller-identity", "--profile", profile],
            capture_output=True,
            text=True,
        )
        if identity.returncode != 0:
            self.logger.error(f"No AWS access for profile '{profile}': {identity.stderr.strip()}")
            sys.exit(1)

        export = subprocess.run(
            ["aws", "configure", "export-credentials", "--profile", profile, "--format", "process"],
            capture_output=True,
            text=True,
        )
        if export.returncode != 0:
            self.logger.error(f"Failed to export credentials for profile '{profile}': {export.stderr.strip()}")
            sys.exit(1)

        data = json.loads(export.stdout)
        self.logger.info(f"Refreshed credentials for profile '{profile}', expiring {data['Expiration']}")
        return AwsCreds(
            aws_profile=profile,
            aws_access_key_id=data["AccessKeyId"],
            aws_secret_access_key=data["SecretAccessKey"],
            aws_session_token=data["SessionToken"],
            expiration=data["Expiration"],
        )

    def _seconds_until_next_refresh(self) -> float:
        next_refresh = min(creds.refresh_at() for creds in self._creds.values())
        seconds = (next_refresh - datetime.now(timezone.utc)).total_seconds()
        return max(seconds, 0.0)

    def list_sandboxes(self) -> list[str]:
        result = subprocess.run(["sbx", "ls", "--json"], capture_output=True, text=True)
        if result.returncode != 0:
            self.logger.error(f"Failed to list sandboxes: {result.stderr.strip()}")
            return []
        data = json.loads(result.stdout)
        return [sandbox["name"] for sandbox in data.get("sandboxes", [])]

    def inject_all(self):
        for sbx_name in self.list_sandboxes():
            self.inject_aws_creds(sbx_name=sbx_name)

    def inject_aws_creds(self, *, sbx_name: str):
        contents = "".join(
            creds.credentials_file_block(profile) for profile, creds in self._creds.items()
        )
        encoded = base64.b64encode(contents.encode()).decode()
        command = (
            "mkdir -p /home/agent/.aws && "
            f"echo {encoded} | base64 -d > /home/agent/.aws/credentials"
        )
        result = subprocess.run(
            ["sbx", "exec", sbx_name, "bash", "-c", command],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            self.logger.error(f"Failed to inject AWS creds into sandbox '{sbx_name}': {result.stderr.strip()}")
        else:
            self.logger.info(f"Injected AWS creds into sandbox '{sbx_name}'")
