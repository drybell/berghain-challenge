from core.datatypes.timestamp import Timestamp
from core.datatypes.sequence  import Sequence

from config import settings

from models.game import (
    NewGameRequest
    , NewGameParams
    , DecideNextRequest
    , DecideNextParams
    , Player
    , NewGameResponse as NewGameResponseT
    , DecideNextResponseT
)

import utils

from pydantic import BaseModel, AnyUrl

class BaseControllerRequest(BaseModel):
    ts      : Timestamp
    url     : AnyUrl
    request : (
        NewGameRequest
        | DecideNextRequest
    )
    player  : Player

    @staticmethod
    def _base_params():
        """
        Possible Extensions
            * allow for players to be set dynamically
        """
        return {
            'ts'       : utils.DT.now()
            , 'url'    : settings.game.url
            , 'player' : settings.player.model_dump()
        }

    @classmethod
    def build(
        cls, request=None
    ):
        return cls(
            **BaseControllerRequest._base_params()
            , request=request
        )

class NewGameControllerRequest(BaseControllerRequest):
    request : NewGameRequest

    @staticmethod
    def build(**kw):
        return BaseControllerRequest.build(
            request=NewGameParams(**kw)
        )

class DecideNextControllerRequest(BaseControllerRequest):
    request : DecideNextRequest

    @staticmethod
    def build(**kw):
        return BaseControllerRequest.build(
            request=DecideNextParams(**kw)
        )

class BaseGameResponse(BaseModel):
    status : int

class NewGameResponse(BaseGameResponse):
    request  : NewGameControllerRequest
    response : NewGameResponseT

class DecideNextResponse(BaseGameResponse):
    request  : DecideNextControllerRequest
    response : DecideNextResponseT
