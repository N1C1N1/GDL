import flet as ft
from flet import icons
import requests, os, shutil, zipfile, json, sys, webbrowser
from bs4 import BeautifulSoup
from translate import Translator

bsus = requests.get('https://raw.githubusercontent.com/N1C1N1/GDL/main/main.json').json()
__verison__ = 1.0

try:
    with open('launcher.json', 'r') as f:
        CFG = json.loads(f.read())
except:
    with open('launcher.json', 'w', encoding='UTF-8') as f:
        json.dump({"path": "", "theme": "light", "lang": "RU"}, f, indent=4)
        CFG = {"path": "", "theme": "light", "lang": "RU"}
GDpath = CFG["path"]

if GDpath != "":
    if "packs" in os.listdir(GDpath):
        packs_path = GDpath + '\\packs'
    else:
        packs_path = False

    if "GDMenu" in os.listdir(GDpath):
        mod = 'GDMO'
        mod_install_path = GDpath + '\\GDMenu\\dll'
    elif "extensions" in os.listdir(GDpath):
        mod = 'Mega Hack'
        mod_install_path = GDpath + '\\extensions'
    elif ".GDHM" in os.listdir(GDpath):
        mod = 'GDHM'
        mod_install_path = GDpath + '\\.GDHM\\dll'
    else:
        mod_install_path = GDpath

bgcolor = '#1A1C1E' if CFG["theme"] == "dark" else 'white'
smoth_color = '#272b2e' if CFG["theme"] == "dark" else '#ebebeb'
invertcolor = 'white' if CFG["theme"] == "dark" else 'black'
tlang = CFG["lang"]

help_link = 'https://sites.google.com/view/n1c1n1/gdl-gd-launcher/help-ru' if tlang == 'RU' else 'https://sites.google.com/view/n1c1n1/gdl-gd-launcher/help-en'

class translates:
    global tlang
    restartapp = 'Перезапустите программу' if tlang == 'RU' else 'Restart app'
    restartappdesc = 'Для того что бы продолжить перезапустите программу' if tlang == 'RU' else 'To continue restart the program'
    restart = 'Перезапустить' if tlang == 'RU' else 'Restart'
    download = 'Скачать' if tlang == 'RU' else 'Dowload'
    loading = 'Загрузка' if tlang == 'RU' else 'Loading'
    downloadmoodmenu = 'Скачайте мод меню!' if tlang == 'RU' else 'Download the mod menu first!'
    textureldrerror = 'Сначало установите textureLDR!' if tlang == 'RU' else 'Install textureLDR first!'
    gdpath = 'Расположение ГД' if tlang == 'RU' else 'Location of the GD'
    gdpatherror = 'В данной папке нет ГД!' if tlang == 'RU' else 'There is no GD in this folder!'
    pathway = 'Путь к папке' if tlang == 'RU' else 'Folder path'
    applytext = 'Применить' if tlang == 'RU' else 'Apply'
    darktheme = 'Тёмная' if tlang == 'RU' else 'Dark'
    lighttheme = 'Светлая' if tlang == 'RU' else 'Light'
    theme = 'Тема' if tlang == 'RU' else 'Theme'
    menus = 'Менюшки' if tlang == 'RU' else 'Menus'
    mods = 'Моды' if tlang == 'RU' else 'Mods'
    TP = 'Текстур паки' if tlang == 'RU' else 'Texture packs'
    settings = 'Насройки' if tlang == 'RU' else 'Settings'
    main = 'Главная' if tlang == 'RU' else 'Main'
    lang = 'Язык' if tlang == 'RU' else 'language'
    welcome = 'Привет, для продолжения укажи путь к ГД и нажми применить!' if tlang == 'RU' else 'Hi, to continue, specify the path to the GD and click apply!'
    screenshot = 'Скрин' if tlang == 'RU' else 'Screenshot'
    popupbutton = 'Открыть меню' if tlang == 'RU' else 'Open menu'
    help = 'Помощь' if tlang == 'RU' else 'Help'
    appdata = 'Аппдата' if tlang == 'RU' else 'Appdata'
    versiontext = f'Установленная версия: {__verison__} / {bsus["version"]}' if tlang == 'RU' else f'Installed version: {__verison__} / {bsus["version"]}'
    news = 'Новости' if tlang == 'RU' else 'News'
    mods_all = 'Все' if tlang == 'RU' else 'All'
    mods_mod = 'Моды' if tlang == 'RU' else 'Mods'
    mods_bot = 'Боты' if tlang == 'RU' else 'Bots'
    mods_clickbot = 'Клик боты' if tlang == 'RU' else 'Click bots'
    mods_bypass = 'Байпасы' if tlang == 'RU' else 'Bypasses'
    lists = 'Листы' if tlang == 'RU' else 'Lists'
    list_main = 'Поинтер' if tlang == 'RU' else 'Pointer'
    list_challenges = 'Челендж' if tlang == 'RU' else 'Challenge'


