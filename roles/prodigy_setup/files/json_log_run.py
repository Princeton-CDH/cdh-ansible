"""
Run a Python module with every log record formatted as one line of JSON,
for the otel collector.

Prodigy and uvicorn configure their own logging handlers and formatters,
so instead of replacing that configuration this replaces the base
``logging.Formatter.format`` before the module runs. Formatters that only
customize ``formatMessage`` (as uvicorn's do) are covered too.

Usage: python json_log_run.py MODULE [ARGS...]
  e.g. python json_log_run.py prodigy concept-eval dataset data.jsonl
"""

import json
import logging
import runpy
import sys
from datetime import datetime, timezone


def json_format(self, record):
    entry = {
        "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
        "level": record.levelname,
        "logger": record.name,
        "message": record.getMessage(),
        "module": record.module,
        "lineno": record.lineno,
        "process": record.process,
    }
    if record.exc_info:
        entry["exc_info"] = self.formatException(record.exc_info)
    if record.stack_info:
        entry["stack_info"] = self.formatStack(record.stack_info)
    return json.dumps(entry, default=str)


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    logging.Formatter.format = json_format
    module = sys.argv[1]
    # the module sees the same argv it would get from `python -m MODULE ...`
    sys.argv = [sys.argv[0]] + sys.argv[2:]
    runpy.run_module(module, run_name="__main__", alter_sys=True)


if __name__ == "__main__":
    main()
