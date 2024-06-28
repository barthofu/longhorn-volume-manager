import random
import time


def get_volumes(client):
    return client.list_volume().data

def get_volume(client, volume_name: str):
    return client.by_id_volume(volume_name)

def create_volume(client, name: str, size: int, access: str = "rwo"):
    return client.create_volume(
        name = name,
        size = str(size) + "Gi",
        accessMode = access
    )

def create_pv_pvc_from_volume(client, volume_name: str, namespace: str):
    volume = client.by_id_volume(volume_name)
    if volume is None:
        print(f"Volume '{volume_name}' not found, exiting with error.")
        exit(1)
    
    volume.pvCreate(
        pvName="pv-" + volume_name, 
        fsType="ext4", 
        storageClassName=""
    )
    time.sleep(random.randint(3, 15))
    volume.pvcCreate(
        pvcName="pvc-" + volume_name, 
        namespace=namespace
    )