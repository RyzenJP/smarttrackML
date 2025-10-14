#!/usr/bin/env python3
"""
Smart Track - Synthetic Data Generator for Maintenance Prediction
Generates realistic synthetic data based on maintenance schedule for ML training
"""

import pandas as pd
import numpy as np
import mysql.connector
from datetime import datetime, timedelta
import random
import json
import os

class SyntheticDataGenerator:
    def __init__(self, db_config):
        self.db_config = db_config
        # Map user schedule to maintenance_schedules enum values
        self.maintenance_schedule = {
            5000: {"tasks": ["oil_change"], "months": 3},
            10000: {"tasks": ["oil_change", "tire_rotation"], "months": 6},
            15000: {"tasks": ["oil_change"], "months": 9},
            20000: {"tasks": ["oil_change", "tire_rotation", "wheel_alignment", "brake_inspection"], "months": 12},
            25000: {"tasks": ["oil_change"], "months": 15},
            30000: {"tasks": ["oil_change", "tire_rotation"], "months": 18},
            35000: {"tasks": ["oil_change"], "months": 21},
            40000: {"tasks": ["oil_change", "tire_rotation", "wheel_alignment", "brake_inspection", "ac_maintenance"], "months": 24},
            45000: {"tasks": ["oil_change", "battery_check"], "months": 27},
            50000: {"tasks": ["oil_change", "tire_rotation"], "months": 30},
            55000: {"tasks": ["oil_change"], "months": 33},
            60000: {"tasks": ["oil_change", "tire_rotation", "wheel_alignment", "brake_inspection"], "months": 36},
            65000: {"tasks": ["oil_change"], "months": 39},
            70000: {"tasks": ["oil_change", "tire_rotation"], "months": 42},
            75000: {"tasks": ["oil_change"], "months": 45},
            80000: {"tasks": ["oil_change", "tire_rotation", "wheel_alignment", "brake_inspection", "ac_maintenance"], "months": 48},
            85000: {"tasks": ["oil_change", "battery_check"], "months": 51},
            90000: {"tasks": ["oil_change", "tire_rotation"], "months": 54},
            95000: {"tasks": ["oil_change"], "months": 57},
            100000: {"tasks": ["oil_change", "tire_rotation", "wheel_alignment", "brake_inspection"], "months": 60}
        }
    
    def connect_db(self):
        """Connect to MySQL database"""
        try:
            connection = mysql.connector.connect(
                host=self.db_config['host'],
                user=self.db_config['user'],
                password=self.db_config['password'],
                database=self.db_config['database'],
            )
            return connection
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    def get_existing_vehicles(self):
        """Get existing vehicles from database"""
        conn = self.connect_db()
        if not conn:
            return []
            
        try:
            query = "SELECT id, article, plate_number, created_at FROM fleet_vehicles WHERE status = 'active'"
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query)
            vehicles = cursor.fetchall()
            conn.close()
            return vehicles
        except Exception as e:
            print(f"Error fetching vehicles: {e}")
            conn.close()
            return []
    
    def generate_vehicle_usage_pattern(self, vehicle_age_days, total_km):
        """Generate realistic GPS usage patterns"""
        # Simulate daily usage patterns
        avg_daily_km = total_km / vehicle_age_days if vehicle_age_days > 0 else 50
        
        # Generate GPS points based on usage (more km = more GPS points)
        base_gps_points = int(avg_daily_km * 2)  # 2 GPS points per km on average
        gps_variation = random.uniform(0.7, 1.3)  # 30% variation
        
        return int(base_gps_points * gps_variation)
    
    def generate_maintenance_history(self, vehicle_id, vehicle_created, total_km):
        """Generate synthetic maintenance history for a vehicle"""
        maintenance_records = []
        
        # Start from vehicle creation date
        if isinstance(vehicle_created, datetime):
            current_date = vehicle_created
        else:
            current_date = datetime.strptime(vehicle_created, '%Y-%m-%d %H:%M:%S')
        current_km = 0
        
        # Generate maintenance records up to current total_km
        while current_km < total_km:
            # Find next maintenance milestone
            next_milestone = None
            for km in sorted(self.maintenance_schedule.keys()):
                if current_km < km:
                    next_milestone = km
                    break
            
            if next_milestone is None:
                break
            
            # Calculate when this maintenance should occur
            km_to_next = next_milestone - current_km
            days_to_next = int(km_to_next / 50)  # Assume 50 km per day average
            
            # Add some randomness to make it realistic
            days_variation = random.uniform(0.8, 1.2)  # 20% variation
            actual_days = int(days_to_next * days_variation)
            
            # Ensure we don't go beyond current date
            maintenance_date = current_date + timedelta(days=actual_days)
            if maintenance_date > datetime.now():
                break
            
            # Get maintenance tasks for this milestone
            maintenance_info = self.maintenance_schedule[next_milestone]
            tasks = maintenance_info["tasks"]
            
            # Create maintenance record
            maintenance_record = {
                'vehicle_id': vehicle_id,
                'maintenance_type': ', '.join(tasks),
                'scheduled_date': maintenance_date.strftime('%Y-%m-%d'),
                'start_time': '08:00:00',
                'end_time': '17:00:00',
                'status': 'completed',
                'notes': f'Synthetic maintenance at {next_milestone} km milestone',
                'assigned_mechanic': random.choice([1, 2, 3]),  # Random mechanic ID
                'created_at': maintenance_date.strftime('%Y-%m-%d %H:%M:%S'),
                'current_km': next_milestone
            }
            
            maintenance_records.append(maintenance_record)
            
            # Update for next iteration
            current_date = maintenance_date
            current_km = next_milestone
        
        return maintenance_records
    
    def generate_gps_logs(self, vehicle_id, device_id, vehicle_created, total_km):
        """Generate synthetic GPS logs for a vehicle"""
        gps_records = []
        
        # Start from vehicle creation
        if isinstance(vehicle_created, datetime):
            current_date = vehicle_created
        else:
            current_date = datetime.strptime(vehicle_created, '%Y-%m-%d %H:%M:%S')
        current_km = 0
        
        # Generate GPS points daily
        while current_km < total_km and current_date < datetime.now():
            # Daily usage varies
            daily_km = random.uniform(30, 80)  # 30-80 km per day
            
            # Generate GPS points for this day
            gps_points_today = random.randint(10, 50)  # 10-50 GPS points per day
            
            for i in range(gps_points_today):
                # Simulate GPS coordinates (Philippines area)
                lat = 14.5995 + random.uniform(-0.1, 0.1)  # Manila area
                lng = 120.9842 + random.uniform(-0.1, 0.1)
                
                # Add some movement simulation
                lat += random.uniform(-0.001, 0.001)
                lng += random.uniform(-0.001, 0.001)
                
                # Generate timestamp within the day
                hour = random.randint(6, 20)  # 6 AM to 8 PM
                minute = random.randint(0, 59)
                second = random.randint(0, 59)
                
                timestamp = current_date.replace(hour=hour, minute=minute, second=second)
                
                gps_record = {
                    'device_id': device_id,
                    'latitude': round(lat, 6),
                    'longitude': round(lng, 6),
                    'speed': random.uniform(0, 80),  # 0-80 km/h
                    'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S')
                }
                
                gps_records.append(gps_record)
            
            current_date += timedelta(days=1)
            current_km += daily_km
        
        return gps_records
    
    def insert_synthetic_data(self, maintenance_records, gps_records):
        """Insert synthetic data into database"""
        conn = self.connect_db()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            # Insert maintenance records
            print(f"📝 Inserting {len(maintenance_records)} maintenance records...")
            for record in maintenance_records:
                query = """
                INSERT INTO maintenance_schedules 
                (vehicle_id, maintenance_type, scheduled_date, start_time, end_time, 
                 status, notes, assigned_mechanic, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    record['vehicle_id'], record['maintenance_type'], 
                    record['scheduled_date'], record['start_time'], record['end_time'],
                    record['status'], record['notes'], record['assigned_mechanic'], 
                    record['created_at']
                ))
            
            # Insert GPS records
            print(f"📍 Inserting {len(gps_records)} GPS records...")
            for record in gps_records:
                query = """
                INSERT INTO gps_logs 
                (device_id, latitude, longitude, speed, timestamp)
                VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(query, (
                    record['device_id'], record['latitude'], record['longitude'],
                    record['speed'], record['timestamp']
                ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error inserting synthetic data: {e}")
            conn.rollback()
            conn.close()
            return False
    
    def generate_synthetic_data(self, num_vehicles=10, max_km=100000):
        """Generate synthetic data for multiple vehicles"""
        print("🚀 Starting synthetic data generation...")
        
        # Get existing vehicles
        existing_vehicles = self.get_existing_vehicles()
        if not existing_vehicles:
            print("❌ No vehicles found in database")
            return False
        
        # Use existing vehicles or create synthetic ones
        vehicles_to_process = existing_vehicles[:num_vehicles]
        
        total_maintenance_records = 0
        total_gps_records = 0
        
        for i, vehicle in enumerate(vehicles_to_process):
            print(f"\n📊 Processing vehicle {i+1}/{len(vehicles_to_process)}: {vehicle['article']}")
            
            # Generate random total kilometers for this vehicle
            if isinstance(vehicle['created_at'], datetime):
                vehicle_age_days = (datetime.now() - vehicle['created_at']).days
            else:
                vehicle_age_days = (datetime.now() - datetime.strptime(vehicle['created_at'], '%Y-%m-%d %H:%M:%S')).days
            total_km = min(random.uniform(5000, max_km), vehicle_age_days * 100)  # Realistic km based on age
            
            # Get device ID for this vehicle
            conn = self.connect_db()
            if not conn:
                continue
                
            cursor = conn.cursor()
            cursor.execute("SELECT device_id FROM gps_devices WHERE vehicle_id = %s", (vehicle['id'],))
            device_result = cursor.fetchone()
            conn.close()
            
            if not device_result:
                print(f"⚠️  No GPS device found for vehicle {vehicle['id']}, skipping...")
                continue
            
            device_id = device_result[0]
            
            # Generate maintenance history
            maintenance_records = self.generate_maintenance_history(
                vehicle['id'], vehicle['created_at'], total_km
            )
            
            # Generate GPS logs
            gps_records = self.generate_gps_logs(
                vehicle['id'], device_id, vehicle['created_at'], total_km
            )
            
            # Insert data
            if self.insert_synthetic_data(maintenance_records, gps_records):
                total_maintenance_records += len(maintenance_records)
                total_gps_records += len(gps_records)
                print(f"✅ Generated {len(maintenance_records)} maintenance records and {len(gps_records)} GPS records")
            else:
                print(f"❌ Failed to insert data for vehicle {vehicle['id']}")
        
        print(f"\n🎉 Synthetic data generation completed!")
        print(f"📊 Total maintenance records: {total_maintenance_records}")
        print(f"📍 Total GPS records: {total_gps_records}")
        print(f"🚗 Vehicles processed: {len(vehicles_to_process)}")
        
        return True
    
    def export_synthetic_data(self, filename="synthetic_data_sample.json"):
        """Export sample synthetic data for review"""
        sample_data = {
            "maintenance_schedule": self.maintenance_schedule,
            "sample_maintenance_record": {
                "vehicle_id": 1,
                "maintenance_type": "CHANGE OIL, TIRE ROTATION",
                "scheduled_date": "2024-01-15",
                "status": "completed",
                "notes": "Synthetic maintenance at 10000 km milestone"
            },
            "sample_gps_record": {
                "device_id": 1,
                "latitude": 14.599512,
                "longitude": 120.984222,
                "speed": 45.5,
                "timestamp": "2024-01-15 14:30:25"
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(sample_data, f, indent=2)
        
        print(f"📄 Sample data exported to {filename}")

def main():
    """Main function for CLI usage"""
    import sys
    
    # Database configuration (use environment variables with localhost-friendly defaults)
    db_config = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'user': os.getenv('DB_USER', 'root'),
        'password': os.getenv('DB_PASS', ''),
        'database': os.getenv('DB_NAME', 'trackingv2')
    }
    
    generator = SyntheticDataGenerator(db_config)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python generate_synthetic_data.py generate [num_vehicles] [max_km]")
        print("  python generate_synthetic_data.py export")
        print("\nExamples:")
        print("  python generate_synthetic_data.py generate 5 50000")
        print("  python generate_synthetic_data.py generate 10 100000")
        return
    
    command = sys.argv[1]
    
    if command == 'generate':
        num_vehicles = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        max_km = int(sys.argv[3]) if len(sys.argv) > 3 else 100000
        
        print(f"🚀 Generating synthetic data for {num_vehicles} vehicles (max {max_km} km)...")
        success = generator.generate_synthetic_data(num_vehicles, max_km)
        
        if success:
            print("\n✅ Synthetic data generation completed successfully!")
            print("🎯 You can now train your ML model with this data:")
            print("   python maintenance_predictor.py train")
        else:
            print("❌ Synthetic data generation failed!")
    
    elif command == 'export':
        print("📄 Exporting sample data structure...")
        generator.export_synthetic_data()
        print("✅ Sample data exported!")
    
    else:
        print("❌ Unknown command")

if __name__ == "__main__":
    main()
