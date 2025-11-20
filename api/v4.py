import operator
from datetime import datetime
from typing import List, Optional

import orjson
import pytz
from hishel.httpx import SyncCacheClient

from .models import Launch, Launchpad, Rocket

BASE_URL = "https://api.spacexdata.com/v4"


def __utc_to_local_time(date_utc: str):
    time_format = "%Y-%m-%dT%H:%M:%S.%f"
    naive_utc_dt = datetime.strptime(date_utc.replace("Z", ""), time_format)
    utc_aware_dt = pytz.utc.localize(naive_utc_dt)
    local_time_dt = utc_aware_dt.astimezone()
    return local_time_dt


def get_launchpad(id: str) -> Optional[Launchpad]:
    with SyncCacheClient(timeout=10.0, base_url=BASE_URL) as client:
        response = client.get(f"/launchpads/{id}")
        response.raise_for_status()
        launchpad = orjson.loads(response.text)
        return Launchpad(
            id=launchpad["id"],
            name=launchpad["name"],
            region=launchpad["region"],
            timezone=launchpad["timezone"],
            longitude=launchpad["longitude"],
            latitude=launchpad["latitude"],
            status=launchpad["status"],
        )


def get_all_launchpads() -> List[Launchpad]:
    with SyncCacheClient(timeout=10.0, base_url=BASE_URL) as client:
        response = client.get("/launchpads")
        response.raise_for_status()
        launchpads = []
        for launchpad in orjson.loads(response.text):
            launchpads.append(
                Launchpad(
                    id=launchpad["id"],
                    name=launchpad["name"],
                    region=launchpad["region"],
                    timezone=launchpad["timezone"],
                    longitude=launchpad["longitude"],
                    latitude=launchpad["latitude"],
                    status=launchpad["status"],
                )
            )
        return launchpads
    return []


def get_rocket(id: str) -> Optional[Rocket]:
    with SyncCacheClient(timeout=10.0, base_url=BASE_URL) as client:
        response = client.get(f"/rockets/{id}")
        response.raise_for_status()
        rocket = orjson.loads(response.text)
        return Rocket(
            id=rocket["id"],
            name=rocket["name"],
            active=rocket["active"],
            type=rocket["type"],
            description=rocket["description"],
        )


def get_all_rockets() -> List[Rocket]:
    with SyncCacheClient(timeout=10.0, base_url=BASE_URL) as client:
        response = client.get("/rockets")
        response.raise_for_status()
        values = []
        for rocket in orjson.loads(response.text):
            values.append(
                Rocket(
                    id=rocket["id"],
                    name=rocket["name"],
                    active=rocket["active"],
                    type=rocket["type"],
                    description=rocket["description"],
                )
            )
        return sorted(values, key=operator.attrgetter("name"))
    return []


def get_launch(id: str) -> Optional[Launch]:
    with SyncCacheClient(timeout=10.0, base_url=BASE_URL) as client:
        response = client.get(f"/launches/{id}")
        response.raise_for_status()

        launch = orjson.loads(response.text)
        rocket = get_rocket(launch["rocket"])
        launchpad = get_launchpad(launch["launchpad"])
        if not rocket or not launchpad:
            raise Exception("Unable to find required information")
        return Launch(
            id=launch["id"],
            rocket=rocket,
            launchpad=launchpad,
            success=launch["success"],
            date=__utc_to_local_time(launch["date_utc"]),
            details=launch["details"],
        )


def filter_launches(
    start: Optional[str],
    end: Optional[str],
    rocket: Optional[str],
    success: Optional[bool],
    failed: Optional[bool],
    site: Optional[str],
) -> List[Launch]:
    query: dict = {}
    
    date_query = {}
    if start:
        date_query["$gte"] = f"{start}T00:00:00.000Z"
    if end:
        date_query["$lte"] = f"{end}T23:59:59.999Z"
    if not date_query:
        date_query = None
    if date_query:
        query["date_utc"] = date_query
    
    if rocket:
        query["rocket"] = rocket
    if site:
        query["launchpad"] = site
    
    with SyncCacheClient(timeout=10.0, base_url=BASE_URL) as client:
        payload = {"query": query, "options": {}}

        response = client.post(f"/launches/query", json=payload)
        response.raise_for_status()

        launches = []
        data = orjson.loads(response.text)
        for launch in data["docs"]:
            _rocket = get_rocket(launch["rocket"])
            launchpad = get_launchpad(launch["launchpad"])
            if not _rocket or not launchpad:
                raise Exception("Unable to find required information")
            launches.append(
                Launch(
                    id=launch["id"],
                    rocket=_rocket,
                    launchpad=launchpad,
                    success=launch["success"],
                    date=__utc_to_local_time(launch["date_utc"]),
                    details=launch["details"],
                )
            )
        return launches
    return []
