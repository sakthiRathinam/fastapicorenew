from fastapi.responses import StreamingResponse
from fastapi import FastAPI
from starlette.responses import JSONResponse
from fastapi import WebSocket, APIRouter, Body, Depends, HTTPException, Request, BackgroundTasks, status, UploadFile, File, Form, Depends, Query
from typing import List
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from src.config.mongo_conf import *
import os
from src.config.mongo_conf import virtual_database, local_database
from src.config.settings import BASE_DIR, STATIC_ROOT, MEDIA_ROOT
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pathlib
import shutil
import uuid
import json
stream_router = APIRouter()
some_file_path = "/app/./src/apps/videostreaming/earth.mp4"
@stream_router.get("/playVideo")
def main():
    def iterfile():
        with open(some_file_path, mode="rb") as file_like:
            yield from file_like
    return StreamingResponse(iterfile(), media_type="video/mp4")
