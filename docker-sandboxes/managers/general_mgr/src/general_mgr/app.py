import argparse

from aws_lambda_powertools import Logger

from general_mgr.orchestrator import Orchestrator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog="general-mgr", description="General Sandbox Manager")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging")
    parser.add_argument(
        "--profile",
        action="append",
        required=True,
        help="AWS profile to inject into sandboxes (repeatable)",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    logger = Logger(service="general-mgr", level="DEBUG" if args.verbose else "INFO")
    Orchestrator(profiles=args.profile, logger=logger)
