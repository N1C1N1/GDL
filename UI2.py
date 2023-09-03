import flet as ft
from flet import icons
import requests, os, shutil, zipfile, json, sys
jsus = requests.get('https://raw.githubusercontent.com/N1C1N1/GDL/main/ext.json').json()
bsus = requests.get('https://raw.githubusercontent.com/N1C1N1/GDL/main/main.json').json()

try:
    with open('launcher.json', 'r') as f:
        CFG = json.loads(f.read())
except:
    with open('launcher.json', 'w', encoding='UTF-8') as f:
        json.dump({"path" : "", "theme" : "light", "lang" : "Русский"}, f, indent=4)
        CFG = {"path" : "", "theme" : "light", "lang" : "Русский"}
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

if CFG["theme"] == "dark":
    bgcolor = '#1A1C1E'
    invertcolor = 'white'
else:
    bgcolor = 'white'
    invertcolor = 'black'
lang = CFG["lang"]
buttonstyle = ft.ButtonStyle(shape={ft.MaterialState.HOVERED: ft.RoundedRectangleBorder(radius=10), ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=15)})
def main(page: ft.Page):
    page.title = 'GDL'
    page.window_width, page.window_height = 500, 600
    if CFG["theme"] != "dark":
        page.theme_mode = ft.ThemeMode.LIGHT
    else:
        page.theme_mode = ft.ThemeMode.DARK
    page.scroll = True

    page.fonts = {
        'Ubuntu' : 'https://raw.githubusercontent.com/google/fonts/master/ufl/ubuntu/Ubuntu-Regular.ttf'
    }

    page.window_title_bar_hidden = True

    tool_bar_title = ft.WindowDragArea(ft.Row([ft.Text('GDL', expand = True, font_family='Ubuntu', size = 30), ft.IconButton(style=buttonstyle, icon_size=30, icon_color=invertcolor, icon=icons.CLOSE, on_click=lambda _: page.window_close())]))

    def restart(e = 1):
        page.window_close()
        os.execl(sys.executable, sys.executable, *sys.argv)
    
    def wexit():
        page.window_close()
        exit()
    pls_restart_dlg = ft.AlertDialog(
        modal=True,
        title=ft.Text("Перезапустите программу!"),
        content=ft.Text("Для того что бы продолжить перезапустите программу"),
        on_dismiss=lambda _: restart(),
        actions=[ft.TextButton('Перезапустить', on_click=lambda _: restart())]
    )
    def dialog_restart_open(e = 1):
        page.dialog = pls_restart_dlg
        pls_restart_dlg.open = True
        page.update()

    class mods():
        def download_mod(self, name):
            url = jsus["mods"][name]["link"]
            
            self.button.icon = icons.DOWNLOADING_ROUNDED
            self.button.icon_color = 'blue'
            if lang == 'RU':
                self.button.tooltip = 'Загрузка'
            else:
                self.button.tooltip = 'Downloading'
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
            self.button.on_click = lambda _: self.deletemod(name = name)
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
            self.button.on_click = lambda _: self.download_mod(name = name)
            self.button.update()
        def __init__(self, name):
            self.main_text = ft.Text(name, expand=True, size = 30)
            if jsus["mods"][name]["files"] not in os.listdir(mod_install_path):
                self.button = ft.IconButton(icon=icons.DOWNLOAD, icon_color='green', on_click=lambda _: self.download_mod(name = name))
            else:
                self.button = ft.IconButton(icon=icons.DELETE, icon_color='red', on_click=lambda _: self.deletemod(name = name))

            if mod_install_path == GDpath:
                self.button.disabled = True
                self.button.icon_color = 'gray'
                self.button.tooltip = 'Install mod menu!'

            if lang == "RU":
                self.disc = ft.Text(jsus["mods"][name]["discription-ru"])
            else:
                self.disc = ft.Text(jsus["mods"][name]["discription-en"])
            self.disc.tooltip = 'file: ' + jsus["mods"][name]["files"] + '\ntype: ' + jsus["mods"][name]["type"]
            self.disc.size = 20
            tab_mods.append(ft.Row([self.main_text, self.button]))
            tab_mods.append(self.disc)
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
            self.button.on_click = lambda _: self.install_menu(name = name)
            self.button.update()
        def install_menu(self, name):
            self.button.icon = icons.DOWNLOADING_ROUNDED
            self.button.icon_color = 'blue'
            if lang == 'RU':
                self.button.tooltip = 'Загрузка'
            else:
                self.button.tooltip = 'Downloading'
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
            dialog_restart_open()
            self.button.icon = icons.DELETE
            self.button.on_click = lambda _: self.remove_menu(name = name)
            self.button.icon_color = 'red'
            self.button.tooltip = ''
            self.button.update()
        def __init__(self, name):
            self.main_label = ft.Text(name, size = 30, expand=True)
            self.button = ft.IconButton(icon = icons.DOWNLOAD, icon_color='green', on_click=lambda _: self.install_menu(name = name))
            if bsus["mod-menus"][name]["files"][0] in os.listdir(GDpath):
                self.button.icon = icons.DELETE
                self.button.on_click = lambda _: self.remove_menu(name = name)
                self.button.icon_color = 'red'
                self.button.tooltip = ''
            self.disc = ft.Text(bsus["mod-menus"][name]["disk-ru"])
            if lang == 'en':
                self.disc.value = bsus["mod-menus"][name]["disk-en"]

            self.screenshot = ft.Image(bsus["mod-menus"][name]["screenshot"], border_radius=10)
            tab_menu.append(ft.Row([self.main_label, self.button]))
            tab_menu.append(self.disc)
            tab_menu.append(self.screenshot)

    class TP():
        def delete_tp(self, name):
            shutil.rmtree(packs_path + '\\' + name)
            self.button.icon = icons.DOWNLOAD
            self.button.icon_color = 'green'
            self.button.on_click = lambda _: self.download_tp(name = name)
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
            self.button.on_click = lambda _: self.delete_tp(name = name)
            self.button.update()
        def __init__(self, name) -> None:
            self.main_text = ft.Text(name, size = 30, expand = True)
            self.screenshot = ft.Image(bsus["tp"][name]["screenshot"], border_radius=10)
            self.button = ft.IconButton(icon = icons.DOWNLOAD, icon_color='green', on_click = lambda _: self.download_tp(name = name))
            if packs_path != False:
                if name in os.listdir(packs_path):
                    self.button.icon = icons.DELETE
                    self.button.icon_color = 'red'
                    self.button.on_click = lambda _: self.delete_tp(name = name)
            else:
                self.button.icon_color = 'gray'
                self.button.disabled = True
                self.button.tooltip = 'TextureLDR not installed'
            tab_tp.append(ft.Row([self.main_text, self.button]))
            tab_tp.append(self.screenshot)

    tab_menu, tab_mods, tab_tp = [], [], []

    if CFG["path"] == "":
        start_tab = 3
    else:
        start_tab = 0

    if GDpath != "":
        for i in jsus["mods"].keys():
            mods(i)
        for i in bsus["mod-menus"].keys():
            modmenu(i)
        for i in bsus["tp"].keys():
            TP(i)

    def write_in_cfg(cfg, value):
        CFG[cfg] = value
        with open('launcher.json', 'w', encoding='UTF-8') as f:
            json.dump(CFG, f, indent=4)

    class settings:
        def save(e):
            if theme_select.value == '0':
                write_in_cfg("theme", "light")
            elif theme_select.value == '1':
                write_in_cfg("theme", "dark")

            if lang_select.value == '0':
                write_in_cfg("lang", "RU")
            elif theme_select.value == '1':
                write_in_cfg("lang", "EN")

            dialog_restart_open()
        def gd_direct_pick_save(e: ft.FilePickerResultEvent):
            global path_saved
            path_field.value = e.path
            if 'GeometryDash.exe' in os.listdir(e.path):
                path_field.border_color = 'black'
                path_field.label = 'Расположение ГД'
                path_field.label_style = ft.TextStyle(color = 'black')

                path_saved = e.path
                write_in_cfg("path", path_saved)
            else:
                path_field.border_color = 'red'
                path_field.label = 'В данной папке нет ГД!'
                path_field.label_style = ft.TextStyle(color = 'red')

                path_saved = ""
            page.update()
    gd_direct_pick = ft.FilePicker(on_result=settings.gd_direct_pick_save)
    page.overlay.append(gd_direct_pick)


    settings = [ft.Row([path_field := ft.TextField(label = 'Расположение ГД', hint_text='Путь к папке', expand=True, border_radius=10),
                path_select := ft.IconButton(icon=icons.FOLDER_ROUNDED, icon_color='blue', bgcolor=bgcolor, style = buttonstyle, on_click=lambda _: gd_direct_pick.get_directory_path('Папка с гд'))]),
                lang_select := ft.Dropdown(options=[ft.dropdown.Option(0, 'Русский'),
                                     ft.dropdown.Option(1, 'English')],
                            border_radius=10,
                            label='Язык',
                            value = CFG["lang"]),
                theme_select := ft.Dropdown(options=[ft.dropdown.Option(0, 'Светлая'),
                                     ft.dropdown.Option(1, 'Тёмная')],
                            border_radius=10,
                            label='Тема',
                            value=CFG["theme"]),
                ft.ElevatedButton('Применить', icon=icons.CHECK_ROUNDED, style=buttonstyle, bgcolor='blue', color = 'black', on_click=settings.save)]
    
    tabs_tabs = [
        ft.Tab(content=ft.Column(tab_menu), text='Менюшки', icon=icons.MENU_ROUNDED),
        ft.Tab(content=ft.Column(tab_mods), text='Моды', icon=icons.VIEW_MODULE_ROUNDED),
        ft.Tab(content=ft.Column(tab_tp), text='Текстур паки', icon=icons.IMAGE_ROUNDED),
        ft.Tab(content=ft.Column(settings), text = 'Настройки', icon=icons.SETTINGS)
    ]

    if GDpath == "":
        settings.append(ft.Text('Привет, для продолжения укажи путь к ГД и нажми применить!'))
        tabs_tabs = [ft.Tab(content=ft.Column(settings), text = 'Главная', icon=icons.SETTINGS)]
        start_tab = 0

    tabs = ft.Tabs(tabs=tabs_tabs, divider_color=bgcolor, indicator_color='blue', overlay_color=bgcolor, indicator_border_radius=50,
    indicator_padding=10, animation_duration=250, selected_index=start_tab)
    page.add(tool_bar_title, tabs)
ft.app(main)