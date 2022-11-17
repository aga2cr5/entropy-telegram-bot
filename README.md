# How to run the application

After you have downloaded the code create a .env file to the same folder as bot.py.
The file contents should look like this:

	TOKEN=your_token_here
	ENTROPY_INFO_CHAT_ID=your_chat_id_here

## With docker
First do `docker build -t entropy-bot . network host`

Then do `docker run -d --restart unless-stopped --name --volume ./:/ entropy-bot`

## Alternative way
First install requirements via terminal by typing:
`pip install -r requirements.txt`

Then you probably should type `screen -S entropy-bot` and `python bot.py`
