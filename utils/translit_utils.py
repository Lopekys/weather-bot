from transliterate import translit

def transliterate_city(city: str) -> str:
    try:
        return translit(city, 'ru', reversed=True)
    except Exception as e:
        raise ValueError(f"Error during city transliteration: {e}")
