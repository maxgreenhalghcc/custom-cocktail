from flask import Flask, request, jsonify
import random

app = Flask(__name__)

def oz_to_ml(oz):
    return oz * 29.5735

@app.route('/generate', methods=['POST'])
def generate_bespoke_cocktail():
    user = request.get_json()

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

    flavour_matrix = [
        # SPIRITS
        {'type': 'spirit', 'name': 'vodka', 'seasons': ['spring', 'summer'], 'aromas': ['citrus', 'sweet'], 'profiles': ['clean', 'zesty', 'vibrant']},
        {'type': 'spirit', 'name': 'gin', 'seasons': ['spring'], 'aromas': ['floral', 'citrus'], 'profiles': ['botanical', 'fresh', 'floral']},
        {'type': 'spirit', 'name': 'rum', 'seasons': ['summer', 'autumn'], 'aromas': ['sweet'], 'profiles': ['tropical', 'rich', 'fruity']},
        {'type': 'spirit', 'name': 'bourbon', 'seasons': ['autumn', 'winter'], 'aromas': ['woody', 'sweet'], 'profiles': ['indulgent', 'warm', 'classic']},
        {'type': 'spirit', 'name': 'peach schnapps', 'seasons': ['spring', 'summer'], 'aromas': ['fruity'], 'profiles': ['sweet', 'fresh']},
        {'type': 'spirit', 'name': 'bacardi', 'seasons': ['summer'], 'aromas': ['sweet'], 'profiles': ['tropical', 'light']},
        {'type': 'spirit', 'name': 'dark rum', 'seasons': ['autumn', 'winter'], 'aromas': ['woody'], 'profiles': ['rich', 'indulgent']},
        {'type': 'spirit', 'name': 'spiced rum', 'seasons': ['autumn'], 'aromas': ['woody'], 'profiles': ['spiced', 'warm']},
        {'type': 'spirit', 'name': 'malibu', 'seasons': ['summer'], 'aromas': ['sweet'], 'profiles': ['tropical', 'coconut']},
        {'type': 'spirit', 'name': 'passionfruit vodka', 'seasons': ['summer', 'winter'], 'aromas': ['sweet'], 'profiles': ['tropical', 'exotic']},
        {'type': 'spirit', 'name': 'berry vodka', 'seasons': ['spring', 'winter'], 'aromas': ['sweet'], 'profiles': ['fruity', 'vibrant']},
        {'type': 'spirit', 'name': 'tropical rum', 'seasons': ['summer'], 'aromas': ['sweet'], 'profiles': ['tropical', 'zesty']},
        {'type': 'spirit', 'name': 'rhubarb gin', 'seasons': ['spring'], 'aromas': ['floral'], 'profiles': ['tart', 'fresh']},
        {'type': 'spirit', 'name': 'pink gin', 'seasons': ['spring'], 'aromas': ['floral'], 'profiles': ['fruity', 'romantic']},
        {'type': 'spirit', 'name': 'orange gin', 'seasons': ['summer'], 'aromas': ['citrus'], 'profiles': ['zesty', 'clean']},
        {'type': 'spirit', 'name': 'lemon gin', 'seasons': ['summer'], 'aromas': ['citrus'], 'profiles': ['zesty', 'fresh']},
        {'type': 'spirit', 'name': 'berry bacardi', 'seasons': ['spring', 'summer'], 'aromas': ['sweet'], 'profiles': ['fruity', 'vibrant']},

         # SYRUPS
        {'type': 'syrup', 'name': 'vanilla syrup', 'spirits': ['vodka', 'rum'], 'seasons': ['winter'], 'aromas': ['sweet'], 'profiles': ['rich', 'classic']},
        {'type': 'syrup', 'name': 'maple syrup', 'spirits': ['bourbon', 'rum'], 'seasons': ['autumn'], 'aromas': ['woody'], 'profiles': ['earthy', 'indulgent']},
        {'type': 'syrup', 'name': 'peach syrup', 'spirits': ['vodka', 'gin'], 'seasons': ['summer'], 'aromas': ['floral'], 'profiles': ['fresh', 'fruity']},
        {'type': 'syrup', 'name': 'blue raspberry syrup', 'spirits': ['vodka'], 'seasons': ['spring'], 'aromas': ['sweet'], 'profiles': ['candy', 'vibrant']},

        # MODIFIERS
        {'type': 'modifier', 'name': 'amaretto', 'spirits': ['bourbon'], 'seasons': ['autumn'], 'aromas': ['woody'], 'profiles': ['nutty', 'rich']},
        {'type': 'modifier', 'name': 'grenadine', 'spirits': ['vodka', 'rum'], 'seasons': ['summer', 'spring'], 'aromas': ['sweet'], 'profiles': ['candy', 'classic']},
        {'type': 'modifier', 'name': 'vermouth', 'spirits': ['gin'], 'seasons': ['spring'], 'aromas': ['floral'], 'profiles': ['dry', 'herbal']},
        {'type': 'modifier', 'name': 'citrus vodka / triple sec', 'spirits': ['vodka', 'rum'], 'seasons': ['summer'], 'aromas': ['citrus'], 'profiles': ['zesty', 'vibrant']},

        # JUICES
        {'type': 'juice', 'name': 'orange juice', 'spirits': ['vodka', 'gin', 'tequila'], 'seasons': ['spring'], 'aromas': ['citrus'], 'profiles': ['zesty', 'fresh']},
        {'type': 'juice', 'name': 'pineapple juice', 'spirits': ['rum', 'vodka'], 'seasons': ['summer'], 'aromas': ['sweet'], 'profiles': ['tropical', 'vibrant']},
        {'type': 'juice', 'name': 'cranberry juice', 'spirits': ['vodka', 'rum'], 'seasons': ['autumn'], 'aromas': ['woody'], 'profiles': ['dry', 'subtle']},
        {'type': 'juice', 'name': 'passion fruit juice', 'spirits': ['vodka', 'rum'], 'seasons': ['winter'], 'aromas': ['sweet'], 'profiles': ['exotic', 'indulgent']},

        # GARNISHES
        {'type': 'garnish', 'name': 'lavender sprig', 'seasons': ['spring'], 'aromas': ['floral'], 'profiles': ['fresh', 'romantic']},
        {'type': 'garnish', 'name': 'lemon twist', 'seasons': ['summer'], 'aromas': ['citrus'], 'profiles': ['zesty', 'clean']},
        {'type': 'garnish', 'name': 'rosemary sprig', 'seasons': ['autumn'], 'aromas': ['woody'], 'profiles': ['earthy', 'herbal']},
        {'type': 'garnish', 'name': 'maraschino cherry', 'seasons': ['winter'], 'aromas': ['sweet'], 'profiles': ['indulgent', 'classic']},
    ]


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

    # === LOGIC === #
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

   # modifier = match_flavour('modifier', spirit, user.get('season'), user.get('aroma_preference'), preferred_profiles)
   # sweetener = match_flavour('syrup', spirit, user.get('season'), user.get('aroma_preference'), preferred_profiles)

    
    base_ml = oz_to_ml(strength + balance['modifier'] + balance['sweetener'])
    top_up_needed = max(0, glass['min_ml'] - base_ml)


ingredients = [
        f"{oz_to_ml(strength):.0f}ml {spirit}",
        f"{oz_to_ml(balance['modifier']):.0f}ml {modifier}",
        f"{oz_to_ml(balance['sweetener']):.0f}ml {sweetener}",
        f"{juice} juice",
        f"{juice} juice (Lengthener)",
        f"Garnish: {garnish}"
]

    # If top-up is needed, include that in the ingredients
if top_up_needed > 20:
    ingredients.append(f"Top up with {int(top_up_needed)}ml lemonade or {juice} juice")

    # Now, we don't need to join them into a single string, but keep them as a list of ingredients
recipe = {
    'Glass': glass['type'],
    'Ingredients': ingredients  # Return ingredients as a list (not joined into a string)
}

    # Return the recipe as a JSON response


    
return jsonify(recipe)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
