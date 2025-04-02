import re
from logging import Filter, LogRecord
from typing import Any


class DataFilterBase(Filter):
    def _check_message_type(self, message: Any) -> str:
        if not isinstance(message, str):
            try:
                message = str(message)
            except Exception:
                message = "Message format not supported"
        return message

    def mask_data(self, message: Any, compile_patterns: str, mask: str) -> str:
        message = self._check_message_type(message)
        if re.search(compile_patterns, message) is not None:
            return mask
        return message


class SensitiveDataFilter(DataFilterBase):
    sensitive_patterns = [
        r"SECRET_KEY",  # Matches 'SECRET_KEY'
        r"FIRST_SUPERUSER",  # Matches 'FIRST_SUPERUSER'
        r"FIRST_SUPERUSER_PASSWORD",  # Matches 'FIRST_SUPERUSER_PASSWORD'
        r"OLTP_DATABASE_URI",  # Matches 'DATABASE_URL'
    ]
    compile_sensitive_patterns = "|".join(sensitive_patterns)

    def filter(self, record: LogRecord) -> bool:
        record.msg = self.mask_sensitive_data(record.msg)
        return True

    def mask_sensitive_data(self, message: Any):
        mask = "Details contains sensitive information."
        return self.mask_data(
            message=message, compile_patterns=self.compile_sensitive_patterns, mask=mask
        )


class UnwantedDataFilter(DataFilterBase):
    unwanted_patterns = [
        r"/api/api_v1/health",
    ]
    compile_unwanted_patterns = "|".join(unwanted_patterns)

    def filter(self, record: LogRecord) -> bool:
        record.msg = self.mask_unwanted_data(record.msg)
        if not record.msg:
            return False
        return True

    def mask_unwanted_data(self, message: Any):
        mask = ""
        message = self._check_message_type(message)
        masked = self.mask_data(
            message=message, compile_patterns=self.compile_unwanted_patterns, mask=mask
        )
        return masked
