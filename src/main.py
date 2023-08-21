from src import config
from src.contoller import Controller
from src.model import Model
from src.view import View


def main():
    model = Model(
        config.YDB_ENDPOINT,
        config.YDB_DATABASE,
        config.BUNDLE_DIR / config.YDB_SERVICE_ACCOUNT_KEY
    )
    controller = Controller(model)
    view = View(controller)
    view.mainloop()


if __name__ == "__main__":
    main()
