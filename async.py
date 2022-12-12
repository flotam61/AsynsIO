import datetime
import asyncio
from aiohttp import ClientSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, JSON
from sqlalchemy.ext.declarative import declarative_base
from more_itertools import chunked

db_dsn = 'postgresql+asyncpg://flores:zxczxc@localhost:5432/StarWars'
engine = create_async_engine(db_dsn)
Base = declarative_base()

chunk_cize = 10

async def chunked_async(async_iter, size):
    buffer = []
    while True:
        try:
            item = await async_iter.__anext__()
        except StopAsyncIteration:
            break
        buffer.append(item)
        if len(buffer) == size:
            yield buffer
            buffer = []

class People(Base):

    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    json = Column(JSON)

async def get_person(people_id: int, session: ClientSession):
    async with session.get(f'https://swapi.dev/api/people/{people_id}') as response:
        json_data = await response.json()
        if 'detail' not in json_data:
            films_list = []
            for i in json_data['films']:
                async with session.get(f'{i}') as film_data:
                    y = await film_data.json()
                    films_list.append(y['title'])
            speciec_list = []
            for i in json_data['species']:
                async with session.get(f'{i}') as speciec_data:
                    y = await speciec_data.json()
                    speciec_list.append(y['name'])
            starships_list = []
            for i in json_data['starships']:
                async with session.get(f'{i}') as starships_data:
                    y = await starships_data.json()
                    starships_list.append(y['name'])
            vehicles_list = []
            for i in json_data['vehicles']:
                async with session.get(f'{i}') as vehicles_data:
                    y = await vehicles_data.json()
                    vehicles_list.append(y['name'])

            new_data = {'films': films_list, 'species': speciec_list, 'starships': starships_list, 'vehicles': vehicles_list}
            json_data.update(new_data)

    return json_data

async def get_people():
    async with ClientSession() as session:
        for chunk in chunked(range(1, 84), chunk_cize):
            coroutines = [get_person(people_id=i, session=session) for i in chunk]
            results = await asyncio.gather(*coroutines)
            for item in results:
                yield item
                print(item)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async for chunk in chunked_async(get_people(), chunk_cize):
        async with Session() as session:
            session.add_all([People(json=item) for item in chunk])
            await session.commit()

start = datetime.datetime.now()
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(main())
print(datetime.datetime.now() - start)