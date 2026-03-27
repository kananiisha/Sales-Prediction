#!/usr/bin/env python
"""
Test script to verify Flask app setup
"""
from app import app, db

print("✅ Flask app imported successfully!")
print("\n📋 Available Routes:")
print("-" * 60)
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        methods = ','.join(rule.methods - {'OPTIONS', 'HEAD'})
        print(f"  {rule.rule:30} -> {rule.endpoint:20} [{methods}]")
print("-" * 60)

with app.app_context():
    tables = db.metadata.tables.keys()
    print(f"\n🗄️  Database Tables: {list(tables)}")
    print("\n✅ All systems ready! Run 'python app.py' to start the server.")
