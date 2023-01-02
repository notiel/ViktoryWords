import design
from dataclasses import dataclass, field
from PyQt5 import QtWidgets
import sys
from loguru import logger
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from typing import List
from random import randint

CREDENTIALS_FILE = 'token.json'

weak = 'алый белый лазурный пурпурный черный золотой серебряный изумрудный'

special = 'вихрь тигр луч рассвет закат ледяной река ярость'

extra = 'сила пламя феникс'

general = "журавль дракон цилинь черепаха танец порыв долг путь гора камень ветер вода небо тишина воздух сон шепот "


base = {'Гу': 'вихрь', 'Шань': "закат", "Хо": 'ледяной', 'РиО': "река", 'Хэ': 'ярость'}

east_sun = 'тигр в лучах рассвета'

titles = "abcdefghijklmnoprst"

# noinspection PyPep8Naming
@dataclass
class warrior:
    name: str
    wounds: int
    tech_num_weak: int
    tech_num: int
    tech_num_strong: int
    word_num: int
    base_tech: str
    death_words: List[str] = field(default_factory=list)
    technique: List[str] = field(default_factory=list)


# noinspection PyPep8Naming
@dataclass
class result:
    win1: int = 0
    death1: int = 0
    tired1: int = 0
    win2: int = 0
    death2: int = 0
    tired2: int = 0
    wounded1: int = 0
    wounded2: int = 0


def error_message(text: str):
    """
    shows error message with text
    :param text: text of error
    :return:
    """
    error = QtWidgets.QMessageBox()
    # noinspection PyUnresolvedReferences
    error.setIcon(QtWidgets.QMessageBox.Critical)
    error.setText(text)
    error.setWindowTitle('Error!')
    # noinspection PyUnresolvedReferences
    error.setStandardButtons(QtWidgets.QMessageBox.Ok)
    error.exec_()


def get_figth_result(warrior1: warrior, warrior2: warrior, fight_result: result):
    """
    update result of figths with one more figth data
    :param fight_result: current fight result structure
    :param warrior1: first warrior data
    :param warrior2: second warrior data
    :return:
    """
    hit1 = warrior1.wounds
    hit2 = warrior2.wounds
    technique1 = warrior1.technique.copy()
    technique2 = warrior2.technique.copy()
    while hit1 > 0 and hit2 > 0:
        # first warrior
        if technique1:
            current_technique = technique1.pop(randint(0, len(technique1) - 1))
            for word in current_technique.split():
                if word.lower() in warrior2.death_words:
                    hit2 -= 1
                    fight_result.wounded2 += 1
                    if hit2 == 0:
                        fight_result.death1 += 1
                        fight_result.win1 += 1
                        return

        else:
            fight_result.tired2 += 1
            fight_result.win2 += 1
            return
        # second warriors
        if technique2:
            current_technique = technique2.pop(randint(0, len(technique2) - 1))
            for word in current_technique.split():
                if word.lower() in warrior1.death_words:
                    hit1 -= 1
                    fight_result.wounded1 += 1
                    if hit1 == 0:
                        fight_result.death2 += 1
                        fight_result.win2 += 1
                        return

        else:
            fight_result.tired1 += 1
            fight_result.win1 += 1
            return


