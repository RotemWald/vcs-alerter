def update_message_info_list_by_time_interval(msg_info_list, new_msg_info, time_interval):
    new_msg_info_list = []
    for curr_msg_info in msg_info_list:
        if in_time_interval(curr_msg_info.timestamp, new_msg_info.timestamp, time_interval):
            new_msg_info_list.append(curr_msg_info)

    new_msg_info_list.append(new_msg_info)
    return new_msg_info_list


def in_time_interval(old_time, new_time, time_interval):
    return (new_time - old_time).total_seconds() <= time_interval


def out_time_interval(old_time, new_time, time_interval):
    return (new_time - old_time).total_seconds() > time_interval
