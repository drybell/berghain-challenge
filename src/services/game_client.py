from models.controller import (
    NewGameControllerRequest
    , NewGameResponse
    , DecideNextControllerRequest
    , DecideNextResponse
    , ErrorResponse
    , GameRequestT
    , GameResponseT
)

import requests

class GameClient:

    @staticmethod
    def _request(request : GameRequestT) -> GameResponseT:
        reqkw = {
            'request': request
            , 'status': 999
        }

        try:
            response = requests.get(
                *request.to_request_payload()
            )

            reqkw['status'] = response.status_code

            match request:
                case DecideNextControllerRequest():
                    cls = DecideNextResponse
                case NewGameControllerRequest():
                    cls = NewGameResponse

            return cls(
                response=response.json()
                , **reqkw
            )
        except Exception as e:
            return ErrorResponse(
                response=e
                , **reqkw
            )

    @staticmethod
    def new_game(**kw) -> GameResponseT:
        """
        kw should satisfy models.game.NewGameParams
        """
        return GameClient._request(
            NewGameControllerRequest.build(
                **kw
            )
        )

    @staticmethod
    def decide_and_next(**kw) -> GameResponseT:
        """
        kw should satisfy models.game.DecideNextParams
        """
        return GameClient._request(
            DecideNextControllerRequest.build(
                **kw
            )
        )
