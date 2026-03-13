import os

from dotenv import load_dotenv
from pyb1slayer import SLConnection


load_dotenv()

class SapService:

    # Para Crear el object de sap
    @staticmethod
    async def sap()->SLConnection:
        verify = os.getenv("VERIFY_SSL", "False").lower() == "true"

        client = SLConnection(
            url=os.getenv("SAP_URL"),
            password=os.getenv("SAP_PASS"),
            username=os.getenv("SAP_USER"),
            company_db=os.getenv("SAP_DB"),
            verify_ssl=verify,
        )
        # Devolver el login
        await client.login()

        # Devolver los datos para continuar
        return client