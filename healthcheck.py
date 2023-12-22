import logging
import sys
import time
from collections import defaultdict
from itertools import count
from urllib.parse import urlparse

import requests
import yaml

INTERVAL_SECONDS = 15
LOG_LEVEL = logging.INFO

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

availability = defaultdict(int)
total_requests = defaultdict(int)


def log_availability():
    for domain, up_requests in availability.items():
        percentage = (up_requests / total_requests[domain]) * 100
        logger.info(f"{domain} has {round(percentage)}% availability percentage")


def is_healthy(endpoint):
    try:
        response = requests.request(
            method=endpoint.get("method", "GET"),
            url=endpoint["url"],
            headers=endpoint.get("headers", {}),
            data=endpoint.get("body", ""),
            timeout=3,
        )

        if (
            response.status_code >= 200
            and response.status_code < 300
            and response.elapsed.total_seconds() < 0.5
        ):
            return True
        else:
            return False
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to send request to {endpoint['url']}: {e}")
        return False


def main():
    if len(sys.argv) != 2:
        logger.error("Usage: python healthcheck.py <config_file_path>")
        sys.exit(1)

    config_file_path = sys.argv[1]

    with open(config_file_path, "r") as file:
        endpoints = yaml.safe_load(file)

    try:
        for i in count(1):
            for endpoint in endpoints:
                domain = urlparse(endpoint["url"]).netloc
                result = is_healthy(endpoint)
                total_requests[domain] += 1
                availability[domain] += result

            logger.debug(f"Cycle: {i}")
            log_availability()
            time.sleep(INTERVAL_SECONDS)

    except KeyboardInterrupt:
        logger.info("Exiting program...")
        sys.exit(0)


if __name__ == "__main__":
    main()
