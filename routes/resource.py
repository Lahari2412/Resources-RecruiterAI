# from fastapi import APIRouter, HTTPException, status
# from models.resource import Resource
# from config.db import conn
# from schemas.resource import resourceEntity, resourcesEntity

# resource = APIRouter(prefix="/api/v1/resource")

# @resource.get('/')
# async def find_all_resources():
#     resources = list(conn.local.resource.find())
#     return resourcesEntity(resources)


# @resource.post('/')
# async def create_resource(resource: Resource):
#     resource_dict = dict(resource)
#     conn.local.resource.insert_one(resource_dict)
#     return resourceEntity(resource_dict)


# @resource.put('/{id}')
# async def update_resource(id: int, resource: Resource):
#     resource_dict = dict(resource)
#     result = conn.local.resource.update_one(
#         {"id": id},
#         {"$set": resource_dict}
#     )

#     if result.modified_count == 1:
#         return resourceEntity(resource_dict)
#     else:
#         raise HTTPException(status_code=404, detail=f"Resource with id {id} not found")


# @resource.get('/{id}')
# async def get_resource(id: int):
#     resource = conn.local.resource.find_one({"id": id})
#     if resource:
#         return resourceEntity(resource)
#     else:
#         raise HTTPException(status_code=404, detail=f"Resource with id {id} not found")


# @resource.delete('/{id}')
# async def delete_resource(id: int):
#     result = conn.local.resource.delete_one({"id": id})

#     if result.deleted_count == 1:
#         return {"message": f"Resource with id {id} deleted successfully"}
#     else:
#         raise HTTPException(status_code=404, detail=f"Resource with id {id} not found")


from fastapi import APIRouter, HTTPException, status
from models.resource import Resource
from config.db import conn
from schemas.resource import resourceEntity, resourcesEntity
from pymongo.errors import DuplicateKeyError

resource = APIRouter(prefix="/api/v1/resource")

@resource.get('/')
async def find_all_resources():
    resources = list(conn.local.resource.find())
    if resources:
        return resourcesEntity(resources)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No resources found"
        )

@resource.post('/')
async def create_resource(resource: Resource):
    try:
        resource_dict = dict(resource)
        conn.local.resource.insert_one(resource_dict)
        return resourceEntity(resource_dict)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resource with this identifier already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the resource"
        )

@resource.put('/{id}')
async def update_resource(id: int, resource: Resource):
    resource_dict = dict(resource)
    result = conn.local.resource.update_one(
        {"id": id},
        {"$set": resource_dict}
    )

    if result.modified_count == 1:
        return resourceEntity(resource_dict)
    else:
        raise HTTPException(status_code=404, detail=f"Resource with id {id} not found")

@resource.get('/{id}')
async def get_resource(id: int):
    resource = conn.local.resource.find_one({"id": id})
    if resource:
        return resourceEntity(resource)
    else:
        raise HTTPException(status_code=404, detail=f"Resource with id {id} not found")

@resource.delete('/{id}')
async def delete_resource(id: int):
    result = conn.local.resource.delete_one({"id": id})

    if result.deleted_count == 1:
        return {"message": f"Resource with id {id} deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail=f"Resource with id {id} not found")
