import design
from dataclasses import dataclass, field
from PyQt5 import QtWidgets
import sys
from loguru import logger
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from typing import List
from random import randint, sample

titles = 'abcdefghijklmnopqrstuvwxyz'

CREDENTIALS_FILE = 'token.json'

weak = "ярость гнев удушье кровь"
middle = "пламя вихрь гром дождь тьма"
strong = "камень бамбук поток гора дракон река"

all_techniques = ['кровь ярость', "ярость гнев", "удушье гнев", "кровь дождь", "удушье вихрь",
                  "тема пламя", "гром тьма", "пламя вихрь", "гром гора", "поток дождь",
                  "река дракон", "гора поток", "бамбук река", "камень бамбук", "камень дракон"]

first_thresh = 5
second_thresh = 10


strength_dict = {1: weak, 2: middle, 3: strong}


# noinspection PyPep8Naming
@dataclass
class warrior:
    name: str
    wounds: int
    strength: int
    tech_num: int
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
    even: int = 0


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


def get_fight_result(warrior1: warrior, warrior2: warrior, fight_result: result):
    """
    update result of fights with one more fight data
    :param fight_result: current fight result structure
    :param warrior1: first warrior data
    :param warrior2: second warrior data
    :return:
    """
    hit1 = warrior1.wounds
    hit2 = warrior2.wounds
    technique1 = warrior1.technique.copy()
    technique2 = warrior2.technique.copy()
    while technique1 or technique2:
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
    # if (warrior1.wounds - hit1) > (warrior2.wounds - hit2):
    '''if hit1 > hit2:
        fight_result.tired1 += 1
        fight_result.win2 += 1
    # elif (warrior1.wounds - hit1) < (warrior2.wounds - hit2):
    elif hit1 < hit2:
        fight_result.tired2 += 1
        fight_result.win1 += 1
    else:'''
    fight_result.even += 1


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
            if len(character) >= 3:
                new_warrior = warrior(name=character[0], wounds=int(character[1]),
                                      strength=int(character[2]), tech_num=int(character[7]),
                                      death_words=list(), technique=list())
                # смерть-слова у всех по каждому
                new_warrior.death_words.append(weak.split()[randint(0, len(weak.split())) - 1])
                new_warrior.death_words.append(middle.split()[randint(0, len(middle.split())) - 1])
                new_warrior.death_words.append(strong.split()[randint(0, len(strong.split())) - 1])
                # доп слово своей силы
                source = strength_dict[new_warrior.strength]
                new_word = source.split()[randint(0, len(source.split())) - 1]
                while new_word in new_warrior.death_words:
                    new_word = source.split()[randint(0, len(source.split())) - 1]
                new_warrior.death_words.append(new_word)

                # раздача приемов
                weak_tech_num = first_thresh if new_warrior.tech_num >= first_thresh else new_warrior.tech_num
                middle_tech_num = second_thresh - first_thresh if new_warrior.tech_num >= second_thresh \
                    else max(new_warrior.tech_num - first_thresh, 0)
                strong_tech_num = max(new_warrior.tech_num - second_thresh, 0)
                indices = sample(range(0, first_thresh), weak_tech_num)
                middle_indices = sample(range(first_thresh, second_thresh), middle_tech_num)
                strong_indices = sample(range(second_thresh, len(all_techniques)), strong_tech_num)
                indices.extend(middle_indices)
                indices.extend(strong_indices)
                for ind in indices:
                    new_warrior.technique.append(all_techniques[ind])
                self.warrior_data.append(new_warrior)
                self.CBWar1.addItem(character[0])
                self.CBWar2.addItem(character[0])
                for word in new_warrior.death_words:
                    if word.lower() not in death_words:
                        death_words.append(word.lower())
                for technique in new_warrior.technique:
                    if technique.lower() not in techniques:
                        techniques.append(technique.lower())
                warrior_result = [' '.join(new_warrior.death_words), ', '.join(new_warrior.technique)]
                request_body = {"valueInputOption": "RAW",
                                "data": [{"range": 'i%i:j%i' % (row, row),
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
            get_fight_result(warrior1, warrior2, new_result)
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
                            get_fight_result(warrior1, warrior2, new_result)
                        f.write("%s победил %i раз, Из них смерть: %i, Вымотал: %i раз, "
                                "получил %i ран\n" % (warrior1.name, new_result.win1, new_result.death1,
                                                      new_result.tired1, new_result.wounded1))
                        f.write("%s победил %i раз, Из них смерть: %i, Вымотал: %i раз, "
                                "получил %i ран\n" % (warrior2.name, new_result.win2, new_result.death2,
                                                      new_result.tired2, new_result.wounded2))
                        f.write(f"Ничья {new_result.even} раз\n")
        '''
        with open("fights1.txt", "w") as f:
            for i in range(self.SpinNum.value()):
                f.write(f"{i}-ая волна сражений\n")
                for warrior1 in self.warrior_data:
                    warrior2 = self.warrior_data[randint(0, len(self.warrior_data) - 1)]
                    while warrior1.name == warrior2.name:
                        warrior2 = self.warrior_data[randint(0, len(self.warrior_data) - 1)]
                    f.write(warrior1.name + " vs " + warrior2.name + '\n')
                    new_result = result()
                    get_fight_result(warrior1, warrior2, new_result)
                    print(new_result)
                    if new_result.win1 > 0:
                        s_win = f"Победил {warrior1.name}. "
                        self.get_new_technique(warrior1)
                        warrior1.tech_num += 1
                        s_win += f"Получил технику {warrior1.technique[-1]}, у него {warrior1.tech_num} ударов\n"
                    elif new_result.win2 > 0:
                        s_win = f"Победил {warrior2.name}. "
                        self.get_new_technique(warrior2)
                        warrior2.tech_num += 1
                        s_win += f"Получил технику {warrior2.technique[-1]}, у него {warrior2.tech_num} ударов \n"
                    else:
                        s_win = "Ничья. "
                    if new_result.death1 > 0 or new_result.death2 > 0:
                        s_reason = "Причина: снял все ци. "
                    else:
                        s_reason = "Причина: Кончились удары. "
                    f.write(s_win + s_reason + f'Снято ци: {new_result.wounded1}, {new_result.wounded2}\n')
                    '''
        with open("fights2.txt", "w") as f:
            for i in range(self.SpinNum.value()):
                f.write(f"{i}-ая волна сражений. С добавлением ци\n")
                for warrior1 in self.warrior_data:
                    warrior2 = self.warrior_data[randint(0, len(self.warrior_data) - 1)]
                    while warrior1.name == warrior2.name:
                        warrior2 = self.warrior_data[randint(0, len(self.warrior_data) - 1)]
                    f.write(warrior1.name + " vs " + warrior2.name + '\n')
                    new_result = result()
                    get_fight_result(warrior1, warrior2, new_result)
                    print(new_result)
                    if new_result.win1 > 0:
                        s_win = f"Победил {warrior1.name}. "
                        self.get_new_technique(warrior1)
                        warrior1.tech_num += 1
                        warrior1.wounds += 1
                        s_win += f"Получил технику {warrior1.technique[-1]}, у него {warrior1.tech_num} ударов " \
                                 f"и {warrior1.wounds} ци\n"
                    elif new_result.win2 > 0:
                        s_win = f"Победил {warrior2.name}. "
                        self.get_new_technique(warrior2)
                        warrior2.tech_num += 1
                        warrior2.wounds += 1
                        s_win += f"Получил технику {warrior2.technique[-1]}, у него {warrior2.tech_num} ударов " \
                                 f"и {warrior2.wounds} ци\n"
                    else:
                        s_win = "Ничья. "
                    if new_result.death1 > 0 or new_result.death2 > 0:
                        s_reason = "Причина: снял все ци. "
                    else:
                        s_reason = "Причина: Кончились удары. "
                    f.write(s_win + s_reason + f'Снято ци: {new_result.wounded1}, {new_result.wounded2}\n')
            self.statusbar.showMessage("Результат записан в файл fights.txt, fight1.txt, fight2.txt")

    @staticmethod
    def get_new_technique(character: warrior):
        if character.tech_num < len(all_techniques):
            if character.tech_num < first_thresh:
                ind_start = 0
                ind_end = first_thresh
            elif character.tech_num < second_thresh:
                ind_start = first_thresh
                ind_end = second_thresh
            else:
                ind_start = second_thresh
                ind_end = len(all_techniques)
            new_technique = all_techniques[randint(ind_start, ind_end-1)]
            while new_technique in character.technique:
                new_technique = all_techniques[randint(ind_start, ind_end-1)]
            character.technique.append(new_technique)


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
