import json
from datetime import datetime, timedelta
from typing import List, Optional
import urllib3

http = urllib3.PoolManager()


API_URL = "https://api.thegraph.com/subgraphs/name/ensdomains/ens"


def by_name(domain_name: str) -> Optional[dict]:
    """
    Fetches ENS domain information by name.
    
    :param domain_name: ENS domain name to fetch.
    :return: Dictionary with domain information or None if not found.
    """
    query = {
        'query': f"""{{ 
            domains(where: {{name: "{domain_name}"}}) {{ 
                id
                name
                expiryDate
                owner {{
                    id
                }}
            }}
        }}"""
    }
    response = http.request('POST', API_URL, body=json.dumps(query), headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    domains = data.get('data', {}).get('domains', [])
    return domains[0] if domains else None


def by_owner(owner_address: str) -> List[dict]:

    owner_address_lower = owner_address.lower()
    query = {
        'query': f"""{{ 
            domains(where: {{owner: "{owner_address_lower}"}}) {{ 
                id
                name
                expiryDate
                owner {{
                    id
                }}
            }}
        }}"""
    }
    response = http.request('POST', API_URL, body=json.dumps(query), headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    return data.get('data', {}).get('domains', [])

def by_expiry_date(start_date: datetime, end_date: datetime) -> List[dict]:

    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())

    query = {
        'query': f"""{{ 
            domains(where: {{expiryDate_gte: "{start_timestamp}", expiryDate_lte: "{end_timestamp}"}}) {{ 
                id
                name
                expiryDate
                owner {{
                    id
                }}
            }}
        }}"""
    }
    response = http.request('POST', API_URL, body=json.dumps(query), headers={'Content-Type': 'application/json'})
    data = json.loads(response.data.decode('utf-8'))
    return data.get('data', {}).get('domains', [])

print(by_name("happin.eth"))
print(by_owner("0xcf4F0b41Ec79a1FCbc83599B60C031465732c5Ba"))
print(by_expiry_date(datetime.now(), datetime.now() + timedelta(days=1)))