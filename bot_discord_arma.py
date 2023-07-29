#pip3 install pywin32
#pip install discord
#pip install datetime
#pip install pywinauto
#pip install application
#pip install asyncio
#pip install berconpy
#$ pip install auto-py-to-exe
#$ auto-py-to-exe
import discord
import datetime
from discord.ext import commands, tasks
from pywinauto import application
import random
 
 

def arma_concole_text():
    # Подключаемся к процессу приложения
    app = application.Application().connect(path="arma3server.exe")
    
    # Получаем основное окно приложения
    #main_window = app.top_window()
    # Выводим информацию о окне
    #print(main_window)
    # Выводим информацию о всех элементах на окне
    #print(main_window.print_control_identifiers())
    # Получите основное окно приложения
    
    main_window = app.window(title='Arma 3 Console version 2.12.150301 x86 : port 2302')
    # Найдите элемент по классу и получите его текст
    element = main_window.child_window(class_name='RichEdit20A')
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

@tasks.loop(seconds=15)
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


bot.run('MTEzMzg1NjE5Mzg3NDUwMTgzMw.Gk2ID6.BpfdTYQCpBS9MEBJ2zRM2d5i9yEdwTCzbzd8Jg')
