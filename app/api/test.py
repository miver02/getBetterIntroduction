from fastapi import APIRouter
from . import get_apirouters_data, logger, get_server_data, res



TEST_ROUTES = get_apirouters_data().get("TEST_ROUTES")

test_router = APIRouter(
    prefix=TEST_ROUTES["prefix"],
    tags=TEST_ROUTES["tags"],
)

test_conn_model_data = TEST_ROUTES["endpoints"].get("test_conn_model")

@test_router.post(test_conn_model_data["path"], summary=test_conn_model_data["summary"], description=test_conn_model_data["description"])
async def test_conn_model():
    """
    测试模型连接
    """
    logger.info("测试模型连接")
    cm = get_server_data().get("cm")
    response, err = await cm.test_conn()

    if err is not None:
        return res.ErrorResponse(code=500, message=str(err))
    return res.SuccessResponse(data=response)