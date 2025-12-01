
def get_apirouters_data():
    from .routers import MODELS_ROUTES, USERS_ROUTES, TEST_ROUTES
    return {
        "MODELS_ROUTES": MODELS_ROUTES,
        "USERS_ROUTES": USERS_ROUTES,
        "TEST_ROUTES": TEST_ROUTES,
    }