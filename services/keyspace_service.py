from astrapy import DataAPIClient
from config.settings import ASTRA_DEVOPS_API_TOKEN, DATABASE_ID

# Initialize Astra API client
client = DataAPIClient(ASTRA_DEVOPS_API_TOKEN)
db_admin = client.get_admin().get_database_admin(DATABASE_ID)

# Predefined collections to be created under each keyspace
COLLECTIONS = ["domains", "subdomains", "port", "security"]

def get_keyspaces():
    try:
        return db_admin.list_keyspaces()
    except Exception as e:
        print(f"Error fetching org: {e}")
        return None

def check_and_create_collections(org: str):
    """Checks and creates missing collections in the specified keyspace."""
    try:
        # Get the database instance for the specified keyspace
        database = client.get_database(DATABASE_ID, keyspace=org)
        
        existing_collections = [col['name'] for col in database.list_collections()]
        
        # Create any missing collections
        collections_created = []
        for collection in COLLECTIONS:
            if collection not in existing_collections:
                database.create_collection(collection, dimension=768, metric="cosine")
                collections_created.append(collection)
        
        if collections_created:
            return {"message": f"Created missing collections: {collections_created} in keyspace '{org}'."}
        else:
            return {"message": f"All collections are already present in keyspace '{org}'."}
        
    except Exception as e:
        print(f"Error checking/creating collections in '{org}': {e}")
        return {"message": f"Error checking/creating collections in keyspace '{org}'."}

def create_keyspace_if_not_exists(org: str):
    keyspaces = get_keyspaces()
    if keyspaces is None:
        return None

    if org in keyspaces:
        collection_result = check_and_create_collections(org)  # Check and create missing collections
        return {"message": f"Keyspace '{org}' already exists.", "collections": collection_result}

    try:
        # Create the new keyspace
        db_admin.create_keyspace(org)
        collection_result = check_and_create_collections(org)
        return {"message": f"Keyspace '{org}' created successfully.", "collections": collection_result}
    except Exception as e:
        print(f"Error creating keyspace: {e}")
        return {"message": f"Error creating keyspace '{org}'."}
