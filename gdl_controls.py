import flet as ft
from translate import Translator
from iapps.conf import colors
from mods import *

class MenuItem(ft.Container):
    def __init__(self, name: str, icon: ft.icons, on_click = None):
        super().__init__()
        
        def on_hover(e):
            self.bgcolor = ft.colors.TRANSPARENT if self.bgcolor != ft.colors.TRANSPARENT else 'black'
            self.border = ft.border.all(8, 'white') if self.border == ft.border.all(4, 'white') else ft.border.all(4, 'white')
            self.update()


        self.content=ft.Column(
            [ft.Icon(icon, size=70), ft.Text(name, size=40)], alignment='center', horizontal_alignment='center'
        )
        self.border_radius=4
        self.border=ft.border.all(4, 'white')
        self.width=250
        self.height=250
        self.alignment=ft.alignment.center
        self.on_hover=on_hover
        self.blur=40
        self.animate=ft.animation.Animation(200, ft.AnimationCurve.LINEAR)
        self.animate_size=ft.Animation(400, ft.AnimationCurve.EASE_IN_TO_LINEAR)
        self.on_click=on_click
        self.bgcolor = ft.colors.TRANSPARENT

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
            height=500, width=500,
            border=ft.border.all(4, '#0a0a0a'),
            bgcolor='#0f0f0f'
        )

class AppItem(ft.Container):
    def __init__(self, app, page: ft.Page):
        super().__init__()
        
        def hover(e):
            self.padding = 10 if self.padding == 20 else 20
            self.content = ft.Text(app.NAME, size=50, color=colors['app_item_bgcolor']) if self.content == content else content
            self.bgcolor = 'blue' if self.bgcolor == colors['app_item_bgcolor'] else colors['app_item_bgcolor']
            self.border = ft.border.all(6, colors['app_item_bgcolor']) if self.border == None else None
            self.update()
        
        def click(e):
            self.padding = 10 if self.padding == 20 else 20
            self.content = ft.Text(app.NAME, size=50, color=colors['app_item_bgcolor']) if self.content == content else content
            self.bgcolor = 'blue' if self.bgcolor == colors['app_item_bgcolor'] else colors['app_item_bgcolor']
            self.border = ft.border.all(6, colors['app_item_bgcolor']) if self.border == None else None
            self.update()
            page.go(f'/apps/{app.NAME}')
        content = ft.Column([
            ft.Text(app.NAME, size=25, weight=1),
            ft.Text(app.DESCRIPTION, size=18, weight=1)
        ], expand=True)
        self.content = content
        self.animate_size = ft.Animation(400, ft.AnimationCurve.LINEAR)
        self.on_hover = hover
        self.bgcolor = colors['app_item_bgcolor']
        self.alignment = ft.alignment.center
        self.padding = 20
        self.animate = ft.Animation(400, ft.AnimationCurve.LINEAR)
        self.border_radius = 4
        self.width, self.height = [300, 300]
        self.on_click = click