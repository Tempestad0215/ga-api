import asyncio
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

from src.models.item_model import ItemStockLow
from src.responses.odata_response import ODataResponse
from src.services.email_stock_service import SendEmail
from src.services.sap_service import SapService

load_dotenv()


async def check_stok_warehouse(warehouse: str):
    try:
        client = await SapService.sap()
        data_excel: list[ItemStockLow] = []
        skip = 0
        top = 300

        while True:
            # 1. Una sola petición que se repite con el skip actualizado
            response = await (client.request("view.svc/B1_AlertStockLowB1SLQuery")
                            .filter(f"Almacen eq '{warehouse}'")
                            .with_page_size(top)
                            .skip(skip)
                            .get(ODataResponse[ItemStockLow]))


            # 2. Agregamos los items obtenidos
            if response.value:

                data_excel.extend(response.value)

            print(f"Esta es la sigueinte url {response.odata_next_link}")
            # 3. CONDICIÓN DE SALIDA: Si no hay más páginas, rompemos el bucle
            if not response.odata_next_link:
                break

            # 4. Preparamos el siguiente salto
            skip += top

        data_frame = pd.DataFrame([r.model_dump() for r in data_excel])

        excel_path = Path(__file__).resolve().parent.parent.joinpath("static","excel")

        # Creamos el nombre con la ruta
        file_path = excel_path / f"reporte_stock_{warehouse}.xlsx"
        data_frame.to_excel(file_path, index=False, engine="openpyxl")

        if warehouse == "ALM1":
            send_to = ["tecnologia@depositoferretero.com","aduran@depositoferretero.com", "inventariopp@depositoferretero.com","compras@depositoferretero.com"]
        else:
            send_to = ["tecnologia@depositoferretero.com","aduran@depositoferretero.com", "inventariopp@depositoferretero.com","comprasbavaro@depositoferretero.com"]

        await SendEmail.send_email(
            send_to,
            len(data_excel),
            warehouse,
            file_path,
        )

        print("✅ Se ha Generado el Excel")
    except Exception as e:
        print(f"❌ Error durante la extracción: {e}")






if __name__ == "__main__":
    asyncio.run(check_stok_warehouse("ALM1"))