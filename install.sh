#!/usr/bin/env bash

mkdir memory
docker build -t entropy-bot . --network host
docker run --restart unless-stopped --name entropy-bot -v "$(pwd)":/memory --user $(id -u):$(id -g) entropy-bot
