import sys

from PyQt5.QtWidgets import QApplication

from game import Game


if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = Game()
    sys.exit(app.exec_())
