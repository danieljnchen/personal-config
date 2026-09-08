from dataclasses import dataclass
from datetime import datetime, timedelta

REFRESH_BUFFER = timedelta(minutes=5)


@dataclass(kw_only=True)
class AwsCreds:
    aws_profile: str
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str
    expiration: str

    def expires_at(self) -> datetime:
        return datetime.fromisoformat(self.expiration)

    def refresh_at(self) -> datetime:
        return self.expires_at() - REFRESH_BUFFER

    def credentials_file_block(self, profile_name: str) -> str:
        return (
            f"[{profile_name}]\n"
            f"aws_access_key_id = {self.aws_access_key_id}\n"
            f"aws_secret_access_key = {self.aws_secret_access_key}\n"
            f"aws_session_token = {self.aws_session_token}\n"
        )
