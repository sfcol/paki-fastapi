import uvicorn

if __name__ == '__main__':
    uvicorn.run("sfc_backend.asgi:app", reload=True, debug=True)