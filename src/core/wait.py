import time 
import os

RETRY_COMMAND_COUNT = 3
RETRY_COUNTS = 300
RETRY_INTERVAL = 0.5

VOLUME_FIELD_STATE = "state"
VOLUME_STATE_ATTACHED = "attached"
VOLUME_STATE_DETACHED = "detached"

def wait_for_device_login(dest_path, name):
    dev = ""
    for _ in range(RETRY_COUNTS):
        for _ in range(RETRY_COMMAND_COUNT):
            files = []
            try:
                files = os.listdir(dest_path)
                break
            except Exception:
                time.sleep(1)
        assert files
        if name in files:
            dev = name
            break
        time.sleep(RETRY_INTERVAL)
    assert dev == name
    return dev


def wait_for_volume_creation(client, name):
    for _ in range(RETRY_COUNTS):
        volumes = client.list_volume()
        found = False
        for volume in volumes:
            if volume.name == name:
                found = True
                break
        if found:
            break
        time.sleep(RETRY_INTERVAL)
    assert found


def wait_for_volume_attached(client, name):
    return wait_for_volume_status(client, name,
                                  VOLUME_FIELD_STATE,
                                  VOLUME_STATE_ATTACHED)

def wait_for_volume_detached(client, name):
    return wait_for_volume_status(client, name,
                                  VOLUME_FIELD_STATE,
                                  VOLUME_STATE_DETACHED)

def wait_for_volume_status(client, name, key, value):
    wait_for_volume_creation(client, name)
    for _ in range(RETRY_COUNTS):
        volume = client.by_id_volume(name)
        if volume[key] == value:
            break
        time.sleep(RETRY_INTERVAL)
    assert volume[key] == value
    return volume


def wait_for_volume_delete(client, name):
    for _ in range(RETRY_COUNTS):
        volumes = client.list_volume()
        found = False
        for volume in volumes:
            if volume.name == name:
                found = True
                break
        if not found:
            break
        time.sleep(RETRY_INTERVAL)
    assert not found

