from gdshechka import *
import flet as ft

NAME = 'GDYT'
CREATOR = 'N1C1N1'
DESCRIPTION = "Программа которая поможет оформить название и описание для шоукейса."
BGCOLOR = 'black'

level_info = None

def level_search(e):
    global level_info
    try:
        idField.disabled = True
        idField.update()
        try:
            int(idField.value)
            level_info = Level(int(idField.value))
        except:
            find = FindLevelByName(idField.value.strip()).FindResult
            level_info = Level(find[0]["id"])
        buttonsRow.controls.clear()
        for i in level_info.api:
            buttonsRow.controls.append(ft.TextButton(i, on_click=paste_value, animate_size=ft.Animation(500, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN)))
    except: ...
    idField.disabled = False
    idField.update()
    buttonsRow.update()
def change(e):
    try:
        if level_info != None:
            mainField.value = mainField.value.format(**level_info.api)
            mainField.error_text = None
    except:
        mainField.error_text = 'Неправельные аргументы'
    mainField.update()

def paste_value(e: ft.ControlEvent):
    mainField.value += f'{level_info.api[e.control.text]} '
    mainField.update()

idField = ft.TextField(
    on_submit=level_search, 
    hint_text='ID или название уровня',
    border=ft.InputBorder.UNDERLINE,
    animate_size=ft.Animation(400, ft.AnimationCurve.LINEAR_TO_EASE_OUT),
    filled=True,
    bgcolor=ft.colors.with_opacity(0.05, 'blue')
)
mainField = ft.TextField(
    multiline=True, 
    hint_text='Поле ввода', 
    on_change=change, 
    animate_size=ft.Animation(400, ft.AnimationCurve.LINEAR_TO_EASE_OUT), 
    min_lines=3,
    border_radius=4,
    content_padding=20,
    filled=True,
    bgcolor=ft.colors.with_opacity(0.05, 'blue'),
    border_width=0,
    focused_border_width=0
)

buttonsRow = ft.Row(
    animate_size=ft.Animation(500, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN),
    wrap=True
)

tooltip = ft.Tooltip(
    content=ft.Icon(ft.icons.HELP_OUTLINE_ROUNDED),
    message='Инфу об уровне можно вставить кнопкой\nили через "аргументы", аргументы это\nзаписи по типу {name} - где name\nназвание с кнопки.',
    bgcolor='white',
    text_style=ft.TextStyle(size=30, color='black')
)

CONTENT = [
    ft.Container(
        ft.Column([idField, mainField], alignment=ft.alignment.center, expand=True),
        gradient=ft.LinearGradient(['#242424', '#404040']),
        border_radius=15
    ),
    tooltip, 
    buttonsRow
]