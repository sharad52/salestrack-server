"""
"""
from __future__ import annotations

import fire
from salestrack import console


if __name__ == "__main__":
    fire.Fire(console.CliCommand)

# from fastapi import FastAPI

# app = FastAPI()


# @app.get("/")
# async def root():
#     return {"message": "Hello World"}


# @app.get("/hello/{name}")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}