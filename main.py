import flet as ft
from gdl_controls import *
import webbrowser, bs4, requests, os
import mods
__version__ = 2.15

def get_github_version():
    git = requests.get('https://api.github.com/repos/N1C1N1/GDL/releases/latest').json()
    return [float(git["name"]), git["body"]]

get_github = get_github_version()
def main(page: ft.Page):
    page.title = 'GDL'
    page.fonts = {
        'rubik': 'https://github.com/google/fonts/raw/main/ofl/rubik/Rubik%5Bwght%5D.ttf'
    }
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary='white',
            secondary='white'
        ),
        font_family='rubik'
    )
    page.window_height, page.window_width = 650, 600
    news_row = ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)
    if page.client_storage.get('check_updates') == '':
        page.client_storage.set('check_updates', True)
    class dev:
        def __init__(self, name, key):
            self.row = ft.Row([ft.Text(name, size=30, selectable=True), ft.Text('', expand=True), ft.Text(key, size=30, selectable=True)], alignment=ft.alignment.center)

    dev_info = ft.Column(
        [
            dev('Версия', __version__).row,
            dev('Расположение игры', page.client_storage.get('gd_path')).row,
            dev('Обновления', page.client_storage.get('check_updates')).row
        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.alignment.center, scroll=ft.ScrollMode.ADAPTIVE
    )

    class ModItem:
        def __init__(self, 
                     github: mods.GithubModParser = None, 
                     files: list = None, 
                     name: str = None, 
                     description: str = None, 
                     screen: str = None, 
                     type: mods.ModTypes = mods.ModTypes.MODMENU, 
                     download_url = None, 
                     download_file_name = None):
            
            def mod_route(e):
                self.container.border = ft.border.all(4, '#0a0a0a')
                def get(e):
                    mainButton.disabled = True
                    page.update()
                    page.client_storage.set(name + 'v', self.modfile.last_version)
                    try: 
                        self.modfile.Install()
                        page.snack_bar = ft.SnackBar(ft.Text(f'{name} успешно установлен', color='green'), duration=500, bgcolor='black')
                        page.snack_bar.open = True
                    except: page.go('/settings')
                    mainButton.disabled = False

                    page.update()
                    check()

                def delete(e):
                    mainButton.disabled = True
                    page.update()
                    try:
                        if list(page.client_storage.get('gd_path'))[len(list(page.client_storage.get('gd_path'))) - 1] != '\\':
                            page.client_storage.set('gd_path', page.client_storage.get('gd_path') + '\\')
                        self.modfile.Delete()
                        if name in ['GDH', 'gd hacks']: mods.gdh_uninstall_fix(page.client_storage.get('gd_path'))
                        page.snack_bar = ft.SnackBar(ft.Text(f'{name} успешно удалён', color='green'), duration=500, bgcolor='black')
                        page.snack_bar.open = True
                    except Exception as e:
                        page.snack_bar = ft.SnackBar(ft.Text(f'Неизвестная ошибка:\n{e}', color='red'), duration=2000, bgcolor='black')
                        page.snack_bar.open = True
                    
                    mainButton.disabled = False
                    check()
                
                def update(e):
                    mainButton.disabled = True
                    page.update()
                    self.modfile.Delete()
                    self.modfile.Install()
                    page.client_storage.set(name + 'v', self.modfile.last_version)
                    mainButton.disabled = False
                    check()

                mainButton = ft.TextButton('Скачать', on_click=get)
                start_button = ft.TextButton('Запустить', on_click=lambda _: self.modfile.Run())
                start_button.visible = False
                def check():
                    if page.client_storage.get('gd_path') == '':
                        mainButton.on_click = lambda _: page.go('/settings')
                    else:
                        if self.modfile.files[0] in os.listdir(str(page.client_storage.get('gd_path'))):
                            if self.modfile.last_version != str(page.client_storage.get(name + 'v')) and page.client_storage.get(name + 'v') != None:
                                mainButton.text = 'Обновить'
                                mainButton.on_click = update
                            if self.modfile.type == mods.ModTypes.INSTALLER:
                                start_button.visible = True
                            mainButton.text = 'Удалить'
                            mainButton.on_click = delete
                        else:
                            start_button.visible = False
                            mainButton.text = 'Скачать'
                            mainButton.on_click = get
                    page.update()
                
                check()
                page.views.clear()
                page.views.append(ft.View(
                    '/mods/' + name,
                    controls=[
                        ft.Row([
                            ft.Text(name, size=30, expand=True, tooltip=self.modfile.last_version),
                            start_button,
                            mainButton]),
                        ft.Text(description, size=20),
                        ft.Image(screen, border_radius=5, expand=True), 
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/'))
                    ],
                    bgcolor='black',
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ))
                page.update()

            column = ft.Column([
                ft.Image(screen, expand=True, border_radius=5),
                ft.Text(name, size=30),
            ], alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            def container_hover(e):
                self.container.border = ft.border.all(6, 'white') if self.container.border == ft.border.all(4, '#0a0a0a') else ft.border.all(4, '#0a0a0a')
                page.update()

            self.container = ft.Container(
                column,
                height=300,
                on_click=mod_route,
                border=ft.border.all(4, '#0a0a0a'),
                bgcolor='#0f0f0f',
                blur=40,
                animate=ft.animation.Animation(100, ft.AnimationCurve.EASE_IN_CUBIC),
                on_hover=container_hover,
                width=350,
                border_radius=5,
                padding=10
            )

            try:
                self.github = github
                self.modfile = mods.ModFile(
                    path=str(page.client_storage.get('gd_path')),
                    files=files,
                    type=type,
                    github=self.github,
                    download_url=download_url,
                    download_file_name=download_file_name
                )
            except:
                return None
            self.modfile.path_to_install = str(page.client_storage.get('gd_path'))
            dev_info.controls.append(dev(name, page.client_storage.get(name + 'v')).row) # set info to dev
            page.update()
        def add(self):
            mods_row.controls.append(self.container)
            page.update()

    mods_row = ft.Row(wrap=True, alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER)

    def change_banner(type: bool):
        dialogUpdate.open = type
        page.update()

    dialogUpdate = ft.AlertDialog(
        title=ft.Text('Обновление!'),
        modal=True,
        actions=[
            ft.TextButton('Скачать', on_click=lambda _: webbrowser.open('https://github.com/N1C1N1/GDL/releases/latest')),
            ft.TextButton('Закрыть', on_click=lambda _: change_banner(False))
        ],
        content=ft.Markdown()
    )
    gdPathField = ft.TextField(label='Путь к ГД', on_change=lambda _: page.client_storage.set('gd_path', str(gdPathField.value)), value=page.client_storage.get("gd_path"))

    page.dialog = dialogUpdate
    def route(e):
        page.views.clear()
        page.views.append(
            ft.View(
                '/',
                [
                    ft.Container(ft.Row([MenuItem('Новости', ft.icons.NEWSPAPER_ROUNDED, on_click=lambda _: page.go('/news')).c,
                    MenuItem('Моды', ft.icons.MODE_EDIT_ROUNDED, on_click=lambda _: page.go('/mods')).c,
                    MenuItem('Настройки', ft.icons.SETTINGS, on_click=lambda _: page.go('/settings')).c,
                    MenuItem('инфо', ft.icons.INFO_ROUNDED, on_click=lambda _: page.go('/info')).c], wrap=True),
                    alignment=ft.alignment.center, expand = True, gradient=ft.LinearGradient(['red', 'yellow']), border_radius=4)
                 ],
                 bgcolor='black'
            )
        )
        if page.route == '/info':
            page.views.append(
                ft.View(
                    '/info',
                    [
                        ft.Container(ft.Image('https://avatars.githubusercontent.com/u/116889092', border_radius=7, width=200, height=200), on_click=lambda _: page.go('/dev_info')),
                        ft.Text('GDL2', size=30),
                        ft.Container(ft.Text('By N1C1', color='blue'), on_click=lambda _: webbrowser.open('https://github.com/N1C1N1')),
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/'))
                    ],
                    bgcolor='black',
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        if page.route == '/dev_info':
            page.views.append(
                ft.View(
                    '/dev_info',
                    [
                        ft.Text('Информация для разработчика'),
                        dev_info,
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/info'))
                    ],
                    bgcolor='black',
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        if page.route == '/news':
            page.views.append(
                ft.View(
                    '/news',
                    [
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/')),
                        news_row
                    ],
                    bgcolor='black',
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS
                )
            )
        if page.route == '/settings':
            page.views.append(
                ft.View(
                    '/settings',
                    [
                        gdPathField,
                        ft.Divider(),
                        t_updates := ft.CupertinoSwitch(label='Проверять на обновления', on_change=lambda _: page.client_storage.set('check_updates', t_updates.value), value=page.client_storage.get('check_updates')),
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/'))
                    ],
                    bgcolor='black',
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS
                )
            )
        if page.route == '/mods':
            page.views.append(
                ft.View(
                    '/mods',
                    [
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/')),
                        mods_row
                    ],
                    bgcolor='black',
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS
                )
            )
        page.update()

    page.on_route_change = route
    page.go(page.route)

    ModItem(
        mods.GithubModParser('https://api.github.com/repos/TobyAdd/GDH/releases/latest'),
        ['GDH', 'gdh.dll', 'libExtensions.dll', 'libExtensions.dll.bak'],
        'GDH',
        'Мод-меню с обширным функционалом, имеется бот.',
        'https://cdn.discordapp.com/attachments/1186919727046610984/1191015890502819930/image.png'
    ).add()
    ModItem(
        mods.GithubModParser('https://api.github.com/repos/maxnut/GDMegaOverlay/releases/latest'),
        ['GDMO', 'GDMO.dll', 'minhook.x32.dll', 'xinput9_1_0.dll'],
        'GDMO',
        'Имеется бот, множество функций, интерфейс похож на megahack.',
        'https://github.com/maxnut/GDMegaOverlay/raw/2.2/img/screen.jpg'
    ).add()
    ModItem(
        mods.GithubModParser('https://api.github.com/repos/prevter/gdopenhack/releases/latest'),
        ['openhack', 'xinput9_1_0.dll'],
        'OpenHack',
        'Очень красивый интерфейс, но мало функций.',
        'https://github.com/Prevter/GDOpenHack/raw/main/docs/screenshot.png'
    ).add()
    ModItem(
        mods.GithubModParser('https://api.github.com/repos/qwix456/gd-hacks/releases/latest'),
        ['gd-hacks.dll', 'libExtensions.dll'],
        'GD Hacks',
        'Микро мод меню, есть лайаут мод.',
        'https://cdn.discordapp.com/attachments/1190628273210794024/1196770601432518747/296799623-06e91fad-2663-4e42-9b08-f696a329455d.png',
        mods.ModTypes.GD_HACKS
    ).add()
    ModItem(
        mods.GithubModParser('https://api.github.com/repos/zeozeozeo/zcb3/releases/latest', 2),
        ['zcb3.exe'],
        'ZCB',
        'Лучший клик бот.',
        'https://github.com/zeozeozeo/zcb3/raw/master/screenshots/1.png',
        mods.ModTypes.INSTALLER
    ).add()
    ModItem(
        files=['yBot Installer.exe'],
        name='Ybot (free)',
        description='Есть бесплатная версия но без возможности записи макросов.',
        screen='https://cdn.discordapp.com/attachments/1136895151776747620/1189178561442095194/image.png',
        type=mods.ModTypes.INSTALLER,
        download_url='https://ybot.store/files/yBot%20Installer.exe',
        download_file_name='yBot Installer.exe'
    ).add()

    #getting news
    for row_news in bs4.BeautifulSoup(requests.get('https://www.dashword.net/').text, 'lxml').find_all(class_="post cols"):
        news_row.controls.append(news(
            str(row_news.find(class_="title").text).strip(), 
            str(row_news.find(class_="desc").text).strip(), 
            'https://www.dashword.net/' + str(row_news.find(class_="title")).split('href="')[1].split('" style="')[0], 
            str(row_news.find('img')).split('" src="')[1].split('"/>')[0], 
            str(row_news.find(class_="date").text).strip()
        ).container)
        page.update()

    #checking updates
    if page.client_storage.get('check_updates') == True:
        if __version__ != get_github[0]:
            dialogUpdate.content.value = get_github[1]
            change_banner(True)
ft.app(main)