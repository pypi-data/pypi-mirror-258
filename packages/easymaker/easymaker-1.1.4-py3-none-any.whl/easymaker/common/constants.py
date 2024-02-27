DEFAULT_REGION = 'kr1'
SUPPORTED_REGIONS = {
    'kr1',
    'kr3'
    # 'kr2',
    # 'us',
    # 'jp',
}

EASYMAKER_API_WAIT_INTERVAL_SECONDS = 10

# EasyMaker API URL
EASYMAKER_API_URL = 'https://{}-easymaker.api.nhncloudservice.com'
EASYMAKER_DEV_API_URL = 'https://{}-easymaker-{}.api.nhncloudservice.com'

# Object Storage URL
OBJECT_STORAGE_TOKEN_URL = 'https://api-identity-infrastructure.nhncloudservice.com/v2.0/tokens'

# Log & Crash URL
LOGNCRASH_URL = 'https://api-logncrash.nhncloudservice.com/v2/log'
LOGNCRASH_MAX_MESSAGE_SIZE = 8000000  # Log&Crash limit body size(= 8388608)
LOGNCRASH_MAX_BUFFER_SIZE = 40000000  # Log&Crash HTTP 요청 하나의 최대 크기 52MB

class HYPERPARAMETER_TYPE_CODE():
    INT = 'int'
    DOUBLE = 'double'
    DISCRETE = 'discrete'
    CATEGORICAL = 'categorical'

class OBJECTIVE_TYPE_CODE():
    MINIMIZE = 'MINIMIZE'
    MAXIMIZE = 'MAXIMIZE'

class TUNING_STRATEGY():
    GRID = 'GRID'
    RANDOM = 'RANDOM'
    BAYESIAN_OPTIMIZATION = 'BAYESIAN_OPTIMIZATION'

class EARLY_STOPPING_ALGORITHM():
    MEDIAN = 'MEDIAN'
