from flask import Flask, render_template_string, request
from holidays_finland_user_year import count_working_day_holidays

WEEKDAYS_FI = ['maanantai', 'tiistai', 'keskiviikko', 'torstai', 'perjantai', 'lauantai', 'sunnuntai']
WEEKDAYS_SV = ['måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lördag', 'söndag']
WEEKDAYS_NO = ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag']
WEEKDAYS_ET = ['esmaspäev', 'teisipäev', 'kolmapäev', 'neljapäev', 'reede', 'laupäev', 'pühapäev']

COUNTRIES = {
    'fi': {'en': 'Finland', 'fi': 'Suomi', 'sv': 'Finland', 'no': 'Finland', 'et': 'Soome'},
    'se': {'en': 'Sweden', 'fi': 'Ruotsi', 'sv': 'Sverige', 'no': 'Sverige', 'et': 'Rootsi'},
    'no': {'en': 'Norway', 'fi': 'Norja', 'sv': 'Norge', 'no': 'Norge', 'et': 'Norra'},
    'ee': {'en': 'Estonia', 'fi': 'Viro', 'sv': 'Estland', 'no': 'Estland', 'et': 'Eesti'}
}

app = Flask(__name__)

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Finnish Midweek Holidays</title>
    <style>
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            background: linear-gradient(120deg, #e0eafc, #cfdef3);
            min-height: 100vh;
        }
        .container {
            max-width: 600px;
            margin: 3em auto;
            background: #fff;
            border-radius: 12px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.08);
            padding: 2em 2.5em 2.5em 2.5em;
        }
        h2 {
            color: #2a5298;
            text-align: center;
        }
        label {
            font-weight: 500;
            color: #333;
        }
        input[type=number] {
            width: 120px;
            padding: 0.4em;
            border-radius: 5px;
            border: 1px solid #b2bec3;
            margin-right: 0.5em;
        }
        button {
            background: linear-gradient(90deg, #1e3c72, #2a5298);
            color: #fff;
            border: none;
            border-radius: 5px;
            padding: 0.5em 1.2em;
            font-size: 1em;
            cursor: pointer;
            transition: background 0.2s;
        }
        button:hover {
            background: linear-gradient(90deg, #2a5298, #1e3c72);
        }
        .holidays {
            margin-top: 2em;
        }
        .error {
            color: #d90429;
            background: #ffe3e3;
            border: 1px solid #ffb3b3;
            padding: 0.7em 1em;
            border-radius: 6px;
            margin-top: 1em;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 1em;
            background: #f8fafc;
            border-radius: 8px;
            overflow: hidden;
        }
        th, td {
            padding: 0.7em 0.5em;
            text-align: left;
        }
        th {
            background: #2a5298;
            color: #fff;
        }
        tr:nth-child(even) {
            background: #e0eafc;
        }
        tr:nth-child(odd) {
            background: #f6f9fb;
        }
    </style>
</head>
<body>
<div class="container">
    <h2>{{ 'Midweek Holidays' if lang == 'en' else 'Arkipäivälle osuvat pyhät' if lang == 'fi' else 'Helgdagar på vardagar' if lang == 'sv' else 'Helligdager på hverdager' if lang == 'no' else 'Pühadepäevad tööpäevadel' }}</h2>
    <form method="post">
        <label for="year">{{ 'Enter year (1900-2100):' if lang == 'en' else 'Anna vuosi (1900-2100):' if lang == 'fi' else 'Ange år (1900-2100):' if lang == 'sv' else 'Angi år (1900-2100):' if lang == 'no' else 'Sisesta aasta (1900-2100):' }}</label>
        <input type="number" id="year" name="year" min="1900" max="2100" required value="{{ year }}">
        <label for="country" style="margin-left:1em;">{{ 'Country:' if lang == 'en' else 'Maa:' if lang == 'fi' else 'Land:' if lang == 'sv' else 'Land:' if lang == 'no' else 'Riik:' }}</label>
        <select id="country" name="country">
            <option value="fi" {% if country == 'fi' %}selected{% endif %}>{{ countries['fi'][lang] }}</option>
            <option value="se" {% if country == 'se' %}selected{% endif %}>{{ countries['se'][lang] }}</option>
            <option value="no" {% if country == 'no' %}selected{% endif %}>{{ countries['no'][lang] }}</option>
            <option value="ee" {% if country == 'ee' %}selected{% endif %}>{{ countries['ee'][lang] }}</option>
        </select>
        <label for="lang" style="margin-left:1em;">{{ 'Language:' if lang == 'en' else 'Kieli:' if lang == 'fi' else 'Språk:' if lang == 'sv' else 'Språk:' if lang == 'no' else 'Keel:' }}</label>
        <select id="lang" name="lang">
            <option value="en" {% if lang == 'en' %}selected{% endif %}>English</option>
            <option value="fi" {% if lang == 'fi' %}selected{% endif %}>Suomi</option>
            <option value="sv" {% if lang == 'sv' %}selected{% endif %}>Svenska</option>
            <option value="no" {% if lang == 'no' %}selected{% endif %}>Norsk</option>
            <option value="et" {% if lang == 'et' %}selected{% endif %}>Eesti</option>
        </select>
        <button type="submit">{{ 'Show Holidays' if lang == 'en' else 'Näytä pyhät' if lang == 'fi' else 'Visa helgdagar' if lang == 'sv' else 'Vis helligdager' if lang == 'no' else 'Näita pühi' }}</button>
    </form>
    {% if error %}
        <div class="error">{{ error }}</div>
    {% endif %}
    {% if holidays %}
    <div class="holidays">
        <h3>
            {% if lang == 'en' %}
                In {{ year }}, there are {{ count }} public holidays in {{ countries[country][lang] }} that fall on a working day (Mon-Fri):
            {% elif lang == 'fi' %}
                Vuonna {{ year }} on {{ count }} arkipäivälle (ma-pe) osuvaa pyhäpäivää maassa {{ countries[country][lang] }}:
            {% elif lang == 'sv' %}
                År {{ year }} finns det {{ count }} helgdagar i {{ countries[country][lang] }} som infaller på en vardag (mån-fre):
            {% elif lang == 'no' %}
                I {{ year }} er det {{ count }} helligdager i {{ countries[country][lang] }} som faller på en hverdag (man-fre):
            {% else %}
                Aastal {{ year }} on {{ count }} püha {{ countries[country][lang] }} riigis, mis langevad tööpäevadele (E-R):
            {% endif %}
        </h3>
        <table>
            <thead>
                <tr>
                    <th>{{ 'Weekday' if lang == 'en' else 'Viikonpäivä' }}</th>
                    <th>{{ 'Date' if lang == 'en' else 'Päivämäärä' }}</th>
                    <th>{{ 'Holiday Name' if lang == 'en' else 'Pyhän nimi' }}</th>
                </tr>
            </thead>
            <tbody>
            {% for d, name in holidays %}
                <tr>
                    <td>
                        {% if lang == 'en' %}
                            {{ d.strftime('%A') }}
                        {% elif lang == 'fi' %}
                            {{ weekdays_fi[d.weekday()] }}
                        {% elif lang == 'sv' %}
                            {{ weekdays_sv[d.weekday()] }}
                        {% elif lang == 'no' %}
                            {{ weekdays_no[d.weekday()] }}
                        {% else %}
                            {{ weekdays_et[d.weekday()] }}
                        {% endif %}
                    </td>
                    <td>{{ d.strftime('%Y-%m-%d') }}</td>
                    <td>{{ name }}</td>
                </tr>
            {% endfor %}
            </tbody>
        </table>
    </div>
    {% endif %}
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    year = ''
    holidays = None
    count = 0
    error = ''
    lang = 'en'
    country = 'fi'
    if request.method == 'POST':
        year_input = request.form.get('year', '')
        lang = request.form.get('lang', 'en')
        country = request.form.get('country', 'fi')
        try:
            year = int(year_input)
            if year < 1900 or year > 2100:
                error_messages = {
                    'en': 'Please enter a valid year between 1900 and 2100.',
                    'fi': 'Anna vuosi väliltä 1900-2100.',
                    'sv': 'Ange ett år mellan 1900 och 2100.',
                    'no': 'Angi et år mellom 1900 og 2100.',
                    'et': 'Sisestage aasta vahemikus 1900-2100.'
                }
                error = error_messages.get(lang, error_messages['en'])
            else:
                count, holidays = count_working_day_holidays(year, lang=lang, country=country)
        except ValueError:
            error_messages = {
                'en': 'Please enter a valid integer year.',
                'fi': 'Anna kelvollinen vuosiluku.',
                'sv': 'Ange ett giltigt årtal.',
                'no': 'Angi et gyldig årstall.',
                'et': 'Sisestage kehtiv aastaarv.'
            }
            error = error_messages.get(lang, error_messages['en'])
    return render_template_string(
        HTML_TEMPLATE,
        year=year,
        holidays=holidays,
        count=count,
        error=error,
        lang=lang,
        country=country,
        countries=COUNTRIES,
        weekdays_fi=WEEKDAYS_FI,
        weekdays_sv=WEEKDAYS_SV,
        weekdays_no=WEEKDAYS_NO,
        weekdays_et=WEEKDAYS_ET
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
