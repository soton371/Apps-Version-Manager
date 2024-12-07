from fastapi.responses import JSONResponse
from fastapi import status
from fastapi.encoders import jsonable_encoder



def ResponseSuccess(status_code: int = status.HTTP_200_OK, data: any = None, message: str = "The request is ok"):
    content = {
        "success": True,
        "message": message,
    }
    if data is not None:
        content["data"] = jsonable_encoder(data)
    return JSONResponse(
        status_code=status_code,
        content=content
    )


def ResponseFailed(status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, message: any = "Something went wrong"):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": str(message)
        }
    )
