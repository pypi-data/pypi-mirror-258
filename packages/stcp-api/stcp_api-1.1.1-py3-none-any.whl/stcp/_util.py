def get_internal_line_code(line_code: str):
    """
    Converts the human-readable line code into the internal one (e.g. ZC -> 107)
    :param line_code: the human-readable line code
    :return: the internal line code
    """
    from stcp._primitives import get_lines

    for line in get_lines():
        if line['pubcode'] == line_code:
            return line['code']

    raise Exception('Invalid line code')


def to_time_object(time: str):
    from datetime import datetime, timedelta

    bus = datetime.strptime(time, '%H:%M')
    date_obj = datetime.now().replace(hour=bus.hour, minute=bus.minute, second=0, microsecond=0)

    # if it's more than 10 mins in the past assume it's tomorrow
    if date_obj < datetime.now() - timedelta(minutes=10):
        date_obj += timedelta(days=1)

    return date_obj


def condense_numbers(numbers):
    condensed = []
    i = 0
    while i < len(numbers):
        current_group = [numbers[i]]
        i += 1
        while i < len(numbers) and numbers[i] == current_group[-1] + 1:
            current_group.append(numbers[i])
            i += 1

        condensed.append(current_group)

    return condensed
