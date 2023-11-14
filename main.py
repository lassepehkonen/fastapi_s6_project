import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

import tokens.token
from controllers import auth_controller, user_controllers

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def check_csrf(request: Request, call_next):
    if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
        if str(request.url).find('login') == -1 and str(request.url).find('register') == -1:

            try:

                _token = tokens.token.init_token()
                csrf = _token.validate(request.cookies.get('csrf_token_cookie'))
                access = _token.validate(request.cookies.get('access_token_cookie'))
                if csrf is None or access is None:
                    return JSONResponse(content={'err': 'forbidden'}, status_code=403)
                if csrf['sub'] != access['csrf']:
                    return JSONResponse(content={'err': 'forbidden'}, status_code=403)

            except Exception as e:
                return JSONResponse(content={'err': 'forbidden'}, status_code=403)

    response = await call_next(request)
    return response

SSL = True

app.include_router(auth_controller.router)
app.include_router(user_controllers.router)


if __name__ == '__main__':
    if SSL:
        uvicorn.run("main:app", host='localhost', port=8001, reload=False,
                    ssl_keyfile="./cert/CA/localhost/localhost.decrypted.key",
                    ssl_certfile="./cert/CA/localhost/localhost.crt")
    else:
        uvicorn.run("main:app", host='localhost', port=8001, reload=False)


