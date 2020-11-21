# Start Server

```
 uvicorn sfc_backend.asgi:app --debug
```


The Django App can be found under `/django/`, especially admin can be found under `/django/admin``

The OpenAPI API can be found under `/api` and the docs under `/api/docs`.

## How to generate openapi clients (e.g. angular)

### Install openapi-generator

```
npm install @openapitools/openapi-generator-cli -g
```

(See https://openapi-generator.tech/docs/installation/)

### Generate!

```
npx @openapitools/openapi-generator-cli generate -i http://localhost:8000/openapi.json  -o src/app/backend -g typescript-angular
```
(if the server is running).
