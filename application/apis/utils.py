
def get_min_avg_time(assign_complete_times: dict) -> int:
    all_mins = list()
    for key, value in assign_complete_times.items():
        min_for_region = 0
        count = 0
        for i, (assign, complete) in enumerate(value):
            if i == 0:
                min_for_region += complete - assign
                count += 1
            else:
                min_for_region += complete - value[i - 1][1]
                count += 1
        all_mins.append(min_for_region // count)

    return min(all_mins)
