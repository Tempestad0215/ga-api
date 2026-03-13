import base64
import os
from pathlib import Path
from typing import List

import resend
from dotenv import load_dotenv

load_dotenv()

class SendEmail:
    resend.api_key = os.getenv("RESEND_KEY")

    @staticmethod
    async def send_email(send_to: str | list[str], total_items: int, warehouse: str, excel_path: Path):
        template_id = os.getenv("STOCK_TEMPLATE_ID")
        from_email = os.getenv("EMAIL_FROM") or ""

        recipients:List[str] = []

        if isinstance(send_to, List):
            recipients = send_to
        elif isinstance(send_to, str):
            recipients = [email.strip() for email in send_to.split(",") if email.strip()]
        else:
            return None

        try:
            with open(excel_path, 'rb') as excel_file:
                excel_bytes = excel_file.read()

        #         Codificar el archivo a base 64
                encode_content = base64.b64encode(excel_bytes).decode("utf-8")
        except Exception as e:
            print(f"❌ Ha ocurrido un error {e}")
            return None

        return resend.Emails.send({
            "from" : from_email,
            "to" : recipients,
            "template" : {
                "id": template_id,
                "variables": {
                    "WAREHOUSE": warehouse,
                    "TOTAL_ITEMS": total_items,
                }
            },
            "attachments" : [{
                "filename": "report.xlsx",
                "content": encode_content
            }]
        })