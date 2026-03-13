import os

from dotenv import load_dotenv
from fastapi import APIRouter
from pyb1slayer import SLConnection

load_dotenv()


sap_router = APIRouter(prefix="/sap")

@sap_router.get("/")
async def sap_root():
    try:

        sap = SLConnection(
            url= os.getenv("SAP_URL"),
            username= os.getenv("SAP_USER"),
            password=os.getenv("SAP_PASS"),
            company_db= os.getenv("SAP_DB"),
            verify_ssl=False,
        )
        await sap.login()

        info = await (sap.request("Items/$count")
                      .filter("ItemsGroupCode eq 117 and Valid eq 'tYES' and PurchaseItem eq 'tYES' and SalesItem eq 'tYES' and InventoryItem eq 'tYES'")
                      .get())


        return {"Hello": f"World desde sap rputer {str(info)}"}

    except Exception as e:
        return {"Error": f"Ha ocurrido un error aqui {str(e)}"}