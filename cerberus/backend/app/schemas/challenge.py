from pydantic import BaseModel, Field


class ChallengeCreate(BaseModel):
    event_id: int
    title: str = Field(min_length=3, max_length=255)
    category: str
    difficulty: str
    type: str
    hierarchical_rule: dict = Field(default_factory=dict)
    visibility: str = "private"


class ChallengeUpdate(BaseModel):
    title: str | None = None
    category: str | None = None
    difficulty: str | None = None
    visibility: str | None = None


class SubChallengeCreate(BaseModel):
    title: str
    order: int = Field(gt=0)
    flag: str = Field(min_length=1, max_length=256)


class HintCreate(BaseModel):
    content: str
    penalty: int = Field(ge=0, le=1000)
    enabled: bool = False
