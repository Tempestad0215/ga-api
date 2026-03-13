import asyncio
from json import JSONDecodeError
from pathlib import Path

import pandas as pd
from pandas import bdate_range
from pyb1slayer import SLRequestError

from src.services.sap_service import SapService


async def update_id_adicional():

    try:
        excel_path = Path("C:/Users/soporte/Downloads/ID ADICIONAL.xlsx")

        sap  = await SapService.sap()

        if excel_path.exists():
            df = pd.read_excel(excel_path, dtype={"CODIGO":str})

            for index, fila in df.iterrows():
                item_code = str(fila["CODIGO"]).strip()
                item_name = str(fila["DESCRIPCION"]).strip()
                item_id = str(fila["ID ADICIONAL"]).strip()

                current_item = await sap.request("Items", item_code).select("SWW").get()
                sap_sww = current_item.get("SWW")
                # Verificar si existe el id
                if sap_sww is not None and str(sap_sww).strip() != "":
                    continue

                #  Para poder obviar los erroes
                try:

                    await sap.request("Items", item_code).patch(
                        body= {
                            "SWW": item_id
                        },
                    )
                except Exception as e:
                    # Si el error es "Expecting value", es que SAP respondió 204 (ÉXITO)
                    if "Expecting value" in str(e):
                        print(f"✅ ID: {item_code} actualizado correctamente (Confirmado 204)")
                    else:
                        # Si es otro error (ej. 400 o 500), sí lo reportamos
                        print(f"❌ Error real en SAP para {item_code}: {e}")
                        continue


            print("Datos actualizado correctamente")

    except JSONDecodeError as e:
        print(f"Ha ocurrido un error en json {e}")

    except Exception as err:
        print(f"Ha ocurrido un error {err}")



if __name__ == "__main__":
    asyncio.run(update_id_adicional())