buttonstyle = ft.ButtonStyle(shape={ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=10),
                                    ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=15)})


def main(page: ft.Page):
    page.title = 'GDL'
    page.window_width, page.window_height = 500, 600
    page.theme_mode = ft.ThemeMode.LIGHT if CFG["theme"] != "dark" else ft.ThemeMode.DARK
    page.scroll = True

    page.fonts = {
        'Ubuntu': 'https://raw.githubusercontent.com/google/fonts/master/ufl/ubuntu/Ubuntu-Regular.ttf',
        'Lato-Regular': "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Regular.ttf",
        'Lato-Bold': "https://github.com/google/fonts/raw/main/ofl/lato/Lato-Bold.ttf"
    }
    page.window_title_bar_hidden = True
    page.theme = ft.Theme(font_family="Lato-Regular", use_material3=True)
    tool_bar_title = ft.WindowDragArea(ft.Row([ft.Text('GDL', expand=True, font_family='Ubuntu', size=30),
                                               status_label := ft.Text('', size = 15),
                                               ft.PopupMenuButton(items=[
                                                   ft.PopupMenuItem(text=translates.gdpath,
                                                                    on_click=lambda _: os.startfile(GDpath),
                                                                    icon=icons.FOLDER_ROUNDED),
                                                   ft.PopupMenuItem(text=translates.appdata,
                                                                    on_click=lambda _: os.system(
                                                                        'start C:\\Users\\%username%\\AppData\\Local\\GeometryDash'),
                                                                    icon=icons.FOLDER_SHARED_ROUNDED),
                                                   ft.PopupMenuItem(icon=icons.HELP_OUTLINE_OUTLINED,
                                                                    text=translates.help,
                                                                    on_click=lambda _: webbrowser.open(help_link))
                                               ], tooltip=translates.popupbutton),
                                               ft.IconButton(icon_size=30, icon_color=invertcolor, icon=icons.CLOSE,
                                                             on_click=lambda _: page.window_close())]))
    def status_label_update(new_text: str) -> None:
        status_label.value = new_text
        status_label.update()

    def restart(e=1):
        page.window_close()
        os.execl(sys.executable, sys.executable, *sys.argv)

    pls_restart_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text(translates.restartapp),
        content=ft.Text(translates.restartappdesc),
        on_dismiss=lambda _: restart(),
        actions=[ft.TextButton(translates.restart, on_click=lambda _: restart())]
    )

    def dialog_restart_open(e=1):
        page.dialog = pls_restart_dlg
        pls_restart_dlg.open = True
        page.update()

    class mods():
        def download_mod(self, name):
            url = jsus["mods"][name]["link"]

            self.button.icon = icons.DOWNLOADING_ROUNDED
            self.button.icon_color = 'blue'
            self.button.update()

            response = requests.get(url, stream=True)
            file_size = int(response.headers['Content-Length'])
            file_path = os.path.join(mod_install_path, jsus["mods"][name]["files"])

            with open(file_path, 'wb') as fd:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)
                    downloaded += len(chunk)
                    self.button.tooltip = f'{downloaded / file_size:.2f}%'
                    self.button.update()
            if name == 'textureLDR':
                os.mkdir(GDpath + "\\packs")
                dialog_restart_open()
            self.button.icon = icons.DELETE
            self.button.on_click = lambda _: self.deletemod(name=name)
            self.button.icon_color = 'red'
            self.button.tooltip = ''
            self.button.update()

        def deletemod(self, name):
            os.remove(mod_install_path + '\\' + jsus["mods"][name]["files"])

            if name == 'textureLDR':
                shutil.rmtree(GDpath + "\\packs")
                dialog_restart_open()
            self.button.icon = icons.DOWNLOAD
            self.button.icon_color = 'green'
            self.button.on_click = lambda _: self.download_mod(name=name)
            self.button.update()

        def __init__(self, name):
            self.main_text = ft.Text(name, expand=True, size=30, font_family='Lato-Bold')

            self.button = ft.IconButton(icon=icons.DOWNLOAD, icon_color='green',
                                        on_click=lambda _: self.download_mod(name=name)) if jsus["mods"][name][
                                                                                                "files"] not in os.listdir(
                mod_install_path) else ft.IconButton(icon=icons.DELETE, icon_color='red',
                                                     on_click=lambda _: self.deletemod(name=name))

            if mod_install_path == GDpath:
                self.button.disabled = True
                self.button.icon_color = 'gray'
                self.button.tooltip = translates.downloadmoodmenu

            self.disc = ft.Text(jsus["mods"][name]["discription-ru"]) if tlang == 'RU' else ft.Text(
                jsus["mods"][name]["discription-en"])

            self.disc.tooltip = 'file: ' + jsus["mods"][name]["files"] + '\ntype: ' + jsus["mods"][name]["type"]
            self.disc.size = 20
            self.result = ft.Container(ft.Column([ft.Row([self.main_text, self.button]), self.disc]), border_radius=5,
                                       gradient=ft.LinearGradient(['blue', 'purple'], begin=ft.alignment.bottom_left,
                                                                  end=ft.alignment.top_right)) if jsus["mods"][name][
                                                                                                      "img"] == "" else ft.Container(
                ft.Column([ft.Image(jsus["mods"][name]["img"], tooltip=translates.screenshot, border_radius=0),
                           ft.Row([self.main_text, self.button]), self.disc]), border_radius=5,
                gradient=ft.LinearGradient(['blue', 'purple'], begin=ft.alignment.bottom_left,
                                           end=ft.alignment.top_right))
            mod_all.append(self.result)
            if jsus["mods"][name]["type"] == 'mod':
                mod_mod.append(self.result)
            elif jsus["mods"][name]["type"] == 'bot':
                mod_bot.append(self.result)
            elif jsus["mods"][name]["type"] == 'click bot':
                mod_clickbot.append(self.result)
            elif jsus["mods"][name]["type"] == 'bypass':
                mod_bypass.append(self.result)

    class modmenu():
        def remove_menu(self, name):
            for i in bsus["mod-menus"][name]["files"]:
                os.remove(GDpath + '\\' + i)
                self.button.tooltip = i
                self.button.update()
            for i in bsus["mod-menus"][name]["paths"]:
                shutil.rmtree(GDpath + '\\' + i)
                self.button.tooltip = i
                self.button.update()
            mod_install_path = GDpath
            dialog_restart_open()
            self.button.icon = icons.DOWNLOAD
            self.button.icon_color = 'green'
            self.button.on_click = lambda _: self.install_menu(name=name)
            self.button.update()

        def install_menu(self, name):
            self.button.icon = icons.DOWNLOADING_ROUNDED
            self.button.icon_color = 'blue'
            self.button.tooltip = translates.download
            self.button.update()

            url = bsus["mod-menus"][name]["link"]
            response = requests.get(url, stream=True)
            file_size = int(response.headers['Content-Length'])
            file_path = os.path.join(GDpath, name + '.zip')

            with open(file_path, 'wb') as fd:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)
                    downloaded += len(chunk)
                    self.button.tooltip = f'{downloaded / file_size:.2f}%'
                    self.button.update()
            with zipfile.ZipFile(GDpath + '\\' + name + '.zip') as zf:
                zf.extractall(GDpath)
            os.remove(GDpath + '\\' + name + '.zip')

            if name == "GDMO":
                os.mkdir(GDpath + '\\GDMenu\\dll')

            dialog_restart_open()
            self.button.icon = icons.DELETE
            self.button.on_click = lambda _: self.remove_menu(name=name)
            self.button.icon_color = 'red'
            self.button.tooltip = ''
            self.button.update()

        def __init__(self, name):
            self.main_label = ft.Text(name, size=30, expand=True)
            self.button = ft.IconButton(icon=icons.DOWNLOAD, icon_color='green',
                                        on_click=lambda _: self.install_menu(name=name))
            if bsus["mod-menus"][name]["files"][0] in os.listdir(GDpath):
                self.button.icon = icons.DELETE
                self.button.on_click = lambda _: self.remove_menu(name=name)
                self.button.icon_color = 'red'
                self.button.tooltip = ''
            self.disc = ft.Text(bsus["mod-menus"][name]["disk-ru"])
            if tlang == 'EN':
                self.disc.value = bsus["mod-menus"][name]["disk-en"]
            self.screenshot = ft.Image(bsus["mod-menus"][name]["screenshot"], border_radius=10,
                                       tooltip=translates.screenshot)
            self.container = ft.Container(ft.Column([self.screenshot,
                                                     ft.Row([self.main_label, self.button]),
                                                     self.disc]), border_radius=5, gradient=ft.LinearGradient(['blue', 'purple']))
            mod_menus.append(self.container)
            mod_all.append(self.container)

    class TP():
        def delete_tp(self, name):
            shutil.rmtree(packs_path + '\\' + name)
            self.button.icon = icons.DOWNLOAD
            self.button.icon_color = 'green'
            self.button.on_click = lambda _: self.download_tp(name=name)
            self.button.update()

        def download_tp(self, name):
            url = bsus["tp"][name]["link"]
            response = requests.get(url, stream=True)
            file_size = int(response.headers['Content-Length'])
            file_path = os.path.join(packs_path, packs_path + '\\' + name + '.zip')

            self.button.icon = icons.DOWNLOADING
            self.button.icon_color = 'blue'
            with open(file_path, 'wb') as fd:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=1024):
                    fd.write(chunk)
                    downloaded += len(chunk)
                    self.button.tooltip = f'{downloaded / file_size:.2f}%'
                    self.button.update()
            with zipfile.ZipFile(packs_path + '\\' + name + '.zip') as zf:
                zf.extractall(packs_path)
            os.remove(packs_path + '\\' + name + '.zip')
            self.button.icon = icons.DELETE
            self.button.icon_color = 'red'
            self.button.on_click = lambda _: self.delete_tp(name=name)
            self.button.update()

        def __init__(self, name) -> None:
            self.main_text = ft.Text(name, size=30, expand=True)
            self.screenshot = ft.Image(bsus["tp"][name]["screenshot"], tooltip=translates.screenshot)
            self.button = ft.IconButton(icon=icons.DOWNLOAD, icon_color='green',
                                        on_click=lambda _: self.download_tp(name=name))
            if packs_path != False:
                if name in os.listdir(packs_path):
                    self.button.icon = icons.DELETE
                    self.button.icon_color = 'red'
                    self.button.on_click = lambda _: self.delete_tp(name=name)
            else:
                self.button.icon_color = 'gray'
                self.button.disabled = True
                self.button.tooltip = translates.textureldrerror
            self.result = ft.Container(ft.Column([
                ft.Row([self.main_text, self.button]),
                self.screenshot
            ]), gradient=ft.LinearGradient(['blue', 'purple']), border_radius=5)
            mod_tp.append(self.result)
            mod_all.append(self.result)

    tab_mods = ft.Tabs(tabs=[ft.Tab(translates.mods_all, content=ft.Column(mod_all := [])),
                             ft.Tab(translates.menus, content=ft.Column(mod_menus := [])),
                             ft.Tab(translates.mods_mod, content=ft.Column(mod_mod := [])),
                             ft.Tab(translates.mods_bot, content=ft.Column(mod_bot := [])),
                             ft.Tab(translates.mods_clickbot, content=ft.Column(mod_clickbot := [])),
                             ft.Tab(translates.mods_bypass, content=ft.Column(mod_bypass := [])),
                             ft.Tab(translates.TP, content=ft.Column(mod_tp := []))],
                             divider_color=bgcolor, indicator_color='blue', overlay_color=bgcolor,
                             indicator_border_radius=50, indicator_padding=10, animation_duration=250)

    start_tab = 3 if CFG["path"] == "" else 0

    def write_in_cfg(cfg, value):
        CFG[cfg] = value
        with open('launcher.json', 'w', encoding='UTF-8') as f:
            json.dump(CFG, f, indent=4)

    class settings:
        def save(e):
            write_in_cfg("theme", "light") if theme_select.value == '0' else write_in_cfg("theme", "dark")
            write_in_cfg("lang", "RU") if lang_select.value == '0' else write_in_cfg("lang", "EN")

            dialog_restart_open()

        def gd_direct_pick_save(e: ft.FilePickerResultEvent):
            global path_saved
            path_field.value = e.path
            if 'GeometryDash.exe' in os.listdir(e.path):
                path_field.border_color = 'black'
                path_field.label = translates.gdpath
                path_field.label_style = ft.TextStyle(color='black')

                path_saved = e.path
                write_in_cfg("path", path_saved)
            else:
                path_field.border_color = 'red'
                path_field.label = translates.gdpatherror
                path_field.label_style = ft.TextStyle(color='red')

                path_saved = ""
            path_field.update()

    gd_direct_pick = ft.FilePicker(on_result=settings.gd_direct_pick_save)
    page.overlay.append(gd_direct_pick)

    settings = [ft.Row([
        path_field := ft.TextField(label=translates.gdpath, hint_text=translates.pathway, expand=True, border_radius=10,
                                   border_width=0),
        ft.IconButton(icon=icons.FOLDER_ROUNDED, icon_color='blue', bgcolor=bgcolor,
                      on_click=lambda _: gd_direct_pick.get_directory_path(translates.gdpath))
            ]),
        lang_select := ft.Dropdown(options=[ft.dropdown.Option(0, 'Русский'), ft.dropdown.Option(1, 'English')],
                                   border_radius=10, label=translates.lang, value=CFG["lang"], border_width=0),
        theme_select := ft.Dropdown(
            options=[ft.dropdown.Option(0, translates.lighttheme), ft.dropdown.Option(1, translates.darktheme)],
            border_radius=10, label=translates.theme, value=CFG["theme"], border_width=0),
        ft.ElevatedButton(translates.applytext, icon=icons.CHECK_ROUNDED, bgcolor='blue', color='black',
                          on_click=settings.save),
        ft.Text(translates.versiontext)
    ]

    class news():
        def __init__(self, title, description, url, image_url, data):
            global tlang
            self.name = ft.Text(title, size=20)
            self.disc = ft.Text(description + '\n\n' + data, size=15)
            self.image = ft.Container(ft.Image(image_url, border_radius=0), on_click=lambda _: webbrowser.open(self.link))
            self.link = url

            def news_translate(e):
                if self.translate.value:
                    self.translate.disabled = True
                    self.translate.update()
                    self.name.value = Translator('RU').translate(title)
                    self.disc.value = Translator('RU').translate(description) + '\n\n' + data
                    self.translate.disabled = False
                else:
                    self.name.value = title
                    self.disc.value = description + '\n\n' + data
                page.update()
            self.translate = ft.Checkbox(label='Перевести', on_change=news_translate) if tlang == 'RU' else ft.Text()
            self.container = ft.Container(ft.Column([self.image, self.name, self.disc, self.translate]), border_radius=10,
                                          gradient=ft.LinearGradient(['blue', 'orange'], begin=ft.alignment.bottom_left,
                                                                     end=ft.alignment.top_right),
                                          shadow=ft.BoxShadow(1, 5, 'black'))

        def ParserNews():
            status_label_update(f'{translates.loading}: {translates.news}')
            news_page = requests.get('https://www.dashword.net/').text
            soup_page = BeautifulSoup(news_page, 'lxml')


            all_news = soup_page.find_all(class_="post cols")
            for new in all_news:
                tab_main.append(news(str(new.find(class_="title").text).strip(), str(new.find(class_="desc").text).strip(), 'https://www.dashword.net/' + str(new.find(class_="title")).split('href="')[1].split('" style="')[0], str(new.find('img')).split('" src="')[1].split('"/>')[0], str(new.find(class_="date").text).strip()).container)
                page.update()
    class TopLevel():
        def __init__(self, top: str, name: str, author: str, youtube: str, image: str):
            self.result = ft.Container(ft.Row([
                ft.Image(image, width=140, height=100, border_radius=10),
                ft.Column([
                    ft.Row([ft.Text(top.strip() + ' - ' + name.strip(), size=30)]),
                    ft.Row([ft.Text(author.strip(), size=25)])
                ])
            ]), shadow=ft.BoxShadow(1, 3, 'black'), bgcolor=smoth_color, border_radius=5, on_click=lambda _: webbrowser.open(youtube))

        def ParserMain():
            site = requests.get('https://pointercrate.com/demonlist/').text
            soup = BeautifulSoup(site, 'lxml')
            for i in soup.find_all(class_="panel fade"):
                lists_main.append(TopLevel(i.find('h2').text.split(' – ')[0].split('#')[1],
                                           i.find('h2').text.split(' – ')[1],
                                           i.find('i').text,
                                           str(i.find('a')).split('class="play" href="')[1].split('"></a>')[0],
                                           str(i.find(class_="thumb ratio-16-9 js-delay-css")).split("url('")[1].split(
                                               "')")[0]).result)
            lists_main.append(ft.Container(ft.Text('PointerCreate', size=30, color='blue'),
                                           on_click=lambda _: webbrowser.open('https://pointercrate.com/demonlist/')))
        def ParserChallenges():
            site = requests.get('https://challengelist.gd/challenges/').text
            soup = BeautifulSoup(site, 'lxml')
            for i in soup.find_all(class_="panel fade"):
                lists_chal.append(TopLevel(i.find('h2').text.split(' – ')[0].split('#')[1],
                                           i.find('h2').text.split(' – ')[1],
                                           i.find('i').text,
                                           str(i.find('a')).split('class="play" href="')[1].split('"></a>')[0],
                                           str(i.find(class_="thumb ratio-16-9 js-delay-css")).split("url('")[1].split(
                                               "')")[0]).result)
            lists_chal.append(ft.Container(ft.Text('The Challenge List', size=30, color='blue'),
                                           on_click=lambda _: webbrowser.open('https://challengelist.gd/challenges/')))
    tab_main = [ft.Row([ft.Text(translates.news, expand=True, size=40, text_align=ft.TextAlign.CENTER)])]
    tab_list = ft.Tabs(tabs=[
            ft.Tab(content=ft.Column(lists_main := []), text=translates.list_main),
            ft.Tab(content=ft.Column(lists_chal := []), text=translates.list_challenges)
        ], divider_color=bgcolor, indicator_color='blue', overlay_color=bgcolor, indicator_border_radius=50, indicator_padding=10, animation_duration=250)
    tabs_tabs = [
        ft.Tab(content=ft.Column(tab_main), text=translates.main, icon=icons.MENU_ROUNDED),
        ft.Tab(content=tab_mods, text=translates.mods, icon=icons.VIEW_MODULE_ROUNDED),
        ft.Tab(content=tab_list, text=translates.lists, icon=icons.ANALYTICS_ROUNDED),
        ft.Tab(content=ft.Column(settings), text=translates.settings, icon=icons.SETTINGS)
    ]

    if GDpath == "":
        settings.append(ft.Text(translates.welcome))
        tabs_tabs = [ft.Tab(content=ft.Column(settings), text=translates.main, icon=icons.SETTINGS)]
        start_tab = 0

    tabs = ft.Tabs(tabs=tabs_tabs, divider_color=bgcolor, indicator_color='blue', overlay_color=bgcolor,
                   indicator_border_radius=50,
                   indicator_padding=10, animation_duration=250, selected_index=start_tab)

    page.add(tool_bar_title, tabs)

    jsus = requests.get('https://raw.githubusercontent.com/N1C1N1/GDL/main/ext.json').json()
    news.ParserNews()
    if GDpath != "":
        status_label_update(f'{translates.loading}: {translates.menus}')
        for i in bsus["mod-menus"].keys():
            modmenu(i)
            page.update()
        status_label_update(f'{translates.loading}: {translates.mods_mod}')
        for i in jsus["mods"].keys():
            mods(i)
            page.update()
        status_label_update(f'{translates.loading}: {translates.TP}')
        for i in bsus["tp"].keys():
            TP(i)
            page.update()
    status_label_update(f'{translates.loading}: {translates.lists}')
    TopLevel.ParserMain()
    TopLevel.ParserChallenges()
    status_label_update('')
    page.update()
def new_programm_version(page: ft.Page):
    page.window_width, page.window_height = 300, 290
    page.title = 'Доступно обновление!' if tlang == 'RU' else 'Update available!'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll = False
    page.window_resizable = False
    page.add(ft.Text(f'Новая {bsus["version"]} версия доступна!' if tlang == 'RU' else f'New {bsus["version"]} version is avaiable!', size = 20, expand = True),
        ft.Row([ft.TextButton('Скачать' if tlang == 'RU' else 'Download', expand = True, on_click=lambda _: webbrowser.open('https://github.com/N1C1N1/GDL/releases'))])
    )

ft.app(main if __verison__ == float(bsus["version"]) else new_programm_version)
