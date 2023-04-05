from controller.controller import Controller
from ui.ui import Ui

if __name__ == '__main__':

    my_controller = Controller((100, 30, 1.9, 0.9, 0.05, 0.5, 3, 10))
    my_ui = Ui(my_controller)

    my_ui.main()

