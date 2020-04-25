"""geographic lists and dicts to aid in transforming the location/place strings to match with covid numbers values"""

countries = [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Benin",
    "Bhutan",
    "Bolivia",
    "Bosnia and Herzegovina",
    "Brazil",
    "Brunei",
    "Bulgaria",
    "Burkina Faso",
    "Cabo Verde",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Congo (Brazzaville)",
    "Congo (Kinshasa)",
    "Costa Rica",
    "Cote d'Ivoire",
    "Croatia",
    "Diamond Princess",
    "Cuba",
    "Cyprus",
    "Czechia",
    "Denmark",
    "Djibouti",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Eswatini",
    "Ethiopia",
    "Fiji",
    "Finland",
    "France",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Guatemala",
    "Guinea",
    "Guyana",
    "Haiti",
    "Holy See",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Korea, South",
    "Kuwait",
    "Kyrgyzstan",
    "Latvia",
    "Lebanon",
    "Liberia",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Madagascar",
    "Malaysia",
    "Maldives",
    "Malta",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Moldova",
    "Monaco",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Namibia",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Macedonia",
    "Norway",
    "Oman",
    "Pakistan",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Qatar",
    "Romania",
    "Russia",
    "Rwanda",
    "Saint Lucia",
    "Saint Vincent and the Grenadines",
    "San Marino",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Seychelles",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Somalia",
    "South Africa",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Sweden",
    "Switzerland",
    "Taiwan",
    "Tanzania",
    "Thailand",
    "Togo",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "Uruguay",
    "United States",
    "Uzbekistan",
    "Venezuela",
    "Vietnam",
    "Zambia",
    "Zimbabwe",
    "Dominica",
    "Grenada",
    "Mozambique",
    "Syria",
    "Timor-Leste",
    "Belize",
    "Laos",
    "Libya",
    "West Bank and Gaza",
    "Guinea-Bissau",
    "Mali",
    "Saint Kitts and Nevis",
    "Kosovo",
    "Burma",
    "MS Zaandam",
    "Botswana",
    "Burundi",
    "Sierra Leone",
    "Malawi",
    "South Sudan",
    "Western Sahara",
    "Sao Tome and Principe",
    "Yemen",
]

state_provinces = [
    "Alberta",
    "Anguilla",
    "Anhui",
    "Aruba",
    "Australian Capital Territory",
    "Beijing",
    "Bermuda",
    "Bonaire, Sint Eustatius and Saba",
    "British Columbia",
    "British Virgin Islands",
    "Cayman Islands",
    "Channel Islands",
    "Chongqing",
    "Curacao",
    "Diamond Princess",
    "Falkland Islands (Malvinas)",
    "Faroe Islands",
    "French Guiana",
    "French Polynesia",
    "Fujian",
    "Gansu",
    "Gibraltar",
    "Grand Princess",
    "Greenland",
    "Guadeloupe",
    "Guangdong",
    "Guangxi",
    "Guizhou",
    "Hainan",
    "Hebei",
    "Heilongjiang",
    "Henan",
    "Hong Kong",
    "Hubei",
    "Hunan",
    "Inner Mongolia",
    "Isle of Man",
    "Jiangsu",
    "Jiangxi",
    "Jilin",
    "Liaoning",
    "Macau",
    "Manitoba",
    "Martinique",
    "Mayotte",
    "Montserrat",
    "New Brunswick",
    "New Caledonia",
    "New South Wales",
    "Newfoundland and Labrador",
    "Ningxia",
    "Northern Territory",
    "Northwest Territories",
    "Nova Scotia",
    "Ontario",
    "Prince Edward Island",
    "Qinghai",
    "Quebec",
    "Queensland",
    "Recovered",
    "Reunion",
    "Saint Barthelemy",
    "Saint Pierre and Miquelon",
    "Saskatchewan",
    "Shaanxi",
    "Shandong",
    "Shanghai",
    "Shanxi",
    "Sichuan",
    "Sint Maarten",
    "South Australia",
    "St Martin",
    "Tasmania",
    "Tianjin",
    "Tibet",
    "Turks and Caicos Islands",
    "Victoria",
    "Western Australia",
    "Xinjiang",
    "Yukon",
    "Yunnan",
    "Zhejiang",
]

