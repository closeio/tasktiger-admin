import os

# Redis database number which will be wiped and used for the tests
TEST_DB = int(os.environ.get("REDIS_DB", 1))

# Redis hostname
REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
