import ipih
from pih.consts.hosts import Hosts
from pih.collections.service import ServiceDescription

from enum import Enum

NAME: str = "Mail"
SECTION: str = "MailboxInfo"

HOST = Hosts.WS255

#1.24 - Persistance caching for email address deliverability checking status
#1.23 - again call for email deliverability checking status == UNKNOWN
VERSION: str = "1.24"

TIMEOUT: int = 10
TRY_AGAIN_COUNT: int = 5
TRY_AGAIN_SLEEP_TIME: int = 1
PACKAGES: tuple[str, ...] = ("py3-validate-email", "imap_tools")

SD: ServiceDescription = ServiceDescription(
    name=NAME,
    description="Mail service",
    host=HOST.NAME,
    commands=(
        "check_email_accessibility",
        "send_email",
        "get_email_information",
        "check_email_external",
    ),
    standalone_name="mail",
    use_standalone=True,
    version=VERSION,
    packages=PACKAGES,
)

EMAIL_STATUS_FIELD: str = "deliverability"
SECTION: str = "email_" + EMAIL_STATUS_FIELD

class EmailStatuses(Enum):

    UNKNOWN = "UNKNOWN"
    DELIVERABLE = "DELIVERABLE"