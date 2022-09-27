# entry point
from application.controllers.main import MainController


def main():
    controller = MainController()
    controller.start()


if __name__ == '__main__':
    main()
