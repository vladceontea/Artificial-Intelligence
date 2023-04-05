from controller.controller import Controller
from repository.repository import Repository
from ui.ui import Ui

if __name__ == '__main__':

    my_repo = Repository()
    my_controller = Controller(my_repo, (40, 10, 40, 0.04, 0.8))
    my_ui = Ui(my_controller)

    my_ui.main()
