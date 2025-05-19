from flask import Flask, request, jsonify
import random
import json
import os

app = Flask(__name__)

# === Load inventory.json flavour matrices === #
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
json_path = os.path.join(BASE_DIR, 'inventory.json')

with open(json_path, 'r') as f:
    full_inventory = json.load(f)


def oz_to_ml(oz):
    return oz * 29.5735

@app.route('/generate', methods=['POST'])
def generate_bespoke_cocktail():
    user = request.get_json()
    bar_id = user.get('bar_id', 'cross axes').lower()

    flavour_matrix = full_inventory.get(bar_id, {}).get("flavour_matrix", [])

    # Base configuration
    music_strength = {
        'jazz/blues': 1.5,
        'rap': 1.75,
        'pop': 2.0,
        'rock': 2.25
    }

    dining_balances = {
        'a balanced blend of flavours': {'modifier': 0.75, 'sweetener': 0.5},
        'subtle tastes which advertise freshness': {'modifier': 0.5, 'sweetener': 0.25},
        'refreshing and vibrant flavours which awaken my senses': {'modifier': 0.75, 'sweetener': 0.25},
        'a sweet tooth indulging in rich flavours': {'modifier': 1.0, 'sweetener': 0.75},
    }

    color_modifiers = {
        'emerald': ['mint leaves in the glass'],
        'amber': ['maple syrup'],
        'pale pink': ['grenadine'],
        'citrus yellow': ['citrus flavoured liqueur']
    }

    sweetener_styles = {
        'classic': ['simple syrup'],
        'rich': ['maple syrup'],
        'floral': ['elderflower syrup'],
        'zesty': ['lime cordial']
    }

    seasonal_accents = {
        'spring': ['elderflower'],
        'summer': ['fresh mint', 'citrus zest'],
        'autumn': ['maple syrup', 'amaretto'],
        'winter': ['cranberry', "vanilla syrup"]
    }

    aroma_garnish = {
        'floral': 'mint sprig',
        'citrus': 'lemon twist',
        'woody': 'rosemary sprig',
        'sweet': 'fruit on the side of the glass'
    }

    dessert_twists = {
        'vanilla': ['vanilla', 'rich', 'sweet'],
        'tangfastics': ['zesty', 'vibrant', 'sour'],
        'fresh fruit': ['fresh', 'subtle', 'natural']
    }

    glassware = {
        'modern house': {'type': 'short glass', 'min_ml': 150},
        'tree house': {'type': 'gin glass', 'min_ml': 250},
        'beach house': {'type': 'long glass', 'min_ml': 300},
        'haunted house': {'type': 'skull glass', 'min_ml': 100}
    }

    juice_preferences = {
        'spring': 'orange',
        'summer': 'pineapple',
        'autumn': 'cranberry',
        'winter': 'passion fruit'
    }

    dining_juice_map = {
        'a balanced blend of flavours': 'orange',
        'subtle tastes which advertise freshness': 'cranberry',
        'refreshing and vibrant flavours which awaken my senses': 'pineapple',
        'a sweet tooth indulging in rich flavours': 'passion fruit'
    }

    flavour_profile_map = {
        'orange': ['balanced', 'classic', 'zesty'],
        'pineapple': ['vibrant', 'tropical', 'zesty'],
        'cranberry': ['fresh', 'subtle', 'dry'],
        'passion fruit': ['sweet', 'indulgent', 'exotic']
    }

    def match_flavour(item_type, spirit, season, aroma, profile_tags):
        compatible = []
        for item in flavour_matrix:
            if item['type'] != item_type:
                continue
            if spirit and spirit not in item.get('spirits', []):
                continue
            if season and season not in item.get('seasons', []):
                continue
            if aroma and aroma not in item.get('aromas', []):
                continue
            if profile_tags and not any(tag in item.get('profiles', []) for tag in profile_tags):
                continue
            compatible.append(item['name'])
        return random.choice(compatible) if compatible else None

    # === User Input Based Logic === #
    spirit = user.get('base_spirit')
    strength = music_strength.get(user.get('music_preference', '').lower(), 2.0)
    balance = dining_balances.get(user.get('dining_style', '').lower(), {'modifier': 0.75, 'sweetener': 0.5})
    modifier_choices = color_modifiers.get(user.get('modifier_question', '').lower(), [''])
    sweetener_choices = sweetener_styles.get(user.get('sweetener_question', '').lower(), ['simple syrup'])
    seasonal_note = random.choice(seasonal_accents.get(user.get('season', 'spring'), []))
    garnish = aroma_garnish.get(user.get('aroma_preference', '').lower(), 'lemon twist')
    glass = glassware.get(user.get('house_type', 'modern house'), {'type': 'short glass', 'min_ml': 150})

    juice_season = juice_preferences.get(user.get('season', 'spring'), 'orange')
    juice_dining = dining_juice_map.get(user.get('dining_style', '').lower(), 'orange')
    juice = random.choice([juice_season, juice_dining])

    preferred_profiles = set(flavour_profile_map.get(juice, []))
    preferred_profiles.update(dessert_twists.get(user.get('favourite_dessert', '').lower(), []))
    preferred_profiles.add(user.get('aroma_preference', '').lower())
    preferred_profiles.update(user.get('dining_style', '').lower().split())

    modifier = next((m for m in modifier_choices if any(p in m.lower() for p in preferred_profiles)), random.choice(modifier_choices))
    sweetener = next((s for s in sweetener_choices if any(p in s.lower() for p in preferred_profiles)), random.choice(sweetener_choices))

    base_ml = oz_to_ml(strength + balance['modifier'] + balance['sweetener'])
    top_up_needed = max(0, glass['min_ml'] - base_ml)




    
@app.route('/generate-recipe', methods=['POST'])
def generate_recipe():

     ingredients = [
        f"{oz_to_ml(strength):.0f}ml {spirit}",
        f"{oz_to_ml(balance['modifier']):.0f}ml {modifier}",
        f"{oz_to_ml(balance['sweetener']):.0f}ml {sweetener}",
        f"{juice} juice",
        f"{juice} juice (Lengthener)",
        f"Garnish: {garnish}"
    ]
    

    if top_up_needed > 20:
        ingredients.append(f"Top up with {int(top_up_needed)}ml lemonade or {juice} juice")

    # Format as HTML
    ingredients_html = "".join(f"<li>{item}</li>" for item in ingredients)
    recipe_html = f"""
    <h2>Glass: {glass['type']}</h2>
    <h3>Ingredients:</h3>
    <ul>{ingredients_html}</ul>
    """

    recipe = {
        "glass": glass['type'],
        "ingredients_list": ingredients,
        "recipe_html": recipe_html
    }

    return jsonify(recipe)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
