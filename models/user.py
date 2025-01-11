from dataclasses import dataclass, asdict
import json

@dataclass
class User:
    id: int
    email: str
    password: str
    first_name: str
    last_name: str
    twitter_handle: str
    is_admin: bool = False

    @property
    def is_authenticated(self):
        return True

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def to_dict(self):
        data = asdict(self)
        # Remove sensitive information
        data.pop('password', None)
        return data

    def __str__(self):
        return json.dumps(self.to_dict()) 