state_province_to_country = {
    "Anhui": "China",
    "Beijing": "China",
    "Chongqing": "China",
    "Fujian": "China",
    "Gansu": "China",
    "Guangdong": "China",
    "Guangxi": "China",
    "Guizhou": "China",
    "Hainan": "China",
    "Hebei": "China",
    "Heilongjiang": "China",
    "Henan": "China",
    "Hong Kong": "China",
    "Hubei": "China",
    "Hunan": "China",
    "Inner Mongolia": "China",
    "Jiangsu": "China",
    "Jiangxi": "China",
    "Jilin": "China",
    "Liaoning": "China",
    "Macau": "China",
    "Ningxia": "China",
    "Qinghai": "China",
    "Shaanxi": "China",
    "Shandong": "China",
    "Shanghai": "China",
    "Shanxi": "China",
    "Sichuan": "China",
    "Tianjin": "China",
    "Tibet": "China",
    "Xinjiang": "China",
    "Yunnan": "China",
    "Zhejiang": "China",
    "Aruba": "Netherlands",
    "Curacao": "Netherlands",
    "Sint Maarten": "Netherlands",
    "Bonaire, Sint Eustatius and Saba": "Netherlands",
    "Australian Capital Territory": "Australia",
    "New South Wales": "Australia",
    "Northern Territory": "Australia",
    "Queensland": "Australia",
    "South Australia": "Australia",
    "Tasmania": "Australia",
    "Victoria": "Australia",
    "Western Australia": "Australia",
    "French Guiana": "France",
    "French Polynesia": "France",
    "Guadeloupe": "France",
    "Mayotte": "France",
    "New Caledonia": "France",
    "Reunion": "France",
    "Saint Barthelemy": "France",
    "St Martin": "France",
    "Martinique": "France",
    "Saint Pierre and Miquelon": "France",
    "Alberta": "Canada",
    "British Columbia": "Canada",
    "Grand Princess": "Canada",
    "Manitoba": "Canada",
    "New Brunswick": "Canada",
    "Newfoundland and Labrador": "Canada",
    "Nova Scotia": "Canada",
    "Ontario": "Canada",
    "Prince Edward Island": "Canada",
    "Quebec": "Canada",
    "Saskatchewan": "Canada",
    "Diamond Princess": "Canada",
    "Recovered": "Canada",
    "Northwest Territories": "Canada",
    "Yukon": "Canada",
    "Faroe Islands": "Denmark",
    "Greenland": "Denmark",
    "Bermuda": "United Kingdom",
    "Cayman Islands": "United Kingdom",
    "Channel Islands": "United Kingdom",
    "Gibraltar": "United Kingdom",
    "Isle of Man": "United Kingdom",
    "Montserrat": "United Kingdom",
    "Anguilla": "United Kingdom",
    "British Virgin Islands": "United Kingdom",
    "Turks and Caicos Islands": "United Kingdom",
    "Falkland Islands (Malvinas)": "United Kingdom",
}

us_state_provinces = [
    "Alabama",
    "Alaska",
    "American Samoa",
    "Arizona",
    "Arkansas",
    "California",
    "Colorado",
    "Connecticut",
    "Delaware",
    "Diamond Princess",
    "District of Columbia",
    "Florida",
    "Georgia",
    "Grand Princess",
    "Guam",
    "Hawaii",
    "Idaho",
    "Illinois",
    "Indiana",
    "Iowa",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Maine",
    "Maryland",
    "Massachusetts",
    "Michigan",
    "Minnesota",
    "Mississippi",
    "Missouri",
    "Montana",
    "Nebraska",
    "Nevada",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "New York",
    "North Carolina",
    "North Dakota",
    "Northern Mariana Islands",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Puerto Rico",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Vermont",
    "Virgin Islands",
    "Virginia",
    "Washington",
    "West Virginia",
    "Wisconsin",
    "Wyoming",
]

us_state_province_to_country = dict((state, "United States") for state in us_state_provinces)

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "American Samoa": "AS",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Guam": "GU",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Northern Mariana Islands": "MP",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Puerto Rico": "PR",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virgin Islands": "VI",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

abbrev_to_us_state = dict((v, k) for (k, v) in us_state_to_abbrev.items())

