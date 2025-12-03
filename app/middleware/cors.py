from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://0.0.0.0:5173"],  # 前端地址
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )