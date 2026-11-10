from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .types import Call, Clock, IdFactory, Record, Scheduler, Sender, ContractError
from .access_control import AccessControl
from .persistence import Persistence
from . import patient_views
from . import reminder_delivery

def _unspecified_sender(payload: Record) -> Record:
    raise NotImplementedError


def create_app(*, store: Persistence | None = None, clock: Clock | None = None, id_factory: IdFactory | None = None, send: Sender | None = None) -> FastAPI:
    app = FastAPI(title="CarePath - Sangam")
    store = store if store is not None else Persistence()
    clock = clock or (lambda: datetime.now(timezone.utc))
    id_factory = id_factory or (lambda kind: str(uuid4()))
    access = AccessControl()
    send = send or _unspecified_sender

    @app.exception_handler(NotImplementedError)
    async def not_implemented(request: Request, exc: NotImplementedError) -> JSONResponse:
        return JSONResponse(status_code=501,content={"error":"not_implemented","message":"CarePath behavior is not implemented."})

    @app.exception_handler(ContractError)
    async def contract_error(request: Request, exc: ContractError) -> JSONResponse:
        body = {"error":exc.error,"message":exc.message}
        if exc.field is not None:
            body["field"]=exc.field
        return JSONResponse(status_code=exc.status,content=body)

    @app.api_route("/patients/{patient_id}/care-summary",methods=["GET"],responses={501:{"description":"Not implemented"}})
    async def http_get_care_summary(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = patient_views.get_care_summary(call,access=access, store=store, clock=clock)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/reminders/run",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_run_reminders(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = reminder_delivery.run_reminders(call,access=access, store=store, clock=clock, id_factory=id_factory, send=send)
        return JSONResponse(status_code=result.status,content=result.body)

    return app

app = create_app()