abbrvs_or_misspelling = {
    **dict((country, (None, country)) for country in countries),
    **dict((state, (state, country)) for (state, country) in state_province_to_country.items()),
    **dict((f"{state}, {country}", (state, country)) for (state, country) in state_province_to_country.items()),
    **dict((f"{state}, United States", (state, "United States")) for (abbr, state) in abbrev_to_us_state.items()),
    **dict((f"{abbr}, United States", (state, "United States")) for (abbr, state) in abbrev_to_us_state.items()),
    **dict((f"{state}, US", (state, "United States")) for (abbr, state) in abbrev_to_us_state.items()),
    **dict((f"{abbr}, US", (state, "United States")) for (abbr, state) in abbrev_to_us_state.items()),
    **dict((f"{state}, USA", (state, "United States")) for (abbr, state) in abbrev_to_us_state.items()),
    **dict((f"{abbr}, USA", (state, "United States")) for (abbr, state) in abbrev_to_us_state.items()),
    **dict((f"{state}", (state, "United States")) for (abbr, state) in abbrev_to_us_state.items()),
    **dict((f"{abbr}", (state, "United States")) for (abbr, state) in abbrev_to_us_state.items()),
    "US": (None, "United States"),
    "USA": (None, "United States"),
    "Hong Kong": (None, "Hong Kong"),
    "Malaysia": (None, "Malaysia"),
    "Indonesia": (None, "Indonesia"),
    "London, England": (None, "United Kingdom"),
    "India": (None, "India"),
    "Republic of the Philippines": (None, "Philippines"),
    "Canada": (None, "Canada"),
    "Australia": (None, "Australia"),
    "Los Angeles, CA": ("California", "United States"),
    "Texas, USA": ("Texas", "United States"),
    "Singapore": (None, "Singapore"),
    "Philippines": (None, "Philippines"),
    "Toronto, Ontario": ("Ontario", "Canada"),
    "New York, NY": ("New York", "United States"),
    "Washington, DC": ("District of Columbia", "United States"),
    "London": (None, "United Kingdom"),
    "United Kingdom": (None, "United Kingdom"),
    "Chicago, IL": ("Illinois", "United States"),
    "Thailand": (None, "Thailand"),
    "Nigeria": (None, "Nigeria"),
    "England, United Kingdom": (None, "United Kingdom"),
    "Houston, TX": ("Texas", "United States"),
    "Dallas, TX": ("Texas", "United States"),
    "Selangor, Malaysia": (None, "Malaysia"),
    "Nairobi, Kenya": (None, "Kenya"),
    "Bangkok, Thailand": (None, "Thailand"),
    "Paris, France": (None, "France"),
    "Atlanta, GA": ("Georgia", "United States"),
    "New Delhi, India": (None, "India"),
    "France": (None, "France"),
    "Toronto": ("Ontario", "Canada"),
    "New South Wales": ("New South Wales", "Australia"),
    "Ontario, Canada": ("Ontario", "Canada"),
    "UK": (None, "United Kingdom"),
    "Venezuela": (None, "Venezuela"),
    "香港": (None, "Hong Kong"),
    "🇵🇭NYC": ("New York", "United States"),
    "Boston, MA": ("Massachusetts", "United States"),
    "Pakistan": (None, "Pakistan"),
    "Melbourne, Victoria": ("Victoria", "Australia"),
    "México	": (None, "Mexico"),
    "South Africa": (None, "South Africa"),
    "Maldives": (None, "United States"),
    "ประเทศไทย": (None, "Thailand"),
    "Brasil": (None, "Brazil"),
    "Las Vegas, NV": ("Nevada", "United States"),
    "Kuala Lumpur": (None, "Malaysia"),
    "Mumbai, India": (None, "India"),
    "Mumbai": (None, "India"),
    "San Diego, CA": ("San Diego", "United States"),
    "Manila, Philippines": (None, "Philippines"),
    "Abuja, Nigeria": (None, "Nigeria"),
    "Miami, FL": ("Florida", "United States"),
    "Austin, TX": ("Texas", "United States"),
    "NYC": ("New York", "United States"),
    "Brooklyn, NY": ("New York", "United States"),
    "Buenos Aires, Argentina": (None, "Argentina"),
    "Vancouver, British Columbia": ("British Columbia", "Canada"),
    "New York City": ("New York", "United States"),
    "Seoul, Republic of Korea": (None, "Korea, South"),
    "São Paulo, Brasil": (None, "Brazil"),
    "Rio de Janeiro, Brasil": (None, "Brazil"),
    "Johannesburg, South Africa": (None, "South Africa"),
    "กรุงเทพมหานคร, ประเทศไทย": (None, "Thailand"),
    "Los Angeles": ("California", "United States"),
    "Dubai, United Arab Emirates": (None, "United Arab Emirates"),
    "Johor Bahru, Johor": (None, "Malaysia"),
    "España": (None, "Spain"),
    "Johore, Malaysia": (None, "Malaysia"),
    "Manila": (None, "Philippines"),
    "Sydney, Australia": ("New South Wales", "Australia"),
    "日本": (None, "Japan"),
    "Islamabad, Pakistan": (None, "Pakistan"),
    "PH": (None, "Philippines"),
    "Bengaluru, India": (None, "India"),
    "Deutschland": (None, "Germany"),
    "Manchester, England": (None, "United Kingdom"),
    "İstanbul, Türkiye": (None, "Turkey"),
    "Italia": (None, "Italy"),
    "Belgique": (None, "Belgium"),
    "Sydney": ("New South Wales", "Australia"),
    "Chicago": ("Illinois", "United States"),
    "San Antonio, TX": ("Texas", "United States"),
    "Perak, Malaysia": (None, "Malaysia"),
    "Jakarta": (None, "Indonesia"),
    "Jakarta, Indonesia": (None, "Indonesia"),
    "Yogyakarta, Indonesia": (None, "Indonesia"),
    "Cebu City, Central Visayas": (None, "Philippines"),
    "London, UK": (None, "United Kingdom"),
    "Karachi, Pakistan": (None, "Pakistan"),
    "Toronto, Canada": ("Ontario", "Canada"),
    "Ontario": ("Ontario", "Canada"),
    "Ottawa, Ontario": ("Ontario", "Canada"),
    "Melbourne, Australia": ("Victoria", "Australia"),
    "Denver, CO": ("Colorado", "United States"),
    "Davao City, Davao Region": (None, "Philippines"),
    "Lahore, Pakistan": (None, "Pakistan"),
    "Hyderabad, India": (None, "India"),
    "England": (None, "United Kingdom"),
    "Paris": (None, "France"),
    "Nairobi": (None, "Kenya"),
    "Quezon City": (None, "Philippines"),
    "Lagos": (None, "Nigeria"),
    "New Delhi": (None, "India"),
    "Kedah, Malaysia": (None, "Malaysia"),
    "Caracas, Venezuela": (None, "Venezuela"),
    "Chennai, India": (None, "India"),
    "Jakarta Capital Region": (None, "Indonesia"),
    "Manhattan, NY": ("New York", "United States"),
    "Calgary, Alberta": ("Alberta", "Canada"),
    "Alberta, Canada": ("Alberta", "Canada"),
    "Orlando, FL": ("Florida", "United States"),
    "MNL": (None, "Philippines"),
    "Bangkok": (None, "Thailand"),
    "Bogotá, D.C., Colombia": (None, "Colombia"),
    "Charlotte, NC": ("North Carolina", "United States"),
    "United States of America": (None, "United States"),
    "America": (None, "United States"),
    "Shanghai": (None, "India"),
    "Minneapolis, MN": ("Minnesota", "United States"),
    "Perth, Western Australia": ("Western Australia", "Australia"),
    "National Capital Region": (None, "United States"),
    "Pittsburgh, PA": ("Pennsylvania", "United States"),
    "Kuching, Sarawak": (None, "Malaysia"),
    "Kuala Lumpur Federal Territory": (None, "Malaysia"),
    "Cape Town, South Africa": (None, "South Africa"),
    "Melbourne": ("Victoria", "Australia"),
    "Washington, D.C.": ("District of Columbia", "United States"),
    "Washington DC": ("District of Columbia", "United States"),
    "People's Republic of China": (None, "China"),
    "Scotland, United Kingdom": (None, "United Kingdom"),
    "Montréal, Québec": ("Quebec", "Canada"),
    "Montreal, Quebec": ("Quebec", "Canada"),
    "Québec, Canada": ("Quebec", "Canada"),
    "Quebec": ("Quebec", "Canada"),
}
