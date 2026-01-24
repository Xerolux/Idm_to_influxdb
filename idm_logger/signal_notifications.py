# SPDX-License-Identifier: MIT
import logging
import re
import subprocess
from typing import Iterable, List

from .config import config

logger = logging.getLogger(__name__)

# Valid phone number pattern (international format: +country code + number)
_PHONE_PATTERN = re.compile(r"^\+[1-9]\d{6,14}$")


def _validate_phone_number(number: str) -> bool:
    """Validate that a string looks like a valid international phone number."""
    return bool(_PHONE_PATTERN.match(number))


def _normalize_recipients(value) -> List[str]:
    if not value:
        return []
    if isinstance(value, str):
        entries = [entry.strip() for entry in value.split(",") if entry.strip()]
    elif isinstance(value, Iterable):
        entries = [str(entry).strip() for entry in value if str(entry).strip()]
    else:
        return []

    # Validate and filter recipients
    valid_recipients = []
    for entry in entries:
        if _validate_phone_number(entry):
            valid_recipients.append(entry)
        else:
            logger.warning(
                f"Invalid Signal recipient format (skipped): {entry[:20]}..."
            )

    return valid_recipients


def send_signal_message(message: str) -> None:
    if not config.get("signal.enabled", False):
        raise RuntimeError("Signal-Benachrichtigungen sind deaktiviert.")

    cli_path = config.get("signal.cli_path", "signal-cli")
    sender = config.get("signal.sender", "")

    # Validate sender
    if not sender:
        raise RuntimeError("Signal-Sender ist nicht konfiguriert.")
    if not _validate_phone_number(sender):
        raise RuntimeError("Signal-Sender hat ungültiges Format (erwartet: +49...).")

    recipients = _normalize_recipients(config.get("signal.recipients", []))
    if not recipients:
        raise RuntimeError("Keine gültigen Signal-Empfänger konfiguriert.")

    # Validate cli_path doesn't contain shell metacharacters
    if not re.match(r"^[a-zA-Z0-9_\-/\.]+$", cli_path):
        raise RuntimeError("Signal CLI Pfad enthält ungültige Zeichen.")

    command = [cli_path, "-u", sender, "send", "-m", message] + recipients
    logger.info(f"Sending Signal message to {len(recipients)} recipient(s)")
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Signal CLI Fehler")
