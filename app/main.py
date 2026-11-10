from datetime import datetime, timezone
from typing import Callable
from uuid import uuid4
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from .types import Call, Clock, IdFactory, Record, Scheduler, Sender, ContractError
from .access_control import AccessControl
from .persistence import Persistence
from . import task_workflow
from .document_validation import DocumentValidation


def create_app(*, store: Persistence | None = None, clock: Clock | None = None, id_factory: IdFactory | None = None, validate_document: Callable[[bytes, str, Record], None] | None = None) -> FastAPI:
    app = FastAPI(title="CarePath - Milan")
    store = store if store is not None else Persistence()
    clock = clock or (lambda: datetime.now(timezone.utc))
    id_factory = id_factory or (lambda kind: str(uuid4()))
    access = AccessControl()
    validate_document = validate_document or DocumentValidation().validate_document

    @app.exception_handler(NotImplementedError)
    async def not_implemented(request: Request, exc: NotImplementedError) -> JSONResponse:
        return JSONResponse(status_code=501,content={"error":"not_implemented","message":"CarePath behavior is not implemented."})

    @app.exception_handler(ContractError)
    async def contract_error(request: Request, exc: ContractError) -> JSONResponse:
        body = {"error":exc.error,"message":exc.message}
        if exc.field is not None:
            body["field"]=exc.field
        return JSONResponse(status_code=exc.status,content=body)

    @app.api_route("/tasks",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_assign_task(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = task_workflow.assign_task(call,access=access, store=store, clock=clock, id_factory=id_factory)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/patients/{patient_id}/tasks",methods=["GET"],responses={501:{"description":"Not implemented"}})
    async def http_list_tasks(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = task_workflow.list_tasks(call,access=access, store=store, clock=clock)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/tasks/{task_id}/documents",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_upload_document(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = task_workflow.upload_document(call,access=access, store=store, clock=clock, id_factory=id_factory, validate_document=validate_document)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/tasks/{task_id}/documents/{document_id}",methods=["GET"],responses={501:{"description":"Not implemented"}})
    async def http_get_document(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = task_workflow.get_document(call,access=access, store=store, clock=clock)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/tasks/{task_id}/complete",methods=["POST"],responses={501:{"description":"Not implemented"}})
    async def http_complete_task(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = task_workflow.complete_task(call,access=access, store=store, clock=clock, id_factory=id_factory)
        return JSONResponse(status_code=result.status,content=result.body)

    @app.api_route("/tasks/{task_id}",methods=["GET"],responses={501:{"description":"Not implemented"}})
    async def http_get_task(request: Request) -> JSONResponse:
        call = Call(request.headers.get("authorization"),dict(request.path_params),dict(request.query_params),await request.body())
        result = task_workflow.get_task(call,access=access, store=store, clock=clock)
        return JSONResponse(status_code=result.status,content=result.body)

    return app

app = create_app()
