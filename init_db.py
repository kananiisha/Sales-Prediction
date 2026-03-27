#!/usr/bin/env python
"""
Database Initialization Script
This script initializes the SQLite database and creates all tables.
Run this once before starting the app for the first time.
"""

from app import app, db, User, Prediction

def init_database():
    """Create all database tables"""
    with app.app_context():
        print("🔄 Initializing database...")
        
        # Drop existing tables (optional - remove if you want to keep data)
        # db.drop_all()
        # print("   Dropped existing tables")
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Show tables
        tables = db.metadata.tables.keys()
        print(f"\n📊 Tables created: {list(tables)}")
        
        # Show table structure
        print("\n📋 User Table Schema:")
        print("   - id (Integer, Primary Key)")
        print("   - name (String)")
        print("   - email (String, Unique)")
        print("   - password_hash (String)")
        
        print("\n📋 Prediction Table Schema:")
        print("   - id (Integer, Primary Key)")
        print("   - user_id (Integer, Foreign Key)")
        print("   - item_category, item_mrp, item_visibility, item_fat_content")
        print("   - outlet_type, outlet_size, outlet_location_type")
        print("   - outlet_establishment_year, festival_flag, discount_percentage")
        print("   - predicted_units_sold, timestamp")
        
        # Count existing data
        user_count = User.query.count()
        pred_count = Prediction.query.count()
        
        print(f"\n📊 Current Data:")
        print(f"   - Users: {user_count}")
        print(f"   - Predictions: {pred_count}")
        
        print("\n✅ Database ready! Start the app with: python app.py")

def create_sample_user():
    """Create a sample user for testing (optional)"""
    with app.app_context():
        # Check if demo user already exists
        if User.query.filter_by(email='demo@example.com').first():
            print("Demo user already exists!")
            return
        
        # Create demo user
        user = User(name='Demo User', email='demo@example.com')
        user.set_password('demo123')
        db.session.add(user)
        db.session.commit()
        
        print("✅ Demo user created!")
        print("   Email: demo@example.com")
        print("   Password: demo123")

if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("BigMart Sales Prediction - Database Initialization")
    print("=" * 60)
    
    init_database()
    
    # Create sample user if requested
    if len(sys.argv) > 1 and sys.argv[1] == '--create-demo':
        print("\n" + "=" * 60)
        create_sample_user()
    
    print("\n" + "=" * 60)
    print("🎉 Setup complete! Ready to run the application.")
    print("=" * 60)
