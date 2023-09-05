#pip3 install pywin32
#pip install discord
#pip install datetime
#pip install pywinauto
#pip install application
#pip install asyncio
#pip install berconpy
#$ pip install auto-py-to-exe
#auto-py-to-exe

import configparser
import discord
import datetime
from discord.ext import commands, tasks
from pywinauto import application
import random
import configparser
config = configparser.ConfigParser()
config.read( 'bot_discord_arma.ini')
main_window = config.get('Settings', 'main_window')
token = config.get('Settings', 'token')
app = config.get('Settings', 'app')
# Выводим полученные значения
print(f"main_window: {main_window}")
print(f"app: {app}")



def arma_concole_text():
    # Подключаемся к процессу приложения
    global app
    app = application.Application().connect(path="arma3server_x64.exe")
    main_window2 = app.top_window()
    print(main_window2)
    print(main_window2.print_control_identifiers())
    # Получите основное окно приложения
    
    #global main_window
    main_window = app.window(title = main_window )
    
    # Найдите элемент по классу и получите его текст
    element = main_window.child_window(class_name='RichEdit20A') #RichEdit20A
    text = element.text_block()

    #очистка поля
    element.set_edit_text('')
    return text
    # Выведите все доступные свойства элемента
    #properties = element.get_properties()
    #print(properties)


 # функцйия логирования всего    
def append_to_file(file_path, text):
    with open(file_path, 'a') as file:
        file.write(text)


 
        
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

@tasks.loop(seconds=30)
async def send_time():
    channel_id = 1134472382183133285
    channel = bot.get_channel(channel_id)
    text = arma_concole_text()
    if text!='':
        file_path = 'bot_log.txt'
        append_to_file(file_path, text)
        
        lines = text.split('\n')

        for line in lines:
            if line.find('connecting.') != -1:
                await channel.send( line)
                print('+ '+line)
            if line.find('disconnected.') != -1:
                await channel.send( line)
                print('+ '+line)
            if line.find('BattlEye Server: (Side) ') != -1:
                new_text = line
                new_text = new_text.replace('BattlEye Server: (Side) ', '' )
                words = new_text.split()
                if len(words) >= 2:
                    formatted_words = [words[0], f'**{words[1]}**', *words[2:]]
                    # Соединяем слова обратно в сообщение
                    new_text = ' '.join(formatted_words)
                
                emoji = '\U0001f575'
                # Формируем новое сообщение
                new_text = f'{emoji} {new_text}'
                await channel.send( new_text)
                print('+ '+line)

                
            if line.find('Game started.') != -1:
                current_time = datetime.datetime.now().strftime("%H:%M")
                await channel.send(f"Сервер запущен {current_time}")

@bot.event
async def on_ready():
    send_time.start()
    print(f'Discord авторизован {bot.user.name}')
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('ARMA 3'))
     
bot.run(token)

