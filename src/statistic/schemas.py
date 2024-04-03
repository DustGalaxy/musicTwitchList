from typing import List

from pydantic import BaseModel


class StatOrderPopularitySchemas(BaseModel):
    video_id: str
    title: str
    quantity: int


class StatChannelPopularitySchemas(BaseModel):
    channel_name: str
    quantity: int


class StatSendlerPopularitySchemas(BaseModel):
    sendler_name: str
    quantity: int


class StatGlobalSchemas(BaseModel):
    orders_quantity: int
    user_quantity: int

    orders_popularity: List[StatOrderPopularitySchemas]
    channels_popularity: List[StatChannelPopularitySchemas]
    sendler_popularity: List[StatSendlerPopularitySchemas]


class StatUserSchemas(BaseModel):
    total_time: int = 0
    orders_quantity: int = 0

    sendler_popularity: List[StatSendlerPopularitySchemas] = []
    orders_popularity: List[StatOrderPopularitySchemas] = []

