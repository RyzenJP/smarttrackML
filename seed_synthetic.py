#!/usr/bin/env python3
import mysql.connector
from datetime import datetime, timedelta
import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', ''),
    'database': os.getenv('DB_NAME', 'trackingv2'),
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

SCHEDULE = {
    5000:  { 'tasks': ['oil_change'], 'months': 3 },
    10000: { 'tasks': ['oil_change','tire_rotation'], 'months': 6 },
    15000: { 'tasks': ['oil_change'], 'months': 9 },
    20000: { 'tasks': ['oil_change','tire_rotation','wheel_alignment','brake_inspection'], 'months': 12 },
    25000: { 'tasks': ['oil_change'], 'months': 15 },
    30000: { 'tasks': ['oil_change','tire_rotation'], 'months': 18 },
    35000: { 'tasks': ['oil_change'], 'months': 21 },
    40000: { 'tasks': ['oil_change','tire_rotation','wheel_alignment','brake_inspection','ac_maintenance'], 'months': 24 },
    45000: { 'tasks': ['oil_change','battery_check'], 'months': 27 },
    50000: { 'tasks': ['oil_change','tire_rotation'], 'months': 30 },
    55000: { 'tasks': ['oil_change'], 'months': 33 },
    60000: { 'tasks': ['oil_change','tire_rotation','wheel_alignment','brake_inspection'], 'months': 36 },
    65000: { 'tasks': ['oil_change'], 'months': 39 },
    70000: { 'tasks': ['oil_change','tire_rotation'], 'months': 42 },
    75000: { 'tasks': ['oil_change'], 'months': 45 },
    80000: { 'tasks': ['oil_change','tire_rotation','wheel_alignment','brake_inspection','ac_maintenance'], 'months': 48 },
    85000: { 'tasks': ['oil_change','battery_check'], 'months': 51 },
    90000: { 'tasks': ['oil_change','tire_rotation'], 'months': 54 },
    95000: { 'tasks': ['oil_change'], 'months': 57 },
    100000:{ 'tasks': ['oil_change','tire_rotation','wheel_alignment','brake_inspection'], 'months': 60 }
}

def ensure_vehicle(cur, name, unit, plate, current_mileage=0):
    cur.execute("SELECT id FROM fleet_vehicles WHERE plate_number=%s", (plate,))
    row = cur.fetchone()
    if row:
        vid = row[0]
        cur.execute("UPDATE fleet_vehicles SET current_mileage=%s WHERE id=%s", (current_mileage, vid))
        return vid
    cur.execute(
        "INSERT INTO fleet_vehicles (article, unit, plate_number, status, created_at, updated_at, current_mileage, last_maintenance_mileage, next_oil_change_mileage, next_general_maintenance_mileage, next_major_service_mileage) VALUES (%s,%s,%s,'active', NOW(), NOW(), %s, 0, 5000, 10000, 20000)",
        (name, unit, plate, current_mileage)
    )
    return cur.lastrowid

def ensure_device(cur, vehicle_id, plate):
    device_id = f"SYN-ESP32-{vehicle_id}"
    cur.execute("SELECT id FROM gps_devices WHERE device_id=%s", (device_id,))
    if cur.fetchone():
        return device_id
    cur.execute(
        "INSERT INTO gps_devices (device_id, imei, vehicle_id, status, created_at, updated_at, lat, lng, speed) VALUES (%s,%s,%s,'active', NOW(), NOW(), NULL, NULL, 0.00)",
        (device_id, f"SYNIMEI{vehicle_id:06d}", vehicle_id)
    )
    return device_id

def insert_maintenance(cur, vehicle_id, base_date):
    for km, info in SCHEDULE.items():
        # Backdate by months so entries are in the past and ordered
        months = info['months']
        sched_date = base_date - timedelta(days=months*30)
        for task in info['tasks']:
            cur.execute(
                "INSERT INTO maintenance_schedules (vehicle_id, maintenance_type, scheduled_date, start_time, end_time, status, notes, assigned_mechanic, created_at) VALUES (%s,%s,%s,%s,%s,'completed',%s,%s,%s)",
                (vehicle_id, task, sched_date, sched_date, sched_date + timedelta(hours=8), f'Synthetic maintenance at {km} km milestone', 1, sched_date)
            )

def delete_synthetic(cur):
    for i in range(1, 21):
        plate = f"SYN-{1000+i}"
        cur.execute("SELECT id FROM fleet_vehicles WHERE plate_number=%s", (plate,))
        row = cur.fetchone()
        if row:
            vid = row[0]
            cur.execute("DELETE FROM maintenance_schedules WHERE vehicle_id=%s", (vid,))
            cur.execute("DELETE FROM gps_devices WHERE vehicle_id=%s", (vid,))
            cur.execute("DELETE FROM fleet_vehicles WHERE id=%s", (vid,))

def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    # Force compatible collation for older MySQL
    try:
        cur0 = conn.cursor()
        cur0.execute("SET NAMES 'utf8mb4' COLLATE 'utf8mb4_general_ci'")
        cur0.close()
    except Exception:
        pass
    cur = conn.cursor()
    # Reset previous and recreate exactly 20 following milestones
    delete_synthetic(cur)
    milestones = [5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,60000,65000,70000,75000,80000,85000,90000,95000,100000]
    base_now = datetime.now()
    for idx, km in enumerate(milestones, start=1):
        plate = f"SYN-{1000+idx}"
        vid = ensure_vehicle(cur, f"Synthetic Vehicle {idx}", "SYN", plate, current_mileage=km)
        ensure_device(cur, vid, plate)
        # Insert maintenance rows up to current mileage
        for mkm, info in SCHEDULE.items():
            if mkm <= km:
                months = info['months']
                sched_date = base_now - timedelta(days=months*30)
                for task in info['tasks']:
                    cur.execute(
                        "INSERT INTO maintenance_schedules (vehicle_id, maintenance_type, scheduled_date, start_time, end_time, status, notes, assigned_mechanic, created_at) VALUES (%s,%s,%s,%s,%s,'completed',%s,%s,%s)",
                        (vid, task, sched_date, sched_date, sched_date + timedelta(hours=8), f'Synthetic maintenance at {mkm} km milestone', 1, sched_date)
                    )
    # Update ambulance current mileage
    cur.execute("UPDATE fleet_vehicles SET current_mileage=9000 WHERE plate_number='434-34e'")
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()


