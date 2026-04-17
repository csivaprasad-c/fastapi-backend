import logging

import logtail

logger = logging.getLogger("fastship")
logger.setLevel(logging.INFO)

logtail_handler = logtail.LogtailHandler(
    source_token="nqbK3no7pnPyCYW6dtFL5UFd",
    host="s2378772.eu-fsn-3.betterstackdata.com",
)

logtail_handler.setFormatter(logging.Formatter("[%(levelname)s]: %(message)s"))

logger.addHandler(logtail_handler)
