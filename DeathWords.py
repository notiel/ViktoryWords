import design
from dataclasses import dataclass, field
from PyQt5 import QtWidgets
import sys
from loguru import logger
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from typing import List

CREDENTIALS_FILE = 'token.json'


@dataclass
class warrior:
    name: str
    wounds: int
    core: str
    death_words: field(default_factory=list)
    technique: field(default_factory=list)


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
        self.BtnLoad.clicked.connect(self.load_clicked)

    def load_clicked(self):
        url_parts: List[str] = self.TxtPath.text().split(r'/')
        start: str = self.LineStart.text()
        end: str = self.LineEnd.text()
        if len(url_parts) < 2:
            error_message("Ссылка на таблицу не валидна")
        else:
            spreadsheet_id: str = url_parts[-1] if "edit" not in url_parts[-1] else url_parts[-2]
            # noinspection PyUnresolvedReferences
            try:
                answer = self.service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                                  range='%s:%s' % (start, end)).execute()
                warrior_data: List[warrior] = list()
                for character in answer['values']:
                    if len(character) > 4:
                        warrior_data.append(warrior(name=character[0], wounds=character[1], core=character[3],
                                              death_words=character[2].split(', '),  technique=character[4:]))
                

            except googleapiclient.errors.HttpError:
                error_message("Таблица не существует,\n неверный диапазон ячеек\n или отказано в доступе")


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
