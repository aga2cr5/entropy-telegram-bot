#!/usr/bin/local python3

import telegram
import asyncio
from time import sleep
import aioschedule as schedule
import requests
from bs4 import BeautifulSoup
from datetime import date
from dotenv import load_dotenv
import os


load_dotenv()

TOKEN = os.getenv("TOKEN")
ENTROPY_INFO_CHAT_ID = os.getenv("ENTROPY_INFO_CHAT_ID")
BASE_URL = "https://entropy.fi/"
event_list = []


class Event:
    def __init__(self, name, date, url) -> None:
        self.name = name
        self.date = date
        self.url = url
    
    def get_all_info(self):
        info = self.name + " - " + self.date + "\n" + self.url
        return info
    
    def get_small_info(self):
        info = self.name + " - " + self.date
        return info


bot = telegram.Bot(TOKEN)


async def get_events():
    response = requests.get(BASE_URL + "tapahtumat")
    soup = BeautifulSoup(response.content, "html.parser")
    events = soup.find(id="events").find_all("div")
    for div in events:
        # nämä voisi varmaan jotenkin filtteröidä ja ottaa sitten vain uusimman tapahtuman
        # eikä käsitellä muita ollenkaan
        if str(date.today().year - 1) not in div.text:
            if "post" in str(div):
                info = list(filter(lambda value: len(value) > 1, div.text.replace("\n", "").strip(" ").split("  "))) #tässä on splitissä kaksi välilyöntiä
                event_name = info[0]
                event_date = info[1]
                event_url = str(div.find("a")["href"])
                found = False

                # tällä hetkellä taitaa luoda ns turhia olioita,
                # mutta hoitaakohan pythonin carbage collector ne pois?
                for event in event_list:
                    if event.name == event_name:
                        found = True
                if found == False:
                    event_list.append(Event(event_name, event_date, BASE_URL + event_url))
        else:
            break
    message = event_list[0]
    event_list.clear()
    return message


def set_last_event(event) -> None:
    with open("last_posted_event.txt", 'r+') as file:
        data = file.readlines()
        if data != event:
            file.seek(0)
            file.write(event)
            file.truncate()
            print("Tiedosto päivitetty")
    return


def get_last_event():
    try:
        with open("last_posted_event.txt", 'r') as file:
            data = file.readlines()
            if len(data) > 0:
                return data[0]
            return None
    except FileNotFoundError:
        print("Kyseistä tiedostoa ei löydy hakemistosta.\nLuodaan tiedosto tapahtumien tallentamista varten\n")
        with open("last_posted_event.txt", 'w') as file:
            print("Uusi tiedosto luotu tapahtumien tallentamista varten.\n")
        return None


async def send_message_entropy() -> None:
    new_event = await get_events()
    new_event_info = new_event.get_small_info()
    message = new_event.get_all_info()
    last_event = get_last_event()
    if new_event_info == last_event or new_event_info is None:
        return
    async with bot:
        await bot.send_message(chat_id=ENTROPY_INFO_CHAT_ID, text=message)
    print(f"Lähetetty seuraava viesti tiedotuskanavalle:\n{message}\n")
    set_last_event(new_event_info)
    return


def main():
    schedule.every(10).seconds.do(send_message_entropy)
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(schedule.run_pending())
            sleep(5)
        except KeyboardInterrupt:
            print("\nLopetetaan ohjelma")
            exit()


if __name__ == "__main__":
    main()