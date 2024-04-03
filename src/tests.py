import asyncio

from icecream import ic

from src.statistic.utils import order_popylarity


if __name__ == '__main__':
    res = asyncio.run(order_popylarity())
    ic(res)

