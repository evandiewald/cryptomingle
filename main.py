import transactions
from database import *
import config
from pinata import *

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi import Depends, FastAPI, HTTPException, Form, File, UploadFile
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from starlette.responses import RedirectResponse, Response, JSONResponse, HTMLResponse
from starlette.requests import Request


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Postgres
db = create_engine(config.DB_STRING)
conn = db.connect()
session = Session(db)
table = users_table(db)


@app.route("/", methods=["GET", "POST"])
async def homepage(request: Request):
    users_list = list_users(table)
    return templates.TemplateResponse("index.html", {"request": request, "users_list": users_list})


@app.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/newuser")
async def new_user(name: str = Form(...), email: str = Form(...), address: str = Form(...), age: str = Form(...),
                   height: str = Form(...), bio: str = Form(...), files: UploadFile = File(...)):
    r = pin_to_pinata(files.file, files.filename)
    user_id = get_next_id(session, table)
    txn = transactions.add_user(int(user_id), int(height), address)
    transaction_url = 'https://ropsten.etherscan.io/tx/' + txn['transactionHash']
    ipfs_url = 'https://gateway.pinata.cloud/ipfs/' + r['IpfsHash']
    add_user(session, table, int(height), address, name, email, int(age), bio, ipfs_url, transaction_url)
    return RedirectResponse("/")
