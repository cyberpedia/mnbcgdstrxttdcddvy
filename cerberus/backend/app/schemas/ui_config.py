from pydantic import BaseModel, HttpUrl


class UIConfigPayload(BaseModel):
    theme: str
    logo_url: HttpUrl
    primary_color: str
    secondary_color: str
    assets: dict[str, str] = {}
