import design
from dataclasses import dataclass, field
from PyQt5 import QtWidgets
import sys
from loguru import logger
from typing import List
from random import randint
import csv

logger.start("logfile.log", rotation="1 week", format="{time} {level} {message}", level="DEBUG", enqueue=True)


@dataclass
class warrior:
    name: str
    wounds: int
    death_words: List[str] = field(default_factory=list)
    technique: List[str] = field(default_factory=list)


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
    error.setIcon(QtWidgets.QMessageBox.Critical)
    error.setText(text)
    error.setWindowTitle('Error!')
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
            current_technique = technique1.pop(randint(0, len(technique1)-1))
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
            current_technique = technique2.pop(randint(0, len(technique2)-1))
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
        self.warrior_data: List[warrior] = list()
        self.BtnLoad.clicked.connect(self.load_clicked)
        self.BtnFight.clicked.connect(self.fight_clicked)
        self.BtnFull.clicked.connect(self.full_clicked)

    def load_clicked(self):
        """
        loads data form link to SpreadSheet and parces it
        :return:
        """
        self.statusbar.clearMessage()
        self.CBWar1.clear()
        self.CBWar2.clear()
        self.warrior_data = list()
        # noinspection PyArgumentList,PyCallByClass
        new_filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file...', None, "*.csv")[0]
        try:
            if new_filename:
                with open(new_filename, encoding='utf-8') as csvfile:
                    data = csv.reader(csvfile, delimiter=',', quotechar='"')
                    self.LblPath.setText("Выбран файл %s" % new_filename)
                    self.parse_warrior_data(data)
        except Exception as e:
            error_message("Неверный формат файла")
            logger.error(e)

    def parse_warrior_data(self, warrior_list: List):
        """
        parse warrior data and creates structure with data and add it to UI
        :param warrior_list: list with data from spreadsheet
        :return:
        """
        techniques: List[str] = list()
        death_words: List[str] = list()
        for character in warrior_list:
            try:
                if len(character) > 4:
                    new_warrior = warrior(name=character[0], wounds=int(character[1]),
                                      death_words=character[2].lower().split(','), technique=character[3:])
                    new_warrior.death_words = [x.strip() for x in new_warrior.death_words]
                    new_warrior.technique = [x.lower().strip() for x in new_warrior.technique]
                    self.warrior_data.append(new_warrior)
                    self.CBWar1.addItem(character[0])
                    self.CBWar2.addItem(character[0])
                    for word in new_warrior.death_words:
                        if word.lower() not in death_words:
                            death_words.append(word.lower())
                    for technique in new_warrior.technique:
                        if technique.lower() not in techniques:
                            techniques.append(technique.lower())
            except ValueError:
                continue

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
                        f.write("%s победил %i раз, Из них ранения: %i, Вымотал: %i раз, получил %i ран\n"
                                % (warrior1.name, new_result.win1, new_result.death1, new_result.tired1,
                                   new_result.wounded1))
                        f.write("%s победил %i раз, Из них ранения: %i, Вымотал: %i раз, получил %i ран\n" %
                                (warrior2.name, new_result.win2, new_result.death2, new_result.tired2,
                                 new_result.wounded2))
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
        # noinspection PyProtectedMember
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
