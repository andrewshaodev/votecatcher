from enum import Enum
from piccolo.columns import Varchar, Text, ForeignKey
from piccolo.columns.readable import Readable
from piccolo.table import Table
from piccolo.apps.user.tables import BaseUser


# 1. Define your Enum
class APIKeyName(str, Enum):
    MISTRAL_API_KEY = "MISTRAL_API_KEY"
    OPENAI_API_KEY = "OPENAI_API_KEY"
    GEMINI_API_KEY = "GEMINI_API_KEY"


# 2. Define the table
class APIKey(Table):
    # This column is restricted to the enum values
    name = Varchar(choices=APIKeyName)

    # Store the actual key securely
    apikey = Text(secret=True)

    # Who the key belongs to or is associated with
    user = ForeignKey(references=BaseUser)

    # Optional: for display in Piccolo Admin or readable views
    @classmethod
    def get_readable(cls):
        return Readable(template="%s", columns=[cls.name])
