from db.session import engine
from models import Base


async def create_tables() -> None:
    print('creating tables...')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print('Tables created.')
