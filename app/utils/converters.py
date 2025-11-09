from datetime import datetime


def hPa_to_mmHg(hPa: int) -> int:
    """Конвертирует гектопаскали в миллиметры ртутного столба"""
    return round(hPa * 0.750062)


def convert_datetime(dt: int) -> list[str]:
    """Конвертирует timestamp в datetime и возвращает кортеж с датой и временем"""
    dt_date_time = datetime.fromtimestamp(dt).strftime("%d-%m-%Y %H:%M")

    return dt_date_time.split()


def degrees_to_direction(degrees: int) -> str:
    """
    Преобразует градусы в текстовое направление ветра
    """
    directions = [
        "северный", "северо-восточный", "восточный", "юго-восточный",
        "южный", "юго-западный", "западный", "северо-западный"
    ]

    index = round(degrees / 45) % 8

    return directions[index]
