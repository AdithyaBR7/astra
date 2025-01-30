from astrapy import DataAPIClient
from config.settings import ASTRA_DEVOPS_API_TOKEN, DATABASE_ID

# Initialize Astra API client
client = DataAPIClient(ASTRA_DEVOPS_API_TOKEN)
db_admin = client.get_admin().get_database_admin(DATABASE_ID)

def get_keyspaces():
    try:
        return db_admin.list_keyspaces()
    except Exception as e:
        print(f"Error fetching org: {e}")
        return None

def create_keyspace_if_not_exists(org: str):
    keyspaces = get_keyspaces()
    if keyspaces is None:
        return None

    if org in keyspaces:
        return {"message": f"org '{org}' already exists."}

    try:
        db_admin.create_keyspace(org)
        return {"message": f"org '{org}' created successfully."}
    except Exception as e:
        print(f"Error creating org: {e}")
        return {"message": f"Error creating org '{org}'."}
