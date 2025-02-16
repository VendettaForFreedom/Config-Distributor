# Running TeleTweet Bot with Docker

This guide explains how to run the TeleTweet bot using Docker.

## Prerequisites

1. Docker installed on your system
2. Docker Compose installed
3. Your Telegram and Twitter credentials ready

## Quick Start

1. Clone the repository:

```bash
git clone https://github.com/yourusername/teletweet.git
cd teletweet
```

2. Create and configure .env file:

```bash
cp .env.example .env
nano .env  # Or use your preferred editor
```

3. Build and start the container:

```bash
docker-compose up -d
```

4. Check the logs:

```bash
docker-compose logs -f
```

## Directory Structure

```
.
├── data/              # Persistent data (created by Docker)
├── teletweet/         # Bot source code
├── .env               # Environment configuration
├── Dockerfile
└── docker-compose.yml
```

## Configuration

### Environment Variables

All environment variables are read from the `.env` file. This file is mounted into the container, so you can update it without rebuilding.

### Data Persistence

The following directories are persisted:

- `./data`: Application data
- `./teletweet`: Bot source code
- `./.env`: Configuration file

## Management Commands

### Start the bot:

```bash
docker-compose up -d
```

### Stop the bot:

```bash
docker-compose down
```

### View logs:

```bash
docker-compose logs -f
```

### Restart the bot:

```bash
docker-compose restart
```

### Update the bot:

```bash
git pull
docker-compose build
docker-compose up -d
```

## Health Checks

The container includes a health check that verifies the bot's connection to Telegram every 5 minutes. You can check the status with:

```bash
docker ps
```

Look for the `STATUS` column - it should show `healthy`.

## Troubleshooting

### Common Issues

1. Container keeps restarting:

   - Check logs: `docker-compose logs -f`
   - Verify your .env configuration
   - Ensure network connectivity

2. Permission issues:

   - Check volume permissions
   - Ensure the data directory is writable

3. Network issues:
   - Verify your internet connection
   - Check if Telegram is accessible

### Debug Mode

To enable debug logging:

1. Add to your .env file:

```
DEBUG=1
```

2. Restart the container:

```bash
docker-compose restart
```

## Maintenance

### Log Rotation

Logs are automatically rotated with:

- Maximum size: 10MB
- Keep last 3 files

### Updates

To update the bot:

1. Pull latest changes:

```bash
git pull
```

2. Rebuild and restart:

```bash
docker-compose build
docker-compose up -d
```

### Backup

To backup your data:

1. Stop the container:

```bash
docker-compose down
```

2. Copy data directory:

```bash
cp -r data/ backup/
cp .env backup/
```

3. Restart the container:

```bash
docker-compose up -d
```

## Security Considerations

1. Environment Variables:

   - Never commit .env file
   - Use strong credentials
   - Regularly rotate secrets

2. Volume Permissions:

   - Set appropriate ownership
   - Restrict access to data directory

3. Network Security:
   - Use container isolation
   - Monitor network access
   - Keep Docker updated

## Support

If you encounter issues:

1. Check the logs
2. Review configuration
3. Search existing issues
4. Create new issue with:
   - Logs
   - Configuration (without secrets)
   - Steps to reproduce
