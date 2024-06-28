#!/usr/bin/env python

import utils.longhorn as longhorn
import core.backup as b
import core.volume as v
import core.wait as w
import os

LONGHORN_URL = os.getenv("LONGHORN_URL", "http://longhorn-frontend.longhorn/v1")
NAMESPACE = os.getenv("NAMESPACE", "default")
APP_NAME = os.getenv("APP_NAME", "longhorn-volume-manager-test")
VOLUME_NAME = os.getenv("VOLUME_NAME", "data")
VOLUME_SIZE = os.getenv("VOLUME_SIZE", 1)
VOLUME_ACCESS_MODE = os.getenv("VOLUME_ACCESS_MODE", "rwo")

FULL_VOLUME_NAME = NAMESPACE + "-" + APP_NAME + "-" + VOLUME_NAME

client = longhorn.Client(url = LONGHORN_URL)

def main():
    print("================================")    
    print("Starting Longhorn Volume Manager")
    print("================================")    

    # Check if volume exists
    volume = v.get_volume(client, FULL_VOLUME_NAME)
    if volume is not None:
        print(f"Volume '{FULL_VOLUME_NAME}' found, exiting.")
        return
    print(f"Volume '{FULL_VOLUME_NAME}' not found")

    # If volume does not exist, check if backup exists
    existing_backup = b.find_backup_volume(client, FULL_VOLUME_NAME)
    if existing_backup is not None:
        # If backup exists, restore from latest backup
        print(f"Backup volume '{FULL_VOLUME_NAME}' found, restoring from latest backup")
        b.restore_volume_from_latest_backup(client, FULL_VOLUME_NAME)
        w.wait_for_volume_detached(client, FULL_VOLUME_NAME)
        v.create_pv_pvc_from_volume(client, FULL_VOLUME_NAME, NAMESPACE)
        print(f"Volume '{FULL_VOLUME_NAME}' restored successfully!")
    else:
        # If backup does not exist, create new volume
        print(f"Backup volume '{FULL_VOLUME_NAME}' not found, creating new volume")
        v.create_volume(client, FULL_VOLUME_NAME, VOLUME_SIZE, VOLUME_ACCESS_MODE)
        w.wait_for_volume_detached(client, FULL_VOLUME_NAME)
        v.create_pv_pvc_from_volume(client, FULL_VOLUME_NAME, NAMESPACE)
        print(f"Volume '{FULL_VOLUME_NAME}' created successfully!")

main()