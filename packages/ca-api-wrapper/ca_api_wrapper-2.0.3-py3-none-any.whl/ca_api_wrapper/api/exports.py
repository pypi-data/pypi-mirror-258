from typing import Optional, Tuple, Union
import time
import urllib
import zipfile
from io import BytesIO
import pandas as pd


class ProductExportClient:
    def __init__(self, client):
        self.client = client
        self.profile_id = client.default_profile_id
        self.data_frame = pd.DataFrame()

    def get_products(self, filter, attributes) -> Union[pd.DataFrame, None]:

        token = self._generate_export_token(filter, attributes)

        if token is not None:
            df = self._get_products_export_data(token)
            df.replace("", None, inplace=True)
            if df["ID"] is not None:
                df['ID'] = df['ID'].astype(int)

            return df
        else:
            raise Exception("Failed to generate export token.")

    def get_export_by_token(self, file_token: str) -> Union[Tuple[dict, pd.DataFrame], None]:
        return self._get_products_export_data(file_token)

    def _generate_export_token(self, filter, attributes) -> Optional[str]:

        headers = {"Content-Type": "application/json"}
        params = {
            "access_token": self.client.access_token,
            "profileid": self.profile_id,
            "$filter": filter,
        }
        response = self.client.make_request(
            endpoint="V1/ProductExport", headers=headers, method="POST", data=attributes, params=params)

        if response.status_code != 200:
            raise Exception(
                f"Error generating export token: {response.status_code}")

        return response.json()["Token"]

    def _get_products_export_data(self, file_token: str) -> Union[pd.DataFrame, None]:
        max_retries = 20

        for i in range(max_retries):
            data = self._get_product_export(file_token)
            if data["status"] == "Successful":
                # <-- Check if data_frame is not None
                if data.get("data_frame") is not None:
                    if not data.get("data_frame").empty and data.get('data_frame') is not None:
                        df = self._assign_column_name_to_column_value(
                            data["data_frame"])
                        df.replace("", None, inplace=True)
                        return df
                    else:
                        return None
                else:
                    return None
            time.sleep(4)
        raise Exception("Failed to get product export data.")

    def _get_product_export(self, file_token: str) -> dict:
        headers = {"Accept": "*/*"}
        params = {
            "access_token": self.client.access_token,
            "token": file_token,
        }
        response = self.client.make_request(
            endpoint="V1/ProductExport", headers=headers, method="GET", params=params)
        result = {"response": response.text, "status": "Failed",
                  "download_url": "NOT_AVAILABLE", "attempt": None}
        if response.status_code == 200:
            response_json = response.json()
            if "ResponseFileUrl" in response_json and response_json["ResponseFileUrl"] is not None:
                download_url = response_json["ResponseFileUrl"]
                result.update({
                    "status": "Successful",
                    "download_url": download_url,
                    "data_frame": self._download_export_convert_to_df(download_url)
                })
        return result

    def _download_export_convert_to_df(self, download_url: str) -> pd.DataFrame:

        with urllib.request.urlopen(download_url) as response:
            file = response.read()

        with zipfile.ZipFile(BytesIO(file)) as zipper:
            with zipper.open(zipper.namelist()[0], "r") as csv_file:
                df = pd.read_csv(csv_file, sep="\t",
                                 keep_default_na=False, dtype='string')

        df.replace('', None, inplace=True)

        return df

    @staticmethod
    def _assign_column_name_to_column_value(df: pd.DataFrame) -> pd.DataFrame:
        columns = df.columns.values.tolist()
        drop_columns_list = []
        columns_dictionary = {}

        for element in range(len(columns)):
            if "Attribute" in columns[element] and "Name" in columns[element]:
                column_name = df[columns[element]].values.tolist()[0]
                columns_dictionary[columns[element + 1]] = column_name
                drop_columns_list.append(columns[element])

            elif "Unnamed" in columns[element]:
                drop_columns_list.append(columns[element])

        df.drop(drop_columns_list, axis=1, inplace=True)
        df.rename(columns=columns_dictionary, inplace=True)
        return df
