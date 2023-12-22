# README

### Start containers
```sh
docker compose up -d
```

### View healthcheck logs
```sh
docker compose logs healthcheck --follow
```

### Optional: Open second terminal and view mock services logs
```sh
docker compose logs mock-first mock-second --follow
```

### Cleanup
```sh
docker compose down -v
```
