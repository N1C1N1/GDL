import flet as ft
from pytube import YouTube
import os

NAME = 'NONG'
CREATOR = 'N1C1N1'
DESCRIPTION = "Программа для установки нонг музыки с утубчика."
BGCOLOR = 'black'

def searchUrl():
    global song
    urlField.disabled = True
    urlField.update()
    if urlField.value.find('youtu') >= 0:
        yt = YouTube(urlField.value)
        song = yt.streams.filter(only_audio=True).first()
        saveID.value = song.title
    elif urlField.value.find('mp3') >= 0 or urlField.value.find('wav') >= 0:
        song = urlField.value
        saveID.value = song.split("\\")[len(song.split("\\")) - 1].split('.')[0]
    else:
        urlField.clean()
    
    urlField.disabled = False
    saveID.visible = True
    
    
    saveID.update()
    urlField.update()

def saveSong(e):
    if urlField.value.find('youtu') >= 0:
        song.download(output_path='.', filename=f'{saveID.value}.mp3')
        print(os.system(f'move {saveID.value}.mp3 %localappdata%\\GeometryDash\\{saveID.value}.mp3'))
    else:
        if song.find('C:\\') >= 0 or song.find('D:\\') >= 0:
            print(f'move "{song}" %localappdata%\\GeometryDash\\{saveID.value}.mp3')
            print(os.system(f'move "{song}" %localappdata%\\GeometryDash\\{saveID.value}.mp3'))

urlField = ft.TextField(
    border=ft.InputBorder.UNDERLINE,
    animate_size=ft.Animation(400, ft.AnimationCurve.LINEAR_TO_EASE_OUT),
    filled=True,
    hint_text='Youtube URL или путь',
    on_submit=lambda _: searchUrl()
)

saveID = ft.TextField(
    animate_size=ft.Animation(400, ft.AnimationCurve.LINEAR_TO_EASE_OUT),
    filled=True,
    hint_text='song id',
    visible=False,
    on_submit=saveSong
)

CONTENT = [urlField, saveID]