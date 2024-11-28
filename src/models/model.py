from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class JobParams(BaseModel):
    endpoint_1: str = f"https://api.fda.gov/drug/label.json?api_key={os.getenv('FDA_API_KEY')}&search=effective_time:[20110601+TO+20231231]&limit=100"
    endpoint_2: str = f"https://api.fda.gov/drug/ndc.json?api_key={os.getenv('FDA_API_KEY')}&search=finished:true&limit=300"
    file_name_1: str = 'drug_effective_time_20241127103914.csv'
    file_name_2: str = 'drug_ndc_20241127103914.csv'
    raw_dir: str = "/Users/leonardomuntaner/Documents/GitHub/Medical-Data-Connections/DDF/data/raw"
    staging_table_1: str = 'public.drug_effective_time'
    staging_table_2: str = 'public.drug_ndc'