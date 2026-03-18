import asyncio
from pathlib import Path

import pandas as pd
from anyio import sleep

from src.models.item_model import UpdateStockLimitByWarehouse
from src.services.sap_service import SapService

MAX_CONCURRENT_REQUESTS = 3
semaphore = asyncio.Semaphore(MAX_CONCURRENT_REQUESTS)

async def patch_item(code, data):
    async with semaphore:
        try:
            sap = await SapService.sap()
            # Usamos el patch directamente.
            # Si tu wrapper sap.request(...).patch() espera 'json' en lugar de 'body', cámbialo.
            await sap.request(f"Items('{code}')").patch(body=data)
            print(f"✅ Item {code} procesado.")
            await asyncio.sleep(0.2)
        except Exception as e:
            if "Expecting value" in str(e):
                print(f"✅ Item {code} actualizado (204 No Content).")
            else:
                print(f"❌ Error en {code}: {e}")

async def update_stock():
    try:

        excel_path = Path("C:/Users/soporte/Downloads/stock_ALM1.xlsx")

        if not excel_path.exists():
            print("El archivo no existe.")
            return

        # Cargamos el Excel. 'Columna1' es el ItemCode.
        df = pd.read_excel(excel_path, dtype={"Columna1": str}).fillna(0)
        batch_size = 50

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i + batch_size]

            tasks = []
            for _, row in df.iterrows():
                code = row["Columna1"]

                # Construcción explícita del modelo
                item_data = UpdateStockLimitByWarehouse(
                    WarehouseCode="ALM1",
                    MinimalStock=float(row["STOCK MINIMO"]),
                    MaximalStock=float(row["STOCK MAXIMO"]),
                    MinimalOrder=float(row["COMPRAS MENSUAL"])
                )

                # Generamos el payload con los nombres que SAP entiende (PascalCase)
                data = {
                    "ItemWarehouseInfoCollection": [
                        item_data.model_dump(by_alias=True)
                    ]
                }

                # Creamos la tarea pero no la esperamos todavía
                tasks.append(patch_item(code, data))

                # Ejecutamos todas las tareas concurrentemente respetando el semáforo
                await asyncio.gather(*tasks)

                # Un pequeño respiro de 2 segundos entre lotes para que el Service Layer respire
                print(f"--- Lote de {i} a {i + batch_size} completado. Esperando 2s... ---")
                await asyncio.sleep(2)


    except Exception as e:
        print(f"Error general: {str(e)}")



if __name__ == "__main__":
    asyncio.run(update_stock())