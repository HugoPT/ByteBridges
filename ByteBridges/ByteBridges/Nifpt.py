import requests

from .models import CompanyAPI
from django.conf import settings

class NIFApiClient:
    def __init__(self):
        self.api_key = settings.NIF_PT_API_KEY
        self.session_id = ""
        self.base_url = "https://www.nif.pt/"

    def fetch_company_data(self, nif):
        url = f"{self.base_url}?json=1&q={nif}&key={self.api_key}"

        payload = {}
        headers = {}

        response = requests.get(url, headers=headers, data=payload)

        if response.status_code == 200:
            data = response.json()
            records_data = data.get('records', {}).get(str(nif), {})

            # Creating a Company object with the extracted data
            return CompanyAPI(
                result=data.get('result'),
                nif_validation=records_data.get('nif_validation', False),
                is_nif=records_data.get('is_nif', False),
                records_nif=records_data.get('nif'),
                records_seo_url=records_data.get('seo_url'),
                records_title=records_data.get('title'),
                records_address=records_data.get('address'),
                records_pc4=records_data.get('pc4'),
                records_pc3=records_data.get('pc3'),
                records_city=records_data.get('city'),
                records_start_date=records_data.get('start_date'),
                records_activity=records_data.get('activity'),
                records_status=records_data.get('status'),
                records_cae=records_data.get('cae', []),
                records_contacts_email=records_data.get('contacts', {}).get('email'),
                records_contacts_phone=records_data.get('contacts', {}).get('phone'),
                records_contacts_website=records_data.get('contacts', {}).get('website'),
                records_contacts_fax=records_data.get('contacts', {}).get('fax'),
                records_structure_nature=records_data.get('structure', {}).get('nature'),
                records_structure_capital=records_data.get('structure', {}).get('capital'),
                records_structure_capital_currency=records_data.get('structure', {}).get('capital_currency'),
                records_geo_region=records_data.get('geo', {}).get('region'),
                records_geo_county=records_data.get('geo', {}).get('county'),
                records_geo_parish=records_data.get('geo', {}).get('parish'),
                records_place_address=records_data.get('place', {}).get('address'),
                records_place_pc4=records_data.get('place', {}).get('pc4'),
                records_place_pc3=records_data.get('place', {}).get('pc3'),
                records_place_city=records_data.get('place', {}).get('city'),
                records_racius=records_data.get('racius'),
                records_alias=records_data.get('alias'),

            )

        else:
            # Handle error cases here
            print(f"Error fetching data. Status code: {response.status_code}")
            return None
