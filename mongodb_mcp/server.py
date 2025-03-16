from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient
import json
from bson import ObjectId

mcp = FastMCP("MongoDB MCP")
client = MongoClient('mongodb://localhost:27017/')


@mcp.tool()
def get_collection_names() -> list[str]:
    db_names = client.list_database_names()
    collections = []
    
    for db_name in db_names:
        if db_name not in ['admin', 'local', 'config']:  # Skip system databases
            db = client[db_name]
            for collection in db.list_collection_names():
                collections.append(f"{db_name}.{collection}")
    
    return collections


@mcp.tool()
def query_collection(collection_name: str, query: dict = None, limit: int = 10) -> list[dict]:
    """
    Query documents from a MongoDB collection.
    
    Args:
        collection_name: The name of the collection in format 'database.collection'
        query: MongoDB query filter in JSON format (default: empty query that matches all documents)
        limit: Maximum number of documents to return (default: 10)
        
    Returns:
        List of documents matching the query
    """
    if query is None:
        query = {}
        
    try:
        db_name, coll_name = collection_name.split('.')
        db = client[db_name]
        collection = db[coll_name]
        
        # Execute the query and convert results to list of dicts
        cursor = collection.find(query).limit(limit)
        results = list(cursor)
        
        # Convert ObjectId to string for JSON serialization
        for doc in results:
            if '_id' in doc:
                doc['_id'] = str(doc['_id'])
                
        return results
    except Exception as e:
        return [{"error": str(e)}]


@mcp.tool()
def insert_document(collection_name: str, document: dict) -> dict:
    """
    Insert a document into a MongoDB collection.
    
    Args:
        collection_name: The name of the collection in format 'database.collection'
        document: Document to insert
        
    Returns:
        Result of the insert operation including the inserted ID
    """
    try:
        db_name, coll_name = collection_name.split('.')
        db = client[db_name]
        collection = db[coll_name]
        
        result = collection.insert_one(document)
        
        return {
            "success": True,
            "inserted_id": str(result.inserted_id)
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def update_documents(collection_name: str, filter_query: dict, update: dict) -> dict:
    """
    Update documents in a MongoDB collection.
    
    Args:
        collection_name: The name of the collection in format 'database.collection'
        filter_query: Query to select documents to update
        update: Update operations to apply (using MongoDB update operators)
        
    Returns:
        Result of the update operation
    """
    try:
        db_name, coll_name = collection_name.split('.')
        db = client[db_name]
        collection = db[coll_name]
        
        result = collection.update_many(filter_query, update)
        
        return {
            "success": True,
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def delete_documents(collection_name: str, filter_query: dict) -> dict:
    """
    Delete documents from a MongoDB collection.
    
    Args:
        collection_name: The name of the collection in format 'database.collection'
        filter_query: Query to select documents to delete
        
    Returns:
        Result of the delete operation
    """
    try:
        db_name, coll_name = collection_name.split('.')
        db = client[db_name]
        collection = db[coll_name]
        
        result = collection.delete_many(filter_query)
        
        return {
            "success": True,
            "deleted_count": result.deleted_count
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


def main():
    mcp.run()

if __name__ == "__main__":
    main()