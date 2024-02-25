# DeployModel

The awesome DeployModel

## Uploading a new boost version
```bash
docker build . -t boost:0.0.0 -f Dockerfile.pre
```

```bash
docker push boost:0.0.0
```