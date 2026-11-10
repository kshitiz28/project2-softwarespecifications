from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .types import Call, Clock, IdFactory, Record, Scheduler, Sender, ContractError
from .access_control import AccessControl
from .persistence import Persistence
from . import appointment_workflow
from .scheduling_adapter import SchedulingAdapter


def create_app(*, store: Persistence | None = None, clock: Clock | None = None, id_factory: IdFactory | None = None, schedule: Scheduler | None = None) -> FastAPI:
    app = FastAPI(title="CarePath - Pranjal")
    store = store if store is not None else Persistence()
    clock = clock or (lambda: datetime.now(timezone.utc))
    id_factory = id_factory or (lambda kind: str(uuid4()))
    access = AccessControl()
    schedule = schedule or SchedulingAdapter().request

    @app.exception_handler(NotImplementedError)
    async def not_implemented(request: Request, exc: NotImplementedError) -> JSONResponse:
        return JSONResponse(status_code=501,content={"error":"not_implemented","message":"CarePath behavior is not implemented."})

    @app.exception_handler(ContractError)
    async def contract_error(request: Request, exc: ContractError) -> JSONResponse:
        body = {"error":exc.error,"message":exc.message}
        if exc.field is not None:
            body["field"]=exc.field
        return JSONResponse(status_code=exc.status,content=body)

    @app.api_route("/referrals/{referral_id}/appointment-slots",methods=["GET"],responses={501:{"description":"Not implemented"}})
    async def http_list_slots(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = appointment_workflow.list_slots(call,access=access, store=store, clock=clock, schedule=schedule)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/referrals/{referral_id}/appointments",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_book_appointment(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = appointment_workflow.book_appointment(call,access=access, store=store, clock=clock, id_factory=id_factory, schedule=schedule)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/booking-attempts/{attempt_id}/reconcile",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_reconcile_attempt(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = appointment_workflow.reconcile_attempt(call,access=access, store=store, clock=clock, id_factory=id_factory, schedule=schedule)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/appointments/{appointment_id}",methods=["PATCH"],responses={501:{"description":"Not implemented"}})
    async def http_change_appointment(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = appointment_workflow.change_appointment(call,access=access, store=store, clock=clock, id_factory=id_factory, schedule=schedule)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/appointments/{appointment_id}/history",methods=["GET"],responses={501:{"description":"Not implemented"}})
    async def http_get_appointment_history(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = appointment_workflow.get_appointment_history(call,access=access, store=store, clock=clock)
        return JSONResponse(status_code=result.status,content=result.body)

    return app

app = create_app()
