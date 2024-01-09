import flet as ft
import mods
from translate import Translator

class MenuItem():
    def __init__(self, name: str, icon: ft.icons, on_click = None):
        def on_hover(e):
            self.c.bgcolor = 'None' if self.c.bgcolor not in ['None', None] else 'white'
            self.c.update()

        self.c = ft.Container(
            content=ft.Column(
                [ft.Icon(icon, size=70), ft.Text(name, size=40)], alignment='center', horizontal_alignment='center'
            ),
            border_radius=4,
            border=ft.border.all(4, 'white'),
            width=250,
            height=250,
            alignment=ft.alignment.center,
            on_hover=on_hover,
            blur=40,
            animate=ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_CUBIC),
            on_click=on_click
        )
class news():
    def __init__(self, title, description, url, image_url, data):
        self.name = ft.Text(title, size=20)
        self.disc = ft.Text(description + '\n\n' + data, size=15)
        image_url = image_url if list(image_url)[0] != '/' else 'https://www.dashword.net' + image_url
        self.image = ft.Image(image_url, expand=True, border_radius=10)
        self.link = url

        def news_translate(e):
            if self.translate.value:
                self.translate.disabled = True
                self.translate.update()
                self.name.value =Translator('RU').translate(title)
                self.disc.value = Translator('RU').translate(description) + '\n\n' + data
                self.translate.disabled = False
            else:
                self.name.value = title
                self.disc.value = description + '\n\n' + data
            self.container.update()
        self.translate = ft.Checkbox(label='Перевести', on_change=news_translate)
        self.container = ft.Container(
            ft.Column([self.image, self.name, self.disc, self.translate], alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER), 
            border_radius=10,
            blur=100,
            height=400, width=600,
            border=ft.border.all(4, '#0a0a0a'),
            bgcolor='#0f0f0f'
        )