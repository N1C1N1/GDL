import requests, bs4
import zipfile, os, shutil

class ModTypes:
    MODMENU = 'modmenu'
    INSTALLER = 'installer'
    ZIP_MODNENU = 'zip_modmenu'

class GithubModParser:
    def __init__(self, url: str, file_len: int = 0):
        """
        Url must be https://api.github.com/repos/prevter/gdopenhack/releases/latest\n

        Example:
        ```python 
        GDMOgithub = GithubModParser('https://api.github.com/repos/prevter/gdopenhack/releases/latest') 
        ```
        """
        github_latest = requests.get(url).json()
        self.last_version = github_latest["tag_name"]
        self.download_link = github_latest["assets"][file_len]["browser_download_url"]
        self.file_name = github_latest["assets"][file_len]["name"]

class ModFile:
    def __init__(self, path: str = '', files: list = [], type: ModTypes = ModTypes.MODMENU, github: GithubModParser = None, download_url: str = None, download_file_name: str = None):
        """Mod for geometry dash\n
        Example:
        ```python
        GDMOgithub = GithubModParser('https://github.com/maxnut/GDMegaOverlay/releases', 'gdmo.zip')

        gdmo = ModFile(
            path = 'test\\',
            files = ['GDMO', 'GDMO.dll', 'minhook.x32.dll', 'xinput9_1_0.dll'],
            github=GDMOgithub
        )
        ```
        """
        self.path = path
        self.files = files
        self.type = type
        self.github = github
        self.download_url = download_url if self.github == None else self.github.download_link
        self.download_file_name = download_file_name if self.github == None else self.github.file_name

    def Install(self):
        self.path_to_install = self.path
        if self.type == ModTypes.MODMENU:
            download = requests.get(self.github.download_link)

            with open(self.path + self.github.file_name, 'wb') as file:
                file.write(download.content)
            with zipfile.ZipFile(self.path + self.github.file_name) as zf:
                zf.extractall(self.path)
            os.remove(self.path + self.github.file_name)

        elif self.type == ModTypes.INSTALLER:
            download = requests.get(self.download_url)

            with open(self.path + self.download_file_name, 'wb') as file:
                file.write(download.content)        
    def Delete(self):
        for filename in self.files:
            if len(filename.split('.')) > 1:
                os.remove(self.path + filename)
            else:
                shutil.rmtree(self.path + filename)
    
    def Run(self):
        os.startfile(self.path + self.github.file_name)
    
def gdh_uninstall_fix(path: str):
        download = requests.get('https://github.com/N1C1N1/GDL/raw/main/files/libExtensions.dll')

        with open(path + '\\' + 'libExtensions.dll', 'wb') as file:
            file.write(download.content)