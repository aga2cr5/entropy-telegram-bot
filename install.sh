#!/usr/bin/env bash

mkdir memory
docker build -t entropy-bot . --network host
docker run --restart unless-stopped --name entropy-bot -v "$(pwd)":/memory --user 1000:1000 entropy-bot
