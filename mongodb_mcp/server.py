from mcp.server.fastmcp import FastMCP
from pymongo import MongoClient


mcp = FastMCP("MongoDB MCP")
client = MongoClient('mongodb://localhost:27017/')
db = client["main-db"]  # Hardcoded database name


@mcp.tool()
def get_collection_names() -> list[str]:
    return db.list_collection_names()


@mcp.tool()
def query_collection(collection_name: str, query: dict = None, limit: int = 10) -> list[dict]:
    """
    Query documents from a MongoDB collection.
    
    Args:
        collection_name: The name of the collection
        query: MongoDB query filter in JSON format (default: empty query that matches all documents)
        limit: Maximum number of documents to return (default: 10)
        
    Returns:
        List of documents matching the query
    """
    if query is None:
        query = {}
        
    try:
        collection = db[collection_name]
        
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
        collection_name: The name of the collection
        document: Document to insert
        
    Returns:
        Result of the insert operation including the inserted ID
    """
    try:
        collection = db[collection_name]
        
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
        collection_name: The name of the collection
        filter_query: Query to select documents to update
        update: Update operations to apply (using MongoDB update operators)
        
    Returns:
        Result of the update operation
    """
    try:
        collection = db[collection_name]
        
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
        collection_name: The name of the collection
        filter_query: Query to select documents to delete
        
    Returns:
        Result of the delete operation
    """
    try:
        collection = db[collection_name]
        
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


@mcp.tool()
def create_collection(collection_name: str) -> dict:
    """
    Create a new collection.
    
    Args:
        collection_name: The name of the collection to create
        
    Returns:
        Result of the create operation
    """
    try:
        db.create_collection(collection_name)
        
        return {
            "success": True,
            "message": f"Collection '{collection_name}' created"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@mcp.tool()
def delete_collection(collection_name: str) -> dict:
    """
    Delete a collection.
    
    Args:
        collection_name: The name of the collection to delete
        
    Returns:
        Result of the delete operation
    """
    try:
        db[collection_name].drop()
        
        return {
            "success": True,
            "message": f"Collection '{collection_name}' deleted"
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