import inspect
from traceback import format_exc

from fastapi import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.constants import LogMessage



# # # # # # # # Exception Definitions # # # # # # # #

# Any exception should contain an error message that will provide sufficient
# context when troubleshooting.


class InvalidObjectException(Exception):
    def __init__(self, object, validation_detail: str, *args: object) -> None:
        super().__init__(*args)
        self.object = object
        self.validation_detail = validation_detail

    def __str__(self):
        return f"InvalidObhjectException: {self.validation_detail}"


# # # # # # # # Exception Handler Definitions # # # # # # # #


# TODO Handle return verbosity according to the environment
class AppExceptionHandler:
    def __init__(self, app) -> None:
        self.app = app
        self.register_handlers()

    def register_handlers(self):
        app = self.app

        @app.exception_handler(InvalidObjectException)
        async def invalid_object_handler(request: Request, exc: InvalidObjectException):
            error_message = LogMessage.INVALID_OBJECT.format(
                object=type(exc.object).__name__,
            )
            return JSONResponse(
                status_code=422,
                content={
                    "error": error_message,
                    "details": exc.validation_detail,
                    "full_object": f"{exc.object.dict()}",
                    "traceback": format_exc().split("\n"),
                },
            )

        @app.exception_handler(ValidationError)
        # Pydantic is the last line of defense
        # Error of this type ideally should not occur, they should be handled on the code
        # Model defitions must be tight enough to avoid this type of exception
        # The endpoint 'schema' definition should guard before this exception is raised
        async def pydantic_model_validation_error(request: Request, exc: ValidationError):
            if "PydanticObjectId" in str(exc.raw_errors):
                object_id = None
                try:
                    # Since the value is dropped out of the current context
                    # Try to jump back in trace stack to find it
                    # Python 3.11, beanie 1.19.0 @ beanie/odm/documents.py, line 194, code get
                    object_id = inspect.trace()[-3].frame.f_locals.get("document_id")
                except Exception:
                    # If it is exiting from here, functions have changed or could be different case
                    pass

                return JSONResponse(
                    status_code=400,
                    content={
                        "error": f"Invalid object id provided{': ' + object_id if object_id else '' }",
                    },
                )

            return JSONResponse(
                status_code=422,
                content={
                    "error": "Pydantic model validation error",
                    "model": f"{exc.model.__name__}",
                    "traceback": format_exc().split("\n"),
                },
            )
