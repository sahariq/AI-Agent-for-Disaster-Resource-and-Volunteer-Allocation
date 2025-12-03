# ChatGPT Prompt: Generate Working CSV Dataset for Disaster Response System

Copy and paste this entire prompt into ChatGPT:

---

**I need you to generate a CSV dataset for a disaster response volunteer allocation system. The CSV must have EXACT column names and proper data types that work with my Python code.**

## Critical Requirements

1. **ALL numeric columns must be NUMBERS (not strings)** - no quotes around numbers
2. **Column names must match EXACTLY** (case-sensitive)
3. **One row per zone** (multiple zones per scenario)
4. **Proper CSV formatting** - escape commas in text fields with quotes

## Required CSV Structure

The CSV must have these columns in this exact order:

```csv
scenario_id,scenario_name,scenario_type,zone_id,zone_name,location,latitude,longitude,severity,severity_description,required_volunteers,capacity,estimated_victims,resources_available,min_resources_per_volunteer,infrastructure_damage,hazards,resources_needed,scenario_timestamp,duration_hours,affected_population,casualty_estimate,available_volunteers,response_teams
```

## Column Specifications

### REQUIRED Columns (must have correct data types):

1. **scenario_id** (string): Unique scenario ID like "SCENARIO_001", "SCENARIO_002"
2. **scenario_name** (string): Name like "Urban Earthquake", "Flood Relief"
3. **scenario_type** (string): "Earthquake", "Flood", "Wildfire", "Hurricane", "Tornado", "Tsunami", "Pandemic", "Industrial"
4. **zone_id** (string): Zone identifier like "Z1", "Z2", "Z3"
5. **zone_name** (string): Descriptive name like "Downtown District", "Suburban Area"
6. **location** (string): General location like "Downtown", "Suburbs", "Coastal"
7. **latitude** (FLOAT/NUMBER): Geographic latitude, e.g., 40.7128 (NO quotes, must be numeric)
8. **longitude** (FLOAT/NUMBER): Geographic longitude, e.g., -74.0060 (NO quotes, must be numeric)
9. **severity** (INTEGER): Priority level 1-10 (1=Minimal, 5=Critical, 10=Extreme) - MUST be integer, no decimals
10. **severity_description** (string): "Critical", "High", "Moderate", "Low", "Extreme"
11. **required_volunteers** (INTEGER): Number needed, typically 3-30 - MUST be integer
12. **capacity** (INTEGER): Maximum volunteers zone can hold, should be >= required_volunteers - MUST be integer
13. **estimated_victims** (INTEGER): Estimated victims, typically 10-1000 - MUST be integer
14. **resources_available** (INTEGER): Resource units available, typically 30-500 - MUST be integer
15. **min_resources_per_volunteer** (FLOAT): Resource ratio like 3.0, 4.0, 5.0 - MUST be numeric
16. **infrastructure_damage** (string): Description like "High - Multiple building collapses"
17. **hazards** (string): Comma-separated like "Structural instability, Gas leaks, Electrical hazards" (use quotes if contains commas)
18. **resources_needed** (string): Comma-separated like "Medical supplies, Heavy machinery, Search dogs" (use quotes if contains commas)
19. **scenario_timestamp** (string): ISO format like "2025-12-02T10:00:00Z"
20. **duration_hours** (INTEGER): Expected duration 24-168 hours - MUST be integer
21. **affected_population** (INTEGER): Total affected, typically 10000-500000 - MUST be integer
22. **casualty_estimate** (INTEGER): Total casualties, typically 50-2000 - MUST be integer
23. **available_volunteers** (INTEGER): Total volunteers available for ALL zones in scenario - MUST be integer, SAME VALUE for all zones in same scenario
24. **response_teams** (string): JSON-like string like '[{"team_id":"T1","specialty":"Search and Rescue","capacity":4}]' (use quotes)

## Data Rules

1. **Numeric columns MUST be numbers** - NO quotes around: latitude, longitude, severity, required_volunteers, capacity, estimated_victims, resources_available, min_resources_per_volunteer, duration_hours, affected_population, casualty_estimate, available_volunteers

2. **available_volunteers** - This is the TOTAL volunteers for the ENTIRE scenario. All zones in the same scenario must have the SAME value. For example, if SCENARIO_001 has 3 zones, all 3 zones should have the same available_volunteers value (e.g., 25).

3. **Realistic relationships**:
   - Higher severity (7-10) should require more volunteers (15-30)
   - Lower severity (1-4) should require fewer volunteers (3-10)
   - capacity >= required_volunteers
   - Sum of required_volunteers across zones often exceeds available_volunteers (creates allocation challenge)
   - Geographic coordinates should be realistic (not all the same)

4. **Each scenario should have 2-5 zones** with varying severity levels

## Example Row (showing proper formatting):

```csv
SCENARIO_001,Urban Earthquake,Earthquake,Z1,Downtown District,Downtown,40.7128,-74.0060,5,Critical,8,10,150,50,4.0,"High - Multiple building collapses","Structural instability, Gas leaks, Electrical hazards","Medical supplies, Heavy machinery, Search dogs",2025-12-02T10:00:00Z,48,50000,250,12,"[{\"team_id\":\"T1\",\"specialty\":\"Search and Rescue\",\"capacity\":4}]"
```

Notice:
- Numbers have NO quotes (40.7128, -74.0060, 5, 8, 10, etc.)
- Text with commas is in quotes ("High - Multiple building collapses")
- available_volunteers is 12 (same for all zones in SCENARIO_001)

## Output Requirements

Generate a CSV file with:
- **At least 15-20 unique scenarios**
- **40-60 total rows** (zones)
- **Header row with exact column names**
- **All numeric columns as actual numbers** (not strings)
- **Proper CSV escaping** for text fields with commas
- **Realistic, diverse disaster data**

## Important Notes

- The code uses pandas.read_csv() and expects numeric columns to be automatically detected as numbers
- If numbers are in quotes, the code will fail with type conversion errors
- The available_volunteers must be the same for all zones within the same scenario_id
- Make sure severity is an integer (1, 2, 3... not 1.0, 2.0, 3.0)

Please generate the CSV with proper formatting and data types that will work seamlessly with Python pandas processing.

---

**After ChatGPT generates the CSV, save it and test it by loading it into the dashboard. All numeric columns should be recognized as numbers automatically.**

