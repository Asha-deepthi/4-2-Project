from nutrition_lookup import get_gi, get_carbs_per_100g

def calculate_glycemic_load(food_name: str, portion_grams: float):
    """
    Calculates Glycemic Load (GL)
    GL = (GI × available carbs) / 100
    """

    gi = get_gi(food_name)
    carbs_per_100g = get_carbs_per_100g(food_name)

    if gi is None or carbs_per_100g is None:
        return None

    total_carbs = (carbs_per_100g * portion_grams) / 100
    gl = (gi * total_carbs) / 100

    return round(gl, 2)
