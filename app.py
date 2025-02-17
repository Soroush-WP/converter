from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    data = request.get_json()
    value = data['value']
    unit_from = data['unitFrom']
    unit_to = data['unitTo']
    
    conversions = {
        'length': {
            'meters': {'meters': 1, 'kilometers': 0.001, 'centimeters': 100, 'millimeters': 1000},
            'kilometers': {'meters': 1000, 'kilometers': 1, 'centimeters': 100000, 'millimeters': 1000000},
            'centimeters': {'meters': 0.01, 'kilometers': 0.00001, 'centimeters': 1, 'millimeters': 10},
            'millimeters': {'meters': 0.001, 'kilometers': 0.000001, 'centimeters': 0.1, 'millimeters': 1}
        },
        'weight': {
            'grams': {'grams': 1, 'kilograms': 0.001, 'milligrams': 1000, 'pounds': 0.00220462},
            'kilograms': {'grams': 1000, 'kilograms': 1, 'milligrams': 1000000, 'pounds': 2.20462},
            'milligrams': {'grams': 0.001, 'kilograms': 0.000001, 'milligrams': 1, 'pounds': 0.00000220462},
            'pounds': {'grams': 453.592, 'kilograms': 0.453592, 'milligrams': 453592, 'pounds': 1}
        },
        'temperature': {
            'celsius': {'celsius': 1, 'fahrenheit': lambda c: (c * 9/5) + 32, 'kelvin': lambda c: c + 273.15},
            'fahrenheit': {'celsius': lambda f: (f - 32) * 5/9, 'fahrenheit': 1, 'kelvin': lambda f: ((f - 32) * 5/9) + 273.15},
            'kelvin': {'celsius': lambda k: k - 273.15, 'fahrenheit': lambda k: ((k - 273.15) * 9/5) + 32, 'kelvin': 1}
        }
    }
    
    if unit_from in conversions[data['category']] and unit_to in conversions[data['category']][unit_from]:
        conversion = conversions[data['category']][unit_from][unit_to]
        if callable(conversion):
            result = conversion(value)
        else:
            result = value * conversion
        return jsonify({'result': result})
    else:
        return jsonify({'error': 'تبدیل نامعتبر است'}), 400

if __name__ == '__main__':
    app.run(debug=True)
