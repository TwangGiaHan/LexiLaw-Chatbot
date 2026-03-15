# app/core/neo4j.py
import os
from neo4j import AsyncGraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")
NEO4J_DATABASE = os.getenv("NEO4J_DATABASE")

_driver = None

def get_driver():
    global _driver
    if _driver is None:
        _driver = AsyncGraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    return _driver

async def close_driver():
    global _driver
    if _driver:
        await _driver.close()
        _driver = None

def get_db():
    # helper for session kwargs
    return {"database": NEO4J_DATABASE} if NEO4J_DATABASE else {}