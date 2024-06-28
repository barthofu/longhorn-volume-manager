def find_backup_volume(client, volume_name: str):
    backup_volumes = client.list_backupVolume().data
    for bv in backup_volumes:
        if bv.name == volume_name:
            return bv
    return None

def find_latest_backup(client, volume_name: str):
    backup_volume = find_backup_volume(client, volume_name)
    if backup_volume is not None:
        backups = backup_volume.backupList().data
        latest_backup = None
        for backup in backups:
            if latest_backup is None or backup.created > latest_backup.created:
                latest_backup = backup
        return latest_backup
    return None

def restore_volume_from_latest_backup(client, volume_name: str):
    backup = find_latest_backup(client, volume_name)
    if backup is not None:
        return client.create_volume(
            name = volume_name,
            accessMode = backup.labels['longhorn.io/volume-access-mode'],
            fromBackup = backup.url
        )
    return None
