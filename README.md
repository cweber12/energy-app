# Energy App Database Overview

## Database Schema

The Energy App uses a relational SQLite database to track electrical item usage and compare it to hourly utility metrics. The schema is organized into several tables, each serving a specific purpose:

### Users
- Stores user accounts with unique usernames and emails.

### Homes
- Each home is linked to a user.
- Includes a nickname and zip code for location tracking.

### Item Categories
- Defines categories for electrical items (e.g., appliances, lighting).

### Usage Types
- Describes how items are used (e.g., continuous, intermittent).

### Electrical Items
- Represents devices in a home.
- Linked to a home, category, and usage type.
- Stores a nickname and rated wattage.

### Item Usage Events
- Records when an electrical item is used.
- Tracks start and end timestamps for each usage event.

### Meter
- Represents a utility meter for a home.

### Meter Hourly Readings
- Stores hourly energy consumption readings from a meter.
- Includes start/end timestamps and kWh consumed.

### Monthly Utility Rate
- Tracks utility rates for a home on a monthly basis.

## Database Population

To set up and populate the database:

1. **Schema Creation:**  
   - The database tables are created using a SQL script (`populate_database.sql`).
   - This script defines all tables, relationships, and constraints.

2. **Initial Data:**  
   - The script can be extended to insert sample data for users, homes, item categories, usage types, and electrical items.
   - This helps with initial testing and development.

3. **Referential Integrity:**  
   - Foreign key constraints ensure data consistency between related tables ( homes and users, items and homes).

## Getting Started

- Run the provided SQL script (`populate_database.sql`) against your SQLite database to create all necessary tables and relationships.
- You can add sample data to the script or use the backend API to populate the tables.

---
# Energy App Database Overview

## Database Schema

The Energy App uses a relational SQLite database to track electrical item usage and compare it to hourly utility metrics. The schema is organized into several tables, each serving a specific purpose:

### Users
- Stores user accounts with unique usernames and emails.

### Homes
- Each home is linked to a user.
- Includes a nickname and zip code for location tracking.

### Item Categories
- Defines categories for electrical items (e.g., appliances, lighting).

### Usage Types
- Describes how items are used (e.g., continuous, intermittent).

### Electrical Items
- Represents devices in a home.
- Linked to a home, category, and usage type.
- Stores a nickname and rated wattage.

### Item Usage Events
- Records when an electrical item is used.
- Tracks start and end timestamps for each usage event.

### Meter
- Represents a utility meter for a home.

### Meter Hourly Readings
- Stores hourly energy consumption readings from a meter.
- Includes start/end timestamps and kWh consumed.

### Monthly Utility Rate
- Tracks utility rates for a home on a monthly basis.

## Database Population

To set up and populate the database:

1. **Schema Creation:**  
   - The database tables are created using a SQL script (`populate_database.sql`).
   - This script defines all tables, relationships, and constraints.

2. **Initial Data:**  
   - The script can be extended to insert sample data for users, homes, item categories, usage types, and electrical items.
   - This helps with initial testing and development.

3. **Referential Integrity:**  
   - Foreign key constraints ensure data consistency between related tables (e.g., homes and users, items and homes).

## Getting Started

- Run the provided SQL script (`populate_database.sql`) against your SQLite database to create all necessary tables and relationships.
- You can add sample data to the script or use the backend API to populate the tables.

## Opening DB
```powershell
& "C:\Users\coled\AppData\Local\Microsoft\WinGet\Packages\SQLite.SQLite_Microsoft.Winget.Source_8wekyb3d8bbwe\sqlite3.exe" energy.db
