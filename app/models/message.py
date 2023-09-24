from pydantic import BaseModel

class Message(BaseModel):
    from_number: str
    to_number: str
    message_body: str
    