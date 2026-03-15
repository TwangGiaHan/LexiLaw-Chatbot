import neo4j
from neo4j import AsyncGraphDatabase
from app.core.config import settings

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        uri = settings.NEO4J_URI
        auth = (settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)
        
        if "+s" in uri or "+ssc" in uri:
            _driver = AsyncGraphDatabase.driver(uri, auth=auth)
        else:
            _driver = AsyncGraphDatabase.driver(
                uri, 
                auth=auth,
                trusted_certificates=neo4j.TrustSystemCAs()
            )
    return _driver

async def close_driver():
    global _driver
    if _driver:
        await _driver.close()
        _driver = None

def get_db():
    return {"database": settings.NEO4J_DATABASE} if settings.NEO4J_DATABASE else {}