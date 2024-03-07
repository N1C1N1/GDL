import flet as ft
from gdl_controls import *
import webbrowser, bs4, requests, os, mods, sys
from pypresence import Presence
from time import time
import iapps.conf as conf
from tokens import *

__version__ = 2.31

# Парсер последней версии гдл
def get_github_version():
    global githubStatus
    try:
        git = requests.get('https://api.github.com/repos/N1C1N1/GDL/releases/latest', headers=git_headers).json()
        githubStatus = True
        return [float(git["name"]), git["body"]]
    except:
        githubStatus = False
# Проверка на наличее перетащеных файлов
if len(sys.argv) <= 1:
    get_github = get_github_version()

colors = {
    "app_item_bgcolor": "black",
    "app_item_color": "#000000",
    "border_deafult": "#0a0a0a",
    "container_bgcolor": "#0f0f0f",
    "primary": "#ffffff",
    "secondary": "#ffffff",
    "view_bgcolor": "#000000"
}

def main(page: ft.Page):
    global githubStatus
    
    # Создаём РПС
    RPC = Presence(RPC_TOKEN)

    if page.client_storage.get('RPC') == None:
        page.client_storage.set('RPC', True)
    if page.client_storage.get('RPC'):
        RPC.connect()

    def discord_update(text: str, custom_button: dict = None):
        if page.client_storage.get('RPC'):
            try:
                RPC.update(
                    state=text,
                    start=time(),
                    large_image='https://i.imgur.com/GzsXAal.png',
                    buttons=custom_button
                )
            except: ...
    page.title = 'GDL'
    # Стилёк
    page.fonts = {
        'rubik': 'https://github.com/google/fonts/raw/main/ofl/rubik/Rubik%5Bwght%5D.ttf'
    }
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=colors['primary'],
            secondary=colors['secondary']
        ),
        font_family='rubik',
        page_transitions=ft.PageTransitionsTheme(
            windows=ft.PageTransitionTheme.CUPERTINO
        )
    )
    page.window_height, page.window_width = 650, 850
    page.theme_mode = ft.ThemeMode.DARK
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
            dev('Обновления', page.client_storage.get('check_updates')).row,
            dev('Discord RPC', page.client_storage.get('Discord RPC')).row,
            dev('githubstatus', githubStatus).row
        ], expand=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.alignment.center, scroll=ft.ScrollMode.ADAPTIVE
    )

    class ModItem:
        def __init__(self, 
                     github: mods.GithubModParser = None, 
                     files: list = None, 
                     name: str = None, 
                     description: str = None, 
                     screens: list = None, 
                     type: mods.ModTypes = mods.ModTypes.MODMENU, 
                     download_url = None, 
                     download_file_name = None):
            self.name = name
            def mod_route(e):
                discord_update(f'На странице {name}', [{'label': f'Скачать {name} через GDL', 'url': 'https://github.com/N1C1N1/GDL/releases/latest'}])
                self.container.border = ft.border.all(4, colors['border_deafult'])
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
                        if name in ['GDH', 'GD Hacks']: mods.gdh_uninstall_fix(page.client_storage.get('gd_path'))
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
                start_button = ft.TextButton('Запустить', icon=ft.icons.PLAY_ARROW_ROUNDED)

                def check():
                    if page.client_storage.get('gd_path') == '':
                        mainButton.on_click = lambda _: page.go('/settings')
                    else:
                        if self.modfile.files[0] in os.listdir(str(page.client_storage.get('gd_path'))):
                            if self.modfile.last_version != str(page.client_storage.get(name + 'v')) and page.client_storage.get(name + 'v') != None:
                                mainButton.text = 'Обновить'
                                mainButton.on_click = update
                                mainButton.icon = ft.icons.UPDATE_ROUNDED
                                start_button.visible = False
                            if self.modfile.type == mods.ModTypes.INSTALLER:
                                start_button.on_click=lambda _: self.modfile.Run()
                            else:
                                start_button.on_click=lambda _: webbrowser.open('steam://rungameid/322170')
                            
                            start_button.visible = True
                            mainButton.text = 'Удалить'
                            mainButton.on_click = delete
                            mainButton.icon = ft.icons.DELETE_ROUNDED
                        else:
                            start_button.visible = False
                            mainButton.text = 'Скачать'
                            mainButton.on_click = get
                            mainButton.icon = ft.icons.DOWNLOAD_ROUNDED
                    page.update()
                
                check()
                page.views.clear()

                if self.github != None:
                    githubInfo = ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem(content=ft.Text('Github'), on_click=lambda _: webbrowser.open(self.github.html_url))
                        ], tooltip='Открыть меню'
                    )
                    newButton = ft.TextButton('Что нового?', on_click=lambda _: opendlg(True))

                    newDialog = ft.AlertDialog(
                        content=ft.Column([ft.Markdown(self.github.body)], scroll=ft.ScrollMode.ADAPTIVE)
                    )
                else:
                    githubInfo = ft.canvas.Canvas()
                    newButton = ft.canvas.Canvas()

                def opendlg(e):
                    newDialog.open = e
                    page.dialog = newDialog
                    page.update()

                page.views.append(ft.View(
                    '/mods/' + name,
                    controls=[
                        ft.Row([
                            ft.Text(name, size=30, expand=True, tooltip=self.modfile.last_version),
                            start_button,
                            mainButton,
                            githubInfo
                            ]),
                        ft.Text(description, size=20),
                        newButton,             
                        ft.Row([
                            ft.Image(i, border_radius=20, width=600, height=600) for i in screens
                            ], scroll=ft.ScrollMode.ADAPTIVE, expand=True), 
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/'))
                    ],
                    bgcolor='black',
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ))
                page.update()

            column = ft.Column([
                ft.Image(screens[0], expand=True, border_radius=5),
                ft.Text(name, size=30),
            ], alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

            def container_hover(e):
                self.container.border = ft.border.all(6, 'white') if self.container.border == ft.border.all(4, colors['border_deafult']) else ft.border.all(4, colors['border_deafult'])
                page.update()

            self.container = ft.Container(
                column,
                height=300,
                border=ft.border.all(4, colors['border_deafult']),
                bgcolor=colors['container_bgcolor'],
                animate=ft.animation.Animation(100, ft.AnimationCurve.LINEAR),
                on_hover=container_hover,
                width=350,
                border_radius=5,
                padding=10,
                on_click=mod_route,
                blur=25
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

    class Iapps(ft.View):
        def __init__(self, app):
            super().__init__()
            
            self.app = app
            self.route = f'/apps/{app.NAME}'
            self.controls = [
                ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/')),
                ft.Column(app.CONTENT)
            ]
            self.bgcolor = app.BGCOLOR
            self.scroll = ft.ScrollMode.ADAPTIVE
    
    mods_row = ft.Row(
        wrap=True, 
        alignment=ft.MainAxisAlignment.CENTER, 
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        animate_size=ft.animation.Animation(300, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN)
    )

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
    
    gdPathField = ft.TextField(label='Путь к ГД', on_change=lambda _: page.client_storage.set('gd_path', str(gdPathField.value)), value=page.client_storage.get("gd_path"), expand=True, border_width=2)

    def gdPathOpenResult(e: ft.FilePickerResultEvent):
        gdPathField.value = e.path
        page.client_storage.set('gd_path', str(e.path))
        page.update()
    gdPathOpen = ft.FilePicker(on_result=gdPathOpenResult)
    page.overlay.append(gdPathOpen)

    page.dialog = dialogUpdate

    def searchmod(e):
        mods_row.controls.clear()
        if searchField.value.strip() == '':
            for i in ModsList:
                mods_row.controls.append(i.container)
                page.update()
        else:
            for i in ModsList:
                if i.name.lower().find(searchField.value) == 0:
                    mods_row.controls.append(i.container)
                    page.update()
    
    searchField = ft.TextField(label='Поиск', value = '', on_change=searchmod, border_width=3, border_radius=15, width=200, height=50)
    all_apps = [AppItem(i, page) for i in conf.APPS]
    all_apps.insert(0, ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/')))
    apps = [Iapps(i) for i in conf.APPS]
    
    def route(e):
        page.views.clear()
        page.views.append(
            ft.View(
                '/',
                [
                    ft.Container(ft.Row([
                            MenuItem('Новости', ft.icons.NEWSPAPER_ROUNDED, on_click=lambda _: page.go('/news')),
                            MenuItem('Моды', ft.icons.MODE_EDIT_ROUNDED, on_click=lambda _: page.go('/mods')),
                            MenuItem('Ультилиты', ft.icons.APPS_ROUNDED, on_click=lambda _: page.go('/apps')),
                            MenuItem('Настройки', ft.icons.SETTINGS, on_click=lambda _: page.go('/settings')),
                            MenuItem('инфо', ft.icons.INFO_ROUNDED, on_click=lambda _: page.go('/info'))
                        ], wrap=True, animate_size=ft.animation.Animation(300, ft.AnimationCurve.FAST_LINEAR_TO_SLOW_EASE_IN)),
                    alignment=ft.alignment.center, expand = True, gradient=ft.LinearGradient(['red', 'yellow']), border_radius=4)
                 ],
                 bgcolor=colors['view_bgcolor']
            )
        )
        discord_update('Главное меню')
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
                    bgcolor=colors['view_bgcolor'],
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
                    bgcolor=colors['view_bgcolor'],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        if page.route == '/news':
            discord_update('Смотрит новости')
            page.views.append(
                ft.View(
                    '/news',
                    [
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/')),
                        news_row
                    ],
                    bgcolor=colors['view_bgcolor'],
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
                        ft.Row([gdPathField, ft.IconButton(icon=ft.icons.FOLDER_OPEN_ROUNDED, on_click=lambda _: gdPathOpen.get_directory_path('Выберите расположение ГД'))]),
                        ft.Divider(),
                        t_updates := ft.CupertinoSwitch(label='Проверять на обновления', on_change=lambda _: page.client_storage.set('check_updates', t_updates.value), value=page.client_storage.get('check_updates')),
                        t_rpc := ft.CupertinoSwitch(label='Discord RPC', on_change=lambda _: page.client_storage.set('RPC', t_rpc.value), value=page.client_storage.get('RPC')),
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/'))
                    ],
                    bgcolor=colors['view_bgcolor'],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS
                )
            )
        if page.route == '/mods':
            discord_update('Разглядывает моды')
            page.views.append(
                ft.View(
                    '/mods',
                    [
                        ft.TextButton(icon=ft.icons.ARROW_BACK_IOS_NEW_ROUNDED, text = 'Вернуться', on_click=lambda _: page.go('/')),
                        searchField,
                        mods_row
                    ],
                    bgcolor=colors['view_bgcolor'],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    scroll=ft.ScrollMode.ALWAYS
                )
            )
        if page.route == '/apps':
            discord_update('Разглядывает приложения')
            
            page.views.append(ft.View(
                '/apps',
                all_apps,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                vertical_alignment=ft.MainAxisAlignment.CENTER,
                bgcolor=colors['view_bgcolor'],
                scroll=ft.ScrollMode.ADAPTIVE
                )
            )
        if page.route.find('/apps/') >= 0:
            for i in apps:
                if i.route == page.route:
                    discord_update(f'В {i.app.NAME}', custom_button=[{'label': f'Начать пользоваться {i.app.NAME}', 'url': 'https://github.com/N1C1N1/GDL/releases/latest'}])
                    page.views.append(i)
        page.update()

    page.on_route_change = route
    page.go('/')
    # try:
    ModsList = [
        ModItem(
            mods.GithubModParser('https://api.github.com/repos/TobyAdd/GDH/releases/latest'),
            ['GDH', 'gdh.dll', 'libExtensions.dll', 'libExtensions.dll.bak'],
            'GDH',
            'Мод-меню с обширным функционалом, имеется бот.',
            ['https://cdn.discordapp.com/attachments/1186919727046610984/1191015890502819930/image.png']
        ),
        ModItem(
            mods.GithubModParser('https://api.github.com/repos/maxnut/GDMegaOverlay/releases/latest'),
            ['GDMO', 'GDMO.dll', 'minhook.x32.dll', 'xinput9_1_0.dll'],
            'GDMO',
            'Имеется бот, множество функций, интерфейс похож на megahack.',
            ['https://github.com/maxnut/GDMegaOverlay/raw/2.2/img/screen.jpg']
        ),
        ModItem(
            mods.GithubModParser('https://api.github.com/repos/prevter/gdopenhack/releases/latest'),
            ['openhack', 'xinput9_1_0.dll'],
            'OpenHack',
            'Очень красивый интерфейс, но мало функций.',
            ['https://github.com/Prevter/GDOpenHack/raw/main/docs/screenshot.png']
        ),
        ModItem(
            mods.GithubModParser('https://api.github.com/repos/qwix456/gd-hacks/releases/latest'),
            ["GDHacks.dll", "libExtensions.dll", "libExtensions.dll.bak", "gdhacks"],
            'GD Hacks',
            'Мод меню, есть бот и лайаут мод.',
            ['https://i.imgur.com/rn1voq5.png'],
            mods.ModTypes.MODMENU
        ),
        ModItem(
            mods.GithubModParser('https://api.github.com/repos/zeozeozeo/zcb3/releases/latest', 2),
            ['zcb3.exe'],
            'ZCB',
            'Лучший клик бот.',
            ['https://github.com/zeozeozeo/zcb3/raw/master/screenshots/1.png'],
            mods.ModTypes.INSTALLER
        ),
        ModItem(
            github = mods.GithubModParser('https://api.github.com/repos/geode-sdk/geode/releases/latest', 3),
            files = ["GeodeUpdater.exe", "XInput9_1_0.dll", "Geode.dll", "Geode.lib", "Geode.pdb"],
            name = 'Geode',
            description = 'Загрузчик модов Geometry Dash.',
            screens=['https://geode-sdk.org/install.webp', 'https://geode-sdk.org/mods.webp'],
            type=mods.ModTypes.MODMENU
        ),
        ModItem(
            files=['yBot Installer.exe'],
            name='Ybot (free)',
            description='Есть бесплатная версия но без возможности записи макросов.',
            screens=['https://cdn.discordapp.com/attachments/1136895151776747620/1189178561442095194/image.png'],
            type=mods.ModTypes.INSTALLER,
            download_url='https://ybot.store/files/yBot%20Installer.exe',
            download_file_name='yBot Installer.exe'
        )
    ]
    # except Exception as ex:
    #     print(ex)
    #     ModsList = []
    #     githubStatus = False
    
    searchmod('N1C1 дауниха')

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
        if githubStatus:
            if __version__ != get_github[0]:
                dialogUpdate.content.value = get_github[1]
                change_banner(True)

def nongsong(page: ft.Page):
    page.title = 'GDL nong song'
    page.bgcolor = conf.nongsong.BGCOLOR
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40
    page.window_width, page.window_height = [500, 300]
    
    conf.nongsong.CONTENT[0].value = sys.argv[1]
    
    for i in conf.nongsong.CONTENT:
        page.add(i)

def mod_installer(page: ft.Page):
    page.title = 'GDL mod install'
    page.bgcolor = conf.nongsong.BGCOLOR
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 40
    page.window_width, page.window_height = [600, 400]
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(
        primary='white', secondary='white'
    ))
    filename = sys.argv[1].split('\\')[len(sys.argv[1].split('\\')) - 1]
    fileImage = ft.Image('https://geode-sdk.org/geode-logo-2.png', height=100, width=100)
    fileName = ft.Text(filename, size=20, weight=1)
    fileContainer = ft.Container(
        ft.Column([fileImage, fileName], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        bgcolor=colors['container_bgcolor'],
        border_radius=ft.BorderRadius(top_left=10, bottom_left=10, top_right=0, bottom_right=0),
        padding=30,
        height=200,
        ink=True,
        on_click=lambda _: ...
    )
    
    buttonStyle = ft.ButtonStyle(
        shape={ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=1)}
    )
    
    def install(e):
        os.system(f'move "{sys.argv[1]}" "{page.client_storage.get("gd_path")}geode\\mods\\{filename}"')
        page.window_close()
    
    mainText = ft.Text('Установка мода', size=25, weight=1)
    
    if 'geode' in os.listdir(page.client_storage.get("gd_path")) and filename.find('geode') >= 0:
        tooltip = 'Установите Geode!'
    
    installButton = ft.TextButton(
        'Установить мод', 
        icon=ft.icons.DOWNLOAD_ROUNDED, 
        icon_color='green', 
        style=buttonStyle,
        on_click=install,
        disabled=False if 'geode' in os.listdir(page.client_storage.get("gd_path")) else True,
        tooltip=None if 'geode' in os.listdir(page.client_storage.get("gd_path")) else 'У вас не установлен Geode!'
    )
    installClose = ft.TextButton(
        'Закрыть установку', 
        icon=ft.icons.CLOSE_ROUNDED, 
        icon_color=ft.colors.DEEP_PURPLE_ACCENT_400, 
        style=buttonStyle,
        on_click=lambda _: page.window_close()
    )
    
    installContainer = ft.Container(
        ft.Column([mainText, installButton, installClose], tight=True, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        alignment=ft.alignment.center,
        bgcolor=colors['container_bgcolor'],
        border_radius=ft.BorderRadius(top_left=0, bottom_left=0, top_right=10, bottom_right=10),
        padding=10,
        height=200
    )
    
    page.add(ft.Row([fileContainer, installContainer], tight=True))

if len(sys.argv) <= 1:
    ft.app(main)
else:
    if sys.argv[1].find('.geode') >= 0:
        ft.app(mod_installer)
    elif sys.argv[1].find('.mp3') >= 0 or sys.argv[1].find('.wav') >= 0:
        ft.app(nongsong)