import aiosqlite
from config import CACHE_DB

async def init_db():
    async with aiosqlite.connect(CACHE_DB) as db:
        await db.execute(
            '''
            CREATE TABLE IF NOT EXISTS cache (
                topic TEXT PRIMARY KEY,
                content TEXT
            )
            '''
        )
        await db.commit()

async def get_cache(topic):
    async with aiosqlite.connect(CACHE_DB) as db:
        cursor = await db.execute(
            "SELECT content FROM cache WHERE topic=?",
            (topic,)
        )
        row = await cursor.fetchone()

        if row:
            return row[0]

        return None

async def save_cache(topic, content):
    async with aiosqlite.connect(CACHE_DB) as db:
        await db.execute(
            "INSERT OR REPLACE INTO cache VALUES (?, ?)",
            (topic, content)
        )
        await db.commit()