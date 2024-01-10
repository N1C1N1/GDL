import requests, bs4
import zipfile, os, shutil

class ModTypes:
    MODMENU = 'modmenu'
    INSTALLER = 'installer'

class GithubModParser:
    def __init__(self, url: str, main_file: str = None):
        """
        Url must be https://github.com/maxnut/GDMegaOverlay/releases\n
        main_file is inserted automatically, but it takes time, so it is better to write it manually 'gdmo.zip'.\n

        Example:
        ```python 
        GDMOgithub = GithubModParser('https://github.com/maxnut/GDMegaOverlay/releases', 'gdmo.zip') 
        ```
        """
        response = requests.get(url + '/latest')
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        self.url = url
        self.last_link = str(soup.find_all('include-fragment')[3]).split('src="')[1].split('">')[0]
        if main_file == None:
            main_file = bs4.BeautifulSoup(requests.get(self.last_link).text, 'lxml').find(class_="Truncate-text text-bold").text
        self.main_file = main_file
        self.last_version = self.last_link.split(url + '/expanded_assets/')[1]
        self.download_link = f'{url}/download/{self.last_version}/{main_file}'
        logs = bs4.BeautifulSoup(requests.get(f'{url}/tag/{self.last_version}').text, 'lxml')
        self.logs = logs.find(class_="markdown-body my-3").text

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
        self.download_url = download_url
        self.download_file_name = download_file_name

    def Install(self):
        self.path_to_install = self.path
        if self.type == ModTypes.MODMENU:
            download = requests.get(self.github.download_link)

            with open(self.path + self.github.main_file, 'wb') as file:
                file.write(download.content)
            with zipfile.ZipFile(self.path + self.github.main_file) as zf:
                zf.extractall(self.path)
            os.remove(self.path + self.github.main_file)

        elif self.type == ModTypes.INSTALLER:
            download = requests.get(self.download_url)

            with open(self.path + self.download_file_name, 'wb') as file:
                file.write(download.content)

            self.files = self.path + self.download_file_name
            
    def Delete(self):
        for filename in self.files:
            if len(filename.split('.')) > 1:
                os.remove(self.path + filename)
            else:
                shutil.rmtree(self.path + filename)
    
def gdh_uninstall_fix(path: str):
        download = requests.get('https://github.com/N1C1N1/GDL/raw/main/files/libExtensions.dll')

        with open(path + '\\' + 'libExtensions.dll', 'wb') as file:
            file.write(download.content)