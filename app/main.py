from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .types import Call, Clock, IdFactory, Record, Scheduler, Sender, ContractError
from .access_control import AccessControl
from .persistence import Persistence
from . import referral_workflow
from . import external_updates


def create_app(*, store: Persistence | None = None, clock: Clock | None = None, id_factory: IdFactory | None = None) -> FastAPI:
    app = FastAPI(title="CarePath - Kshitiz")
    store = store if store is not None else Persistence()
    clock = clock or (lambda: datetime.now(timezone.utc))
    id_factory = id_factory or (lambda kind: str(uuid4()))
    access = AccessControl()

    @app.exception_handler(NotImplementedError)
    async def not_implemented(request: Request, exc: NotImplementedError) -> JSONResponse:
        return JSONResponse(status_code=501,content={"error":"not_implemented","message":"CarePath behavior is not implemented."})

    @app.exception_handler(ContractError)
    async def contract_error(request: Request, exc: ContractError) -> JSONResponse:
        body = {"error":exc.error,"message":exc.message}
        if exc.field is not None:
            body["field"]=exc.field
        return JSONResponse(status_code=exc.status,content=body)

    @app.api_route("/referrals",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_submit_referral(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = referral_workflow.submit_referral(call,access=access, store=store, clock=clock, id_factory=id_factory)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/referrals/{referral_id}/reviews",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_review_referral(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = referral_workflow.review_referral(call,access=access, store=store, clock=clock, id_factory=id_factory)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/referrals/{referral_id}/findings",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_share_findings(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = referral_workflow.share_findings(call,access=access, store=store, clock=clock, id_factory=id_factory)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/referrals",methods=["GET"],responses={501:{"description":"Not implemented"}})
    async def http_list_referrals(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = referral_workflow.list_referrals(call,access=access, store=store, clock=clock)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/referrals/{referral_id}/information-requests",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_request_information(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = referral_workflow.request_information(call,access=access, store=store, clock=clock, id_factory=id_factory)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/referrals/{referral_id}/information-requests/{request_id}/response",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_respond_to_information_request(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = referral_workflow.respond_to_information_request(call,access=access, store=store, clock=clock, id_factory=id_factory)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/referral-events",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_apply_external_event(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = external_updates.apply_external_event(call,access=access, store=store, clock=clock, id_factory=id_factory)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/referrals/{referral_id}",methods=["GET"],responses={501:{"description":"Not implemented"}})
    async def http_get_referral(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = referral_workflow.get_referral(call,access=access, store=store, clock=clock)
        return JSONResponse(status_code=result.status,content=result.body)

    return app

app = create_app()
