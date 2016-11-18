import mission_control.database

print("This will purge the existing database and remove all data stored there")
print("Are you sure you want to continue [y/N]?")
inp = input()
if str(inp).lower() == 'y':
    mission_control.database.init_db()
