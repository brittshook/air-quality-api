AQI_CATEGORIES = {
    'good': {'min': 0, 'max': 50, 'description': 'Air quality is satisfactory, and air pollution poses little or no risk.'},
    'moderate': {'min': 51, 'max': 100, 'description': 'Air quality is acceptable; however, there may be a risk for some people, particularly who are unusually sensitive to air pollution.'},
    'unhealthy_sensitive': {'min': 101, 'max': 150, 'description': 'Members of sensitive groups may experience health effects. The general public is not likely to be affected.'},
    'unhealthy': {'min': 151, 'max': 200, 'description': 'Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.'},
    'very_unhealthy': {'min': 201, 'max': 300, 'description': 'Health alert: everyone may experience more serious health effects from air pollution.'},
    'hazardous': {'min': 301, 'max': 500, 'description': 'Health warnings of emergency conditions; the entire population is more likely to be affected.'},
}