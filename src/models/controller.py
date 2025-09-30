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
from typing import Any

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

    @staticmethod
    def build(
        cls, request=None
    ):
        return cls(
            **BaseControllerRequest._base_params()
            , request=request.model_dump()
        )

    def _build_url(self):
        return str(self.url) + self.request._route.value

    def to_request_payload(self):
        return (
            self._build_url()
            , self.request.model_dump()
        )

class NewGameControllerRequest(BaseControllerRequest):
    request : NewGameRequest

    @classmethod
    def build(cls, **kw):
        return BaseControllerRequest.build(
            cls
            , request=NewGameParams(
                playerId=settings.player.id
                , **kw
            )
        )

class DecideNextControllerRequest(BaseControllerRequest):
    request : DecideNextRequest

    @classmethod
    def build(cls, **kw):
        return BaseControllerRequest.build(
            cls, request=DecideNextParams(**kw)
        )

class BaseGameResponse(BaseModel):
    status : int

class NewGameResponse(BaseGameResponse):
    request  : NewGameControllerRequest
    response : NewGameResponseT

class DecideNextResponse(BaseGameResponse):
    request  : DecideNextControllerRequest
    response : DecideNextResponseT

GameRequestT = (
    DecideNextControllerRequest
    | NewGameControllerRequest
)

class ErrorResponse(BaseGameResponse):
    request  : GameRequestT
    response : Any

GameResponseT = (
    NewGameResponse
    | DecideNextResponse
    | ErrorResponse
)
