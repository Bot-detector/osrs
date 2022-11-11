from dataclasses import dataclass

from typing import Optional

@dataclass
class userAgent(object):
    discord: str
    email: Optional[str] = ""
    purpose: Optional[str] = ""

    def to_dict(self):
        return {"User-agent": " - ".join([self.purpose, self.discord, self.email])}

