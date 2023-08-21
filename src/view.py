import threading
import tkinter as tk
from tkinter import messagebox
from typing import Callable

import ydb.issues

from src import config, styles
from src.contoller import Controller
from src.exceptions import IncorrectNumber, WrongPassword


def make_non_resizable(window: tk.Tk | tk.Toplevel):
    window.resizable(width=False, height=False)


def set_favicon(window: tk.Tk | tk.Toplevel):
    favicon_path = config.BUNDLE_DIR / "favicon.ico"
    window.iconbitmap(favicon_path)


def place_close_to_parent(
        window: tk.Tk | tk.Toplevel, parent: tk.Tk | tk.Toplevel):
    x = parent.winfo_x() + 25
    y = parent.winfo_y() + 25
    window.geometry(f"+{x}+{y}")


def show_loading_window(
        parent: tk.Tk | tk.Toplevel,
        operation: Callable[[tk.Toplevel], None],
        *args,
        **kwargs
):
    window = tk.Toplevel(parent, **styles.WINDOW_STYLES)

    window.grab_set()

    def prevent_close():
        pass

    window.protocol("WM_DELETE_WINDOW", prevent_close)

    make_non_resizable(window)
    set_favicon(window)
    place_close_to_parent(window, parent)

    tk.Label(
        window, **styles.LABEL_STYLES, text="Подождите, идет загрузка..."
    ).pack(
        padx=20, pady=15)

    thread = threading.Thread(
        target=operation, args=(window, *args), kwargs=kwargs)
    thread.start()


def show_number_window(parent: tk.Tk | tk.Toplevel, number: int):
    window = tk.Toplevel(parent, **styles.WINDOW_STYLES)

    window.grab_set()

    make_non_resizable(window)
    set_favicon(window)
    place_close_to_parent(window, parent)

    number_label_styles = {**styles.LABEL_STYLES, "font": ("Arial", 20)}
    tk.Label(
        window, **number_label_styles, text=number,
    ).pack(
        padx=20, pady=(15, 0))

    tk.Label(
        window, **styles.LABEL_STYLES, text="Используйте указанное число"
    ).pack(
        padx=20, pady=(0, 15))


class View(tk.Tk):
    def __init__(self, controller: Controller):
        super().__init__()

        self.controller = controller

        self.configure(**styles.WINDOW_STYLES)
        self.title("Нумератор")
        self.bind("<Configure>", self.on_configure)

        make_non_resizable(self)
        set_favicon(self)

        tk.Button(
            self, **styles.PRIMARY_BUTTON_STYLES, text="Получить номер", width=20,
            command=self.get_next_number_command
        ).pack(
            side="left", padx=(20, 5), pady=10)

        tk.Button(
            self, **styles.BUTTON_STYLES, text="Установить номер", width=20,
            command=self.set_number_command
        ).pack(
            side="right", padx=(5, 20), pady=10)

    def on_configure(self, _):
        state = self.state()
        for child in self.winfo_children():
            if isinstance(child, tk.Toplevel):
                child.state(state)

    def get_next_number_command(self):
        def load_and_show_next_number(loading_window: tk.Toplevel):
            try:
                number = self.controller.get_next_number()
            except ydb.issues.Aborted:
                loading_window.destroy()
                messagebox.showwarning(
                    title="Внимание",
                    message=f"Вероятно, что кто-то другой уже выполняет "
                            f"операцию. Чтобы предотвратить конфликт, Ваш "
                            f"запрос был отклонен. Попробуйте выполнить "
                            f"операцию еще раз.",
                    parent=self)
            except ydb.issues.Error as e:
                loading_window.destroy()
                messagebox.showerror(
                    title="Ошибка",
                    message=f"Произошла ошибка при выполнении операции. "
                            f"Попробуйте выполнить операцию позже. "
                            f"Сообщение ошибки: {e.message}",
                    parent=self)
            else:
                loading_window.destroy()
                show_number_window(self, number)

        show_loading_window(self, load_and_show_next_number)

    def set_number_command(self):
        SetNumberFormWindow(self)


class SetNumberFormWindow(tk.Toplevel):
    def __init__(self, parent: View):
        super().__init__(parent, **styles.WINDOW_STYLES)

        self.parent = parent

        self.grab_set()

        make_non_resizable(self)
        set_favicon(self)
        place_close_to_parent(self, parent)

        tk.Label(
            self, **styles.LABEL_STYLES, text="Номер"
        ).grid(
            row=0, column=0, padx=(20, 10), pady=(20, 5))

        self.number_entry = tk.Entry(self, **styles.ENTRY_STYLES)
        self.number_entry.grid(
            row=0, column=1, ipady=10, padx=(0, 20), pady=(20, 5))

        tk.Label(
            self, **styles.LABEL_STYLES, text="Пароль"
        ).grid(
            row=1, column=0, padx=(20, 10))

        self.password_entry = tk.Entry(self, **styles.ENTRY_STYLES, show="*")
        self.password_entry.grid(row=1, column=1, ipady=10, padx=(0, 20))

        tk.Button(
            self, **styles.PRIMARY_BUTTON_STYLES, text="Установить номер", width=25,
            command=self.submit_command
        ).grid(
            row=2, column=0, columnspan=2, pady=(10, 20))

    def submit_command(self):
        number = self.number_entry.get()
        password = self.password_entry.get()

        def set_number(loading_window: tk.Toplevel):
            try:
                self.parent.controller.set_number(password, number)
            except IncorrectNumber:
                loading_window.destroy()
                messagebox.showerror(
                    title="Ошибка", message="Введено некорректное число.",
                    parent=self)
            except WrongPassword:
                loading_window.destroy()
                messagebox.showerror(
                    title="Ошибка", message="Введен неверный пароль.",
                    parent=self)
            except ydb.issues.Aborted:
                loading_window.destroy()
                messagebox.showwarning(
                    title="Внимание",
                    message=f"Вероятно, что кто-то другой уже выполняет "
                            f"операцию. Чтобы предотвратить конфликт, Ваш "
                            f"запрос был отклонен. Попробуйте выполнить "
                            f"операцию еще раз.",
                    parent=self)
            except ydb.issues.Error as e:
                loading_window.destroy()
                messagebox.showerror(
                    title="Ошибка",
                    message=f"Произошла ошибка при выполнении операции. "
                            f"Сообщение ошибки: {e.message}",
                    parent=self)
            else:
                loading_window.destroy()
                self.destroy()
                messagebox.showinfo(
                    title="Успешно",
                    message=f"Номер {number} успешно установлен в качестве "
                            f"последнего использованного номера")

        show_loading_window(self, set_number)
