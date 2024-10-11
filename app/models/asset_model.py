
from pydantic import BaseModel
class AssetModel(BaseModel):
    id: str
    name: str
    type: str
    url: str
    size: str
    product_id: str
    

    # def __str__(self):
    #     return f"Asset ID: {self.asset_id}, Asset Name: {self.asset_name}, Asset Type: {self.asset_type}, Asset Status: {self.asset_status}, Asset Location: {self.asset_location}"