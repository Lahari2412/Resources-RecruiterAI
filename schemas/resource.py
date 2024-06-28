import pymongo


def resourceEntity(item) -> dict:
    return {
        "id": (item["id"]),  # Convert ObjectId to string for JSON serialization
        "job_id": item["job_id"],
        "job_description": item["job_description"],
        "skills": item["skills"],
        "qualification": item["qualification"],
        "experience": item["experience"],
        "resources": item["resources"]
    }

def resourcesEntity(entity):
    if isinstance(entity, pymongo.collection.Collection):
        entity = list(entity.find())  # Convert Collection to list of documents
    return [resourceEntity(item) for item in entity]
