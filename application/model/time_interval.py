from typing import List


def prepare_time_to_db(hours: str) -> List[int]:  # "09:00-18:00" -> [540, 1080]
    return convert_time_str_to_int(hours.split("-"))


def convert_time_str_to_int(times: List[str]) -> List[int]:
    start = int(times[0].split(":")[0]) * 60 + int(times[0].split(":")[1])
    end = int(times[1].split(":")[0]) * 60 + int(times[1].split(":")[1])
    return [start, end]


def prepare_time_to_view(hours: List[int]) -> str:  # [540, 1080] -> "09:00-18:00"
    return convert_time_int_to_str(hours)


def convert_time_int_to_str(times: List[int]) -> str:
    return "{:02d}:{:02d}-{:02d}:{:02d}".format(times[0] // 60, times[0] % 60, times[1] // 60, times[1] % 60)
