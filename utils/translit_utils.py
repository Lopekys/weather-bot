from transliterate import translit

def transliterate_city(city: str) -> str:
    try:
        return translit(city, 'ru', reversed=True)
    except Exception as e:
        raise ValueError(f"Ошибка при транслитерации города: {e}")
