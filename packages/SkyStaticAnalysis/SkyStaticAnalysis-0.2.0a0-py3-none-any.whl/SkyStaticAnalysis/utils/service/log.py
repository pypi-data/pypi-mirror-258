import logging
import sys

logger = logging.getLogger("SkyStaticAnalysis")

# logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.DEBUG)
stdoutHandler = logging.StreamHandler(stream=sys.stderr)
stdoutHandler.setLevel(logging.DEBUG)

fmt = logging.Formatter(
    "%(levelname)s [%(asctime)s %(filename)s:%(lineno)s | %(process)d]: %(message)s"
)

# Set the log format on each handler
stdoutHandler.setFormatter(fmt)

logger.addHandler(stdoutHandler)
