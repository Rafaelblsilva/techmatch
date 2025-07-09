from enum import Enum
DEFAULT_SYSTEM_UUID = "daa3d03f-75bc-4f7d-bb16-58154f300662"

class LogMessage:
    INVALID_OBJECT = "Invalid {object} Object"

class API_TAGS(Enum):
    RESUMES = 'Resumes'
    LOGS = 'Logs'
    USERS = 'Users'