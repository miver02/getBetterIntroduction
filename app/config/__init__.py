from .config import CORS_ADDR, MODEL_API_URL, MODEL_NAME

__all__ = ["CORS_ADDR", "MODEL_API_URL", "MODEL_NAME"]

def get_apirouters_data():
    from .routers import MODELS_ROUTES, USERS_ROUTES, TEST_ROUTES
    return {
        "MODELS_ROUTES": MODELS_ROUTES,
        "USERS_ROUTES": USERS_ROUTES,
        "TEST_ROUTES": TEST_ROUTES,
    }