class DeathWords(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # init googlesheets api auth
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        http_auth = credentials.authorize(httplib2.Http())
        self.service = googleapiclient.discovery.build('sheets', 'v4', http=http_auth)
        self.warrior_data: List[warrior] = list()
        self.BtnLoad.clicked.connect(self.load_clicked)
        self.BtnFight.clicked.connect(self.fight_clicked)
        self.BtnFull.clicked.connect(self.full_clicked)
        self.spreadsheet_id = ""

    def load_clicked(self):
        """
        loads data form link to SpreadSheet and parces it
        :return:
        """
        self.statusbar.clearMessage()
        url_parts: List[str] = self.TxtPath.text().split(r'/')
        start: str = self.LineStart.text()
        end: str = self.LineEnd.text()
        if len(url_parts) < 2:
            error_message("Ссылка на таблицу не валидна")
        else:
            self.spreadsheet_id: str = url_parts[-1] if "edit" not in url_parts[-1] else url_parts[-2]
            # noinspection PyUnresolvedReferences
            try:
                answer = self.service.spreadsheets().values().get(spreadsheetId=self.spreadsheet_id,
                                                                  range='%s:%s' % (start, end)).execute()
                self.CBWar1.clear()
                self.CBWar2.clear()
                self.warrior_data = list()
                self.parse_warrior_data(answer['values'])

            except googleapiclient.errors.HttpError as e:
                error_message("Таблица не существует,\n неверный диапазон ячеек\n или отказано в доступе")
                print(e)

    def parse_warrior_data(self, warrior_list: List):
        """
        parse warrior data and creates structure with data and add it to UI
        :param warrior_list: list with data from spreadsheet
        :return:
        """
        techniques: List[str] = list()
        death_words: List[str] = list()
        row = 1
        for character in warrior_list:
            row += 1
            if len(character) >= 10:
                new_warrior = warrior(name=character[0], wounds=int(character[1]),
                                      word_num=int(character[2]), tech_num_weak=int(character[4]),
                                      tech_num=int(character[5]), tech_num_strong=int(character[6]),
                                      base_tech=character[9], death_words=list(), technique=list())
                # смерть-слова из общих и специальных для стран и школы
                source = general + special
                new_warrior.death_words.append(source.split()[randint(0, len(source.split())) - 1])
                for i in range(new_warrior.word_num - 1):
                    new_word = source.split()[randint(0, len(source.split())) - 1]
                    while new_word in new_warrior.death_words:
                        new_word = source.split()[randint(0, len(source.split())) - 1]
                    new_warrior.death_words.append(new_word)

                # смерть-слово для всеобщего приема
                i = randint(0, 2)
                new_warrior.death_words.append(extra.split()[i])

                # раздача приемов
                already_used = list()
                max_words = len(general.split()) - 1

                # особый прием, если он есть
                if new_warrior.base_tech in base.keys():
                    second_word = general.split()[randint(0, max_words)]
                    first_tech = base[new_warrior.base_tech] + ' ' + second_word
                    new_warrior.technique.append(first_tech)
                    already_used.append(second_word)
                    new_warrior.tech_num -= 1
                if new_warrior.base_tech == 'солнце' or new_warrior.name == 'Ху Лэй':
                    new_warrior.technique.append(east_sun)
                    new_warrior.tech_num_strong = - 1

                # слабые приемы
                for i in range(new_warrior.tech_num_weak):
                    new1 = weak.split()[randint(0, len(weak.split())-1)]
                    while new1 in already_used:
                        new1 = weak.split()[randint(0, len(weak.split())-1)]
                    already_used.append(new1)
                    new2 = general.split()[randint(0, max_words)]
                    while new2 in already_used:
                        new1 = general.split()[randint(0, max_words)]
                    already_used.append(new2)
                    new_warrior.technique.append(new1 + ' ' + new2)

                # обычные приемы
                for i in range(new_warrior.tech_num):
                    new1 = general.split()[randint(0, max_words)]
                    while new1 in already_used:
                        new1 = general.split()[randint(0, max_words)]
                    already_used.append(new1)
                    new2 = general.split()[randint(0, max_words)]
                    while new2 in already_used:
                        new2 = general.split()[randint(0, max_words)]
                    new_warrior.technique.append(new1 + ' ' + new2)
                    already_used.append(new2)

                # сильные приемы
                for i in range(new_warrior.tech_num_strong):
                    new1 = general.split()[randint(0, max_words)]
                    while new1 in already_used:
                        new1 = general.split()[randint(0, max_words)]
                    already_used.append(new1)
                    new2 = general.split()[randint(0, max_words)]
                    while new2 in already_used:
                        new2 = general.split()[randint(0, max_words)]
                    already_used.append(new2)
                    new3 = general.split()[randint(0, max_words)]
                    while new3 in already_used:
                        new3 = general.split()[randint(0, max_words)]
                    already_used.append(new3)
                    new_warrior.technique.append(new1 + ' ' + new2 + ' ' + new3)
                self.warrior_data.append(new_warrior)
                self.CBWar1.addItem(character[0])
                self.CBWar2.addItem(character[0])
                for word in new_warrior.death_words:
                    if word.lower() not in death_words:
                        death_words.append(word.lower())
                for technique in new_warrior.technique:
                    if technique.lower() not in techniques:
                        techniques.append(technique.lower())
                warrior_result = [' '.join(new_warrior.death_words)]
                warrior_result.extend(new_warrior.technique)
                request_body = {"valueInputOption": "RAW",
                                "data": [{"range": 'k%i:%s%i' % (row, titles[len(warrior_result)+10], row),
                                          "values": [warrior_result]}]}
                request = self.service.spreadsheets().values().batchUpdate(spreadsheetId=self.spreadsheet_id,
                                                                           body=request_body)
                _ = request.execute()
        if self.warrior_data:
            self.BtnFight.setEnabled(True)
            self.LblHits.setText("Число ударов: %i" % len(techniques))
            self.LblWords.setText("Число слов: %i" % len(death_words))
        print(sorted(techniques))
        print(sorted(death_words))

    def fight_clicked(self):
        self.statusbar.clearMessage()
        warrior1_name = self.CBWar1.currentText()
        warrior2_name = self.CBWar2.currentText()
        warrior1 = [w for w in self.warrior_data if w.name == warrior1_name][0]
        warrior2 = [w for w in self.warrior_data if w.name == warrior2_name][0]
        new_result = result()
        for i in range(self.SpinNum.value()):
            get_figth_result(warrior1, warrior2, new_result)
        self.LblWar1Vik.setText("%s победил %i раз" % (warrior1_name, new_result.win1))
        self.LblWar2Vik.setText("%s победил %i раз" % (warrior2_name, new_result.win2))
        self.LblWar1Wounds.setText("Из них ранения: %i" % new_result.death1)
        self.LblWar2Wounds.setText("Из них ранения: %i" % new_result.death2)
        self.LblWar1Tired.setText("Вымотан: %i раз" % new_result.tired1)
        self.LblWar2Tired.setText("Вымотан: %i раз" % new_result.tired2)

    def full_clicked(self):
        with open("fights.txt", "w") as f:
            for warrior1 in self.warrior_data:
                for warrior2 in self.warrior_data:
                    if warrior1.name != warrior2.name:
                        f.write(warrior1.name + " vs " + warrior2.name + '\n')
                        new_result = result()
                        for i in range(self.SpinNum.value()):
                            get_figth_result(warrior1, warrior2, new_result)
                        f.write("%s победил %i раз, Из них ранения: %i, Вымотал: %i раз, "
                                "получил %i ран\n" % (warrior1.name, new_result.win1, new_result.death1,
                                                      new_result.tired1, new_result.wounded1))
                        f.write("%s победил %i раз, Из них ранения: %i, Вымотал: %i раз, "
                                "получил %i ран\n" % (warrior2.name, new_result.win2, new_result.death2,
                                                      new_result.tired2, new_result.wounded2))
        f.close()
        self.statusbar.showMessage("Результат записан в файл fights.txt")


def initiate_exception_logging():
    # generating our hook
    # Back up the reference to the exceptionhook
    sys._excepthook = sys.excepthook

    def my_exception_hook(exctype, value, traceback):
        # Print the error and traceback
        logger.exception(f"{exctype}, {value}, {traceback}")
        # Call the normal Exception hook after
        # noinspection PyProtectedMember,PyUnresolvedReferences
        sys._excepthook(exctype, value, traceback)
        # sys.exit(1)

    # Set the exception hook to our wrapping function
    sys.excepthook = my_exception_hook


@logger.catch
def main():
    initiate_exception_logging()
    app = QtWidgets.QApplication(sys.argv)
    window = DeathWords()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
