#!/usr/bin/env python3
import mysql.connector
import os

DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASS', ''),
    'database': os.getenv('DB_NAME', 'trackingv2'),
}

def main():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    plates = [f"SYN-{1000+i}" for i in range(1,21)]
    kms = [5000,10000,15000,20000,25000,30000,35000,40000,45000,50000,55000,60000,65000,70000,75000,80000,85000,90000,95000,100000]
    for plate, km in zip(plates, kms):
        cur.execute("UPDATE fleet_vehicles SET current_mileage=%s WHERE plate_number=%s", (km, plate))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    main()


