from core.datatypes.sequence  import Sequence

from pydantic import BaseModel, RootModel, UUID4
from enum import StrEnum

class GameStatus(StrEnum):
    RUNNING   = 'running'
    COMPLETED = 'completed'
    FAILED    = 'failed'

class GameRoute(StrEnum):
    NEW_GAME        = 'new-game'
    DECIDE_AND_NEXT = 'decide-and-next'

class GameScenario(IntEnum):
    EASY   = 1
    MEDIUM = 2
    HARD   = 3

class Player(BaseModel):
    id       : UUID4
    email    : str
    username : str

class NewGameParams(BaseModel):
    scenario : GameScenario

class DecideNextParams(BaseModel):
    gameId      : UUID4
    personIndex : int = 0
    accept      : bool | None = None

class BaseGameRequest(BaseModel):
    route : GameRoute

class NewGameRequest(BaseGameRequest):
    route    : GameRoute = GameRoute.NEW_GAME
    scenario : GameScenario
    playerId : UUID4

class DecideNextRequest(BaseGameRequest):
    route       : GameRoute = GameRoute.DECIDE_AND_NEXT
    gameId      : UUID4
    personIndex : int = 0
    accept      : bool | None = None

class GameConstraint(BaseModel):
    attribute : str
    minCount  : int

class UnknownRelativeFrequencies(RootModel[dict[str, float]]):
    ...

class UnknownCorrelations(RootModel[dict[str, float]]):
    ...

class RelativeFrequencies(BaseModel):
    """
    Note: This was left intentially blank in the beginning since
    we don't know the attributes beforehand. This model was
    populated once I inspected the response data

    Initially data will come from the Unknown* types above
    """
    ...

class Correlations(BaseModel):
    """
    See RelativeFrequencies docstr
    """
    ...

class GameAttributeStatistics(BaseModel):
    relativeFrequencies : (
        UnknownRelativeFrequencies
        | RelativeFrequencies
    )
    correlations : (
        UnknownCorrelations
        | Correlations
    )

class NewGameResponse(BaseModel):
    gameId : UUID4
    constraints : Sequence[GameConstraint]
    attributeStatistics : GameAttributeStatistics

class BaseDecideNextResponse(BaseModel):
    status        : GameStatus
    rejectedCount : int
    nextPerson    : Person | None = None

class RunningDecideNextResponse(BaseDecideNextResponse):
    status        : GameStatus = GameStatus.RUNNING
    admittedCount : int
    nextPerson    : Person

class CompletedDecideNextResponse(BaseDecideNextResponse):
    status : GameStatus = GameStatus.COMPLETED

class FailedDecideNextResponse(BaseDecideNextResponse):
    status : GameStatus = GameStatus.FAILED
    reason : str

DecideNextResponseT = (
    RunningDecideNextResponse
    | CompletedDecideNextResponse
    | FailedDecideNextResponse
)

