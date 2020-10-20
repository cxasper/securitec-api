def format_mintute_seconds(time):
    split_timedelta = str(time).split(':')
    total_minutes = int(split_timedelta[1]) + (int(split_timedelta[0])*60)
    return '%s:%s' %(total_minutes, split_timedelta[2])
