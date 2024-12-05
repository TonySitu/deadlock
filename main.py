from controller import Controller
from UI import View


def main():
    controller = Controller()
    view = View(controller)
    controller.add_view(view)
    view.run()


if __name__ == "__main__":
    main()