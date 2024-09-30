event_emojis = {
    "Битва за Даскшир": "⚔️",  # Битва
    "Битва за зачарованные Пруды": "🌊",  # Вода, пруды
    "Логово Дракона": "🐉",  # Дракон
    "Последний день Ирамканда": "⏳",  # Песочные часы (время)
}


def get_event_msg(event_name: str, event_time: str) -> str:
    msg = f"{event_emojis[event_name]} Событие <b>'{event_name}'</b> начнётся через <b>{event_time}!</b>"
    return msg
