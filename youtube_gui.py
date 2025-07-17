import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import sys
from yt_dlp import YoutubeDL
import time

start_time = time.time()

def browse_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

def paste_from_clipboard():
    try:
        url = root.clipboard_get()
        url_entry.delete(0, tk.END)
        url_entry.insert(0, url)
    except tk.TclError:
        messagebox.showwarning("Буфер обмена", "Буфер обмена пуст или содержит недопустимые данные.")

def download():
    url = url_entry.get().strip()
    folder = folder_var.get().strip()
    quality = quality_var.get()

    if not url or not folder:
        messagebox.showerror("Ошибка", "Введите ссылку и выберите папку")
        return

    def run():
        try:
            download_button.config(state=tk.DISABLED)
            progress_bar.start()

            # Поддержка PyInstaller
            if getattr(sys, 'frozen', False):
                ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg.exe")
            else:
                ffmpeg_path = os.path.abspath("ffmpeg.exe")

            ydl_opts = {
                'format': f'bestvideo[height<={quality}]+bestaudio/best/best',
                'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'ffmpeg_location': ffmpeg_path,
                'progress_hooks': [hook],
                'noplaylist': True,
                # 'playlist_items': '1',  # Можно удалить эту строку
            }

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            progress_bar.stop()
            progress_bar['value'] = 100
            messagebox.showinfo("Успех", "Скачивание завершено")
        except Exception as e:
            progress_bar.stop()
            messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")
        finally:
            download_button.config(state=tk.NORMAL)
            progress_bar['value'] = 0

    threading.Thread(target=run).start()

def hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)
        speed = d.get('speed', 0)
        eta = d.get('eta', 0)

        if total_bytes:
            percent = downloaded_bytes / total_bytes * 100
            mb_downloaded = downloaded_bytes / 1024 / 1024
            mb_total = total_bytes / 1024 / 1024
            speed_mbps = speed / 1024 / 1024 if speed else 0
            time_left = time.strftime("%M:%S", time.gmtime(eta)) if eta else "--:--"

            def update_gui():
                progress_bar['value'] = percent
                progress_label.config(
                    text=f"Загружено: {percent:.1f}% ({mb_downloaded:.1f} из {mb_total:.1f} МБ)\n"
                         f"Скорость: {speed_mbps:.2f} МБ/c | Осталось: {time_left}"
                )
            root.after(0, update_gui)
    elif d['status'] == 'finished':
        def finish_gui():
            progress_bar['value'] = 100
            progress_label.config(text="Загрузка завершена")
        root.after(0, finish_gui)

def show_about():
    messagebox.showinfo("О программе", "YouTube Downloader\nВерсия: 1.2\nСкачивайте видео с YouTube и радуйтесь жизни.")

# --- GUI ---
root = tk.Tk()
root.title("YouTube Downloader")
root.geometry("400x360")
root.resizable(False, False)

# --- Иконка ---
if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS
else:
    base_path = os.path.abspath(".")
icon_path = os.path.join(base_path, "youtubelogo.ico")
try:
    root.iconbitmap(icon_path)
except:
    pass

# --- Меню ---
menubar = tk.Menu(root)
menubar.add_command(label="О программе", command=show_about)
root.config(menu=menubar)

# --- Ввод ссылки ---
tk.Label(root, text="Ссылка на видео:").pack(pady=(10, 0))
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Кнопка вставки из буфера
tk.Button(root, text="Вставить из буфера", command=paste_from_clipboard).pack(pady=(0, 5))

# --- Папка сохранения ---
folder_var = tk.StringVar()
tk.Label(root, text="Папка для сохранения:").pack()
frame = tk.Frame(root)
tk.Entry(frame, textvariable=folder_var, width=35).pack(side=tk.LEFT, padx=(0, 5))
tk.Button(frame, text="Обзор", command=browse_folder).pack(side=tk.LEFT)
frame.pack(pady=5)

# --- Качество ---
quality_var = tk.StringVar(value="1080")
tk.Label(root, text="Максимальное качество:").pack()
tk.OptionMenu(root, quality_var, "720", "1080", "1440", "2160").pack(pady=5)

# --- Прогресс ---
progress_label = tk.Label(root, text="Ожидание...")
progress_label.pack()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress_bar.pack(pady=(5, 5))

# --- Кнопка скачивания ---
download_button = tk.Button(root, text="Скачать", command=download, bg="#5f5f5f", fg="white", padx=20)
download_button.pack(pady=5)

root.mainloop()
