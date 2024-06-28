# Longhorn Volume Manager

This helper is used by myself to manage Longhorn volumes.

It will create a longhorn volume if it does not exist, or restoring from the latest a backup if there are any.

The helper is written in Python and uses the Longhorn API to manage the volumes. It is meant to be run as a Kubernetes job within a Helm Chart.

## Convention

Volume, PVC and PVC names follow an opinionated convention:
```
{namespace}-{app_name}-{volume_name}
```

E.g: 
- `media-plex-config`
- `vaultwarden-vaultwarden-data`

## Usage

```bash
python src/main.py
```

## Configuration

The input variables are managed with environment variables.

| Variable             | Description                                      | Default                                |
| -------------------- | ------------------------------------------------ | -------------------------------------- |
| `NAMESPACE`          | The namespace of the Longhorn volume to create   |                                        |
| `APP_NAME`           | The app name of the Longhorn volume to create    |                                        |
| `VOLUME_NAME`        | The name of the Longhorn volume to create        |                                        |
| `VOLUME_SIZE`        | The size of the Longhorn volume to create        | `1Gi`                                  |
| `VOLUME_ACCESS_MODE` | The access mode of the Longhorn volume to create | `rwo`                                  |
| `LONGHORN_URL`       | The URL of the Longhorn instance                 | `http://longhorn-frontend.longhorn/v1` |

## Deployment

### Docker image

```bash
docker login
docker build -t longhorn-volume-manager-image .
docker tag longhorn-volume-manager-image:latest barthodev/longhorn-volume-manager-image:latest
docker tag longhorn-volume-manager-image:latest barthodev/longhorn-volume-manager-image:<version>
docker push barthodev/longhorn-volume-manager-image:latest
docker push barthodev/longhorn-volume-manager-image:<version>
```

### Helm Chart

```bash
cd chart
helm package .
docker login
helm push longhorn-volume-manager-0.1.0.tgz oci://registry-1.docker.io/barthodev
```

## Development

### Requirements

- Python 3.x
- PiP

### Setup

```bash
pip install -r requirements.txt
```

### Run

```bash
python src/main.py
```

## Credits

- [sekhrivijay/restore-longhorn-volume](https://github.com/sekhrivijay/restore-longhorn-volume/tree/master)
- [Longhorn documentation](https://longhorn.io/docs/1.6.2/references/longhorn-client-python/)