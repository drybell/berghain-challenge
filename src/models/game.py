from core.datatypes.sequence  import Sequence

from pydantic import BaseModel, RootModel, UUID4, PrivateAttr
from enum import StrEnum, IntEnum

import pandas as pd

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
    playerId : UUID4
    scenario : GameScenario

class DecideNextParams(BaseModel):
    gameId      : UUID4
    personIndex : int = 0
    accept      : bool | None = None

class BaseGameRequest(BaseModel):
    _route : GameRoute = PrivateAttr()

class NewGameRequest(BaseGameRequest):
    _route   : GameRoute = PrivateAttr(
        default=GameRoute.NEW_GAME
    )
    scenario : GameScenario
    playerId : UUID4

class DecideNextRequest(BaseGameRequest):
    _route      : GameRoute = PrivateAttr(
        default=GameRoute.DECIDE_AND_NEXT
    )
    gameId      : UUID4
    personIndex : int = 0
    accept      : bool | None = None

class GameConstraint(BaseModel):
    attribute : str
    minCount  : int

class UnknownPersonAttributes(RootModel[dict[str, bool]]):
    ...

class PersonAttributes(BaseModel, extra='forbid'):
    ...

class Person(BaseModel):
    personIndex : int
    attributes  : (
        PersonAttributes
        | UnknownPersonAttributes
    )

class UnknownRelativeFrequencies(RootModel[dict[str, float]]):
    ...

class UnknownCorrelations(RootModel[dict[str, dict[str, float]]]):
    ...

class RelativeFrequencies(BaseModel, extra='forbid'):
    """
    Note: This was left intentially blank in the beginning since
    we don't know the attributes beforehand. This model was
    populated once I inspected the response data

    Initially data will come from the Unknown* types above
    """
    well_dressed : float | None = None
    young        : float | None = None

class Correlations(BaseModel, extra='forbid'):
    """
    See RelativeFrequencies docstr
    """
    ...

class GameAttributeStatistics(BaseModel):
    relativeFrequencies : (
        RelativeFrequencies
        | UnknownRelativeFrequencies
    )
    correlations : (
        Correlations
        | UnknownCorrelations
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

class GameData(BaseModel):
    id : UUID4
    constraints  : Sequence[GameConstraint]
    frequencies  : dict
    correlations : dict

    @classmethod
    def from_new_game(cls, game):
        freqs = game.attributeStatistics.relativeFrequencies
        corr  = game.attributeStatistics.correlations

        match freqs:
            case UnknownRelativeFrequencies():
                freqs = freqs.root
            case _:
                freqs = freqs.model_dump()

        match corr:
            case UnknownCorrelations():
                corr = corr.root
            case _:
                corr = corr.model_dump()

        return cls(
            id=game.gameId
            , constraints=game.constraints
            , frequencies=freqs
            , correlations=corr
        )

    def gen_correlation_matrix_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.correlations)

    def gen_requirements_df(self) -> pd.DataFrame:
        return pd.DataFrame(self.constraints.model_dump())
