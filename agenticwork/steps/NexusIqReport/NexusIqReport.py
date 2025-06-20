import json
from typing import Any

from patchwork.logger import logger
from patchwork.step import Step
import requests
from base64 import b64encode


class NexusIqReport(Step):
    required_keys = "sbom_vdr_file"
    def __init__(self, inputs: dict):
        super().__init__(inputs)
        self.sbom_vdr_file  = inputs.get("sbom_vdr_file")
        self.iq_server = inputs.get("iq_server")
        self.username = inputs.get("username")
        self.password = inputs.get("password")
        self.app_id = inputs.get("app_id")
        self.report_id = inputs.get("report_id")
        self.cyclo_version = inputs.get("cyclo_version")

    def run(self) -> dict[str, Any] | None:
        """
        Read sbom_vdr_file json file
        """
        auth_token = b64encode(f"{self.username}:{self.password}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_token}",
            "Accept": "application/json"
        }

        url = f"{self.iq_server}/api/v2/cycloneDx/{self.cyclo_version }/{self.app_id}/reports/{self.report_id}"
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return {"sbom_vdr_values": data}
        except json.JSONDecodeError as e:
            logger.debug(e)
            raise ValueError(f"Error reading SBOM VDR file from Depscan")
        except FileNotFoundError as e:
            logger.debug(e)
            raise ValueError(f"SBOM VDR file not found from Depscan")
        except Exception as e:
            logger.debug(e)
            raise ValueError(f"Exception raised {e} " )

