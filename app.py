from flask import Flask
from flask_cors import CORS
from queries.users import users_bp
from queries.homes import homes_bp
from queries.electrical_item import electrical_item_bp
from queries.item_usage_event import item_usage_event_bp
from queries.item_category import item_category_bp
from queries.usage_type import usage_type_bp
from queries.meter import meter_bp
from queries.meter_hourly_reading import meter_hourly_reading_bp
from queries.utility_rate import utility_rate_bp

app = Flask(__name__)

CORS(app)

# Register all Blueprints
app.register_blueprint(users_bp)
print("Registered users blueprint: ", users_bp)
app.register_blueprint(homes_bp)
print("Registered homes blueprint: ", homes_bp)
app.register_blueprint(electrical_item_bp)
print("Registered electrical_item blueprint: ", electrical_item_bp)
app.register_blueprint(item_usage_event_bp)
print("Registered item_usage_event blueprint: ", item_usage_event_bp)
app.register_blueprint(item_category_bp)
print("Registered item_category blueprint: ", item_category_bp)
app.register_blueprint(usage_type_bp)
print("Registered usage_type blueprint: ", usage_type_bp)
app.register_blueprint(meter_bp)
print("Registered meter blueprint: ", meter_bp)
app.register_blueprint(meter_hourly_reading_bp)
print("Registered meter_hourly_reading blueprint: ", meter_hourly_reading_bp)
app.register_blueprint(utility_rate_bp)
print("Registered utility_rate blueprint: ", utility_rate_bp)

@app.route('/')
def index():
    return "Energy App API is running."

if __name__ == '__main__':
    app.run(debug=True)