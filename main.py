import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Client, Session, Resource, Contract, Invoice, ContactMessage, Coach

app = FastAPI(title="CoachFlow API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"name": "CoachFlow API", "status": "ok"}

# Health and DB test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = getattr(db, 'name', None) or "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# ----- Public: Contact form -----
@app.post("/api/contact")
def submit_contact(message: ContactMessage):
    try:
        doc_id = create_document("contactmessage", message)
        return {"status": "ok", "id": doc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Coaches & Clients -----
@app.post("/api/clients")
def create_client(client: Client):
    try:
        new_id = create_document("client", client)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/clients")
def list_clients(coach_id: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {"coach_id": coach_id} if coach_id else {}
        docs = get_documents("client", filter_dict, limit)
        # Convert ObjectId to string for frontend safety
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Sessions -----
@app.post("/api/sessions")
def create_session(session: Session):
    try:
        new_id = create_document("session", session)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/sessions")
def list_sessions(client_id: Optional[str] = None, coach_id: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {}
        if client_id:
            filter_dict["client_id"] = client_id
        if coach_id:
            filter_dict["coach_id"] = coach_id
        docs = get_documents("session", filter_dict, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Resources -----
@app.post("/api/resources")
def create_resource(resource: Resource):
    try:
        new_id = create_document("resource", resource)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/resources")
def list_resources(coach_id: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {"coach_id": coach_id} if coach_id else {}
        docs = get_documents("resource", filter_dict, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Contracts -----
@app.post("/api/contracts")
def create_contract(contract: Contract):
    try:
        new_id = create_document("contract", contract)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/contracts")
def list_contracts(coach_id: Optional[str] = None, client_id: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {}
        if coach_id:
            filter_dict["coach_id"] = coach_id
        if client_id:
            filter_dict["client_id"] = client_id
        docs = get_documents("contract", filter_dict, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----- Billing (Invoices) -----
@app.post("/api/invoices")
def create_invoice(invoice: Invoice):
    try:
        new_id = create_document("invoice", invoice)
        return {"id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/invoices")
def list_invoices(coach_id: Optional[str] = None, client_id: Optional[str] = None, status: Optional[str] = None, limit: int = 50):
    try:
        filter_dict = {}
        if coach_id:
            filter_dict["coach_id"] = coach_id
        if client_id:
            filter_dict["client_id"] = client_id
        if status:
            filter_dict["status"] = status
        docs = get_documents("invoice", filter_dict, limit)
        for d in docs:
            d["_id"] = str(d.get("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
