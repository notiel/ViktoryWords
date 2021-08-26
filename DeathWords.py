import design
from dataclasses import dataclass
from PyQt5 import QtWidgets, QtGui
import sys
import os
from loguru import logger
import httplib2
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests

CREDENTIALS_FILE = 'token.json'

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

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
        self.BtnLoad.clicked.connect(self.load_clicked)

    def load_clicked(self):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                                       ['https://www.googleapis.com/auth/spreadsheets',
                                                                        'https://www.googleapis.com/auth/drive'])
        http_auth = credentials.authorize(httplib2.Http())
        url_parts = self.TxtPath.text().split(r'/')
        start = self.LineStart.text()
        end = self.LineEnd.text()
        if len(url_parts) < 2:
            error_message("Ссылка на таблицу не валидна")
        else:
            spreadsheet_id = url_parts[-1] if not "edit" in url_parts[-1] else url_parts[-2]
            error_message(spreadsheet_id)
            service = googleapiclient.discovery.build('sheets', 'v4', http=http_auth)
            try:
                answer = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                             range='%s:%s' % (start, end)).execute()
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


