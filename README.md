# How to run the application

After you have downloaded the code create a .env file to the same folder as bot.py.
The file contents should look like this:

	TOKEN=your_token_here
	ENTROPY_INFO_CHAT_ID=your_chat_id_here

## With docker
First install docker.

Third do `docker build -t entropy-bot . --network host`

Then do `docker -d run --restart unless-stopped --name entropy-bot -v "$(pwd)":/memory --user "$(id -u)":"$(id -g)" entropy-bot`

OR

Install docker, run `chmod +x install.sh` in terminal and then run `install.sh` in terminal.

## Alternative way
First install requirements via terminal by typing:
`pip install -r requirements.txt`

Then you probably should type `screen -S entropy-bot` and `python bot.py`
