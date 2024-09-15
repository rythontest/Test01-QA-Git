from github import Github
from dotenv import load_dotenv
import os

# Загрузка переменных
load_dotenv()

GH_TOKEN = os.getenv("GH_TOKEN")
GH_USERNAME = os.getenv("GH_USERNAME")
REPO_NAME = os.getenv("REPO_NAME")

#print(GH_TOKEN, GH_USERNAME, REPO_NAME)

class GhTest:
    def __init__(self, token):
        self.token = token
        self.gh = None
        self.user = None
        # Авторизация пользователя на GitHub
        try:
            self.gh = Github(token)
            self.user = self.gh.get_user()
            print('Успешная авторизация на GitHub')
        except:
            print('Ошибка авторизации на GitHub')

    def close_connect(self):
        '''
        Закрытие соединения
        '''
        if self.gh != None:
            self.gh.close()

    def repo_create(self, repo_name: str, description='Next test repo'):
        '''
        Создание публичного репозитория
        '''
        if self.user != None:
            try:
                self.user.create_repo(repo_name, description, private=False)
                print(f'Успешное создание репозитория: {repo_name}')
            except:
                print(f'Ошибка создания репозитория: {repo_name}')

    def repo_list(self):
        """
        Получение списка репозиториев
        """
        if self.user != None:
            rez = []
            try:
                rez = [rp.name for rp in list(self.user.get_repos())]
            except:
                print('Ошибка получения списка репозиториев')
            return rez

    def repo_delete(self, repo_name: str):
        """
        Удаление репозитория
        """
        if self.user != None:
            try:
                repo = self.user.get_repo(repo_name)
                repo.delete()
                print(f'Успешное удаление репозитория: {repo_name}')
            except:
                print('Ошибка удаления репозитория')


if __name__ == "__main__":
    # Подключение к GitHub
    gh = GhTest(GH_TOKEN)

    # Создание репозитория
    gh.repo_create(REPO_NAME)

    # Загрузка списка репозиториев и проверка наличия созданного репозитория
    if REPO_NAME in gh.repo_list():
        print(f"Успешная проверка наличия репозитория: {REPO_NAME}")
    else:
        print(f"Репозитория {REPO_NAME} нет в списке.")

    # Удаление репозитория
    gh.repo_delete(REPO_NAME)

    # Закрытие соединения
    gh.close_connect()