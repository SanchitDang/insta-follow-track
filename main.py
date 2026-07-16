import os
import threading
import tkinter as tk

import ttkbootstrap as ttkb
from ttkbootstrap.dialogs import Messagebox
from PIL import Image, ImageTk

import chrome_session
import follow_actions

APP_TITLE = "Instagram Follow Tracker"
THEME = "darkly"
FONT_FAMILY = "Segoe UI"
HEADER_FONT = (FONT_FAMILY, 18, "bold")
SUBHEADER_FONT = (FONT_FAMILY, 10)
SECTION_FONT = (FONT_FAMILY, 11, "bold")

NOT_FOLLOWING_BACK_FILE = r'synced_data/not_following_back.txt'
ACC_YOU_FOLLOW_FILE = r'synced_data/acc_you_follow.txt'
ACC_FOLLOWING_YOU_FILE = r'synced_data/acc_following_you.txt'


def run_async(widget, func, on_done=None):
    """Run func() on a background thread; on_done(result) is invoked back on
    the Tk main thread once finished, so callers can safely touch widgets."""
    def worker():
        result = func()
        if on_done:
            widget.after(0, lambda: on_done(result))
    threading.Thread(target=worker, daemon=True).start()


def count_lines(path):
    try:
        with open(path, 'r') as f:
            return sum(1 for _ in f)
    except FileNotFoundError:
        return None


def load_logo(parent, max_width=260, tint="#E8E8E8"):
    """Load the wordmark, recolored to `tint` (it's a dark mark that's nearly
    invisible on the dark theme's background otherwise)."""
    img = Image.open('resource_data/logo.png').convert('RGBA')
    ratio = max_width / img.width
    img = img.resize((max_width, int(img.height * ratio)))
    if tint:
        solid = Image.new('RGBA', img.size, tint)
        solid.putalpha(img.split()[3])
        img = solid
    photo = ImageTk.PhotoImage(img)
    label = ttkb.Label(parent, image=photo)
    label.image = photo
    return label


class SessionPage(ttkb.Frame):
    """Entry page: open a debuggable Chrome session, then continue to the dashboard."""

    def __init__(self, parent, controller):
        super().__init__(parent, padding=24)

        load_logo(self).pack(pady=(0, 8))
        ttkb.Label(self, text=APP_TITLE, font=HEADER_FONT).pack()
        ttkb.Label(
            self, text="Find and unfollow accounts that don't follow you back.",
            font=SUBHEADER_FONT, bootstyle="secondary"
        ).pack(pady=(0, 20))

        step1 = ttkb.Labelframe(self, text="Step 1 - Open a Chrome session", padding=16)
        step1.pack(fill="x", pady=(0, 16))
        ttkb.Label(
            step1, text="Log into Instagram in the window that opens. This is remembered\n"
                        "for future runs, so you only need to do it again if you sign out.",
            justify="left"
        ).pack(anchor="w", pady=(0, 12))

        btn_row = ttkb.Frame(step1)
        btn_row.pack(fill="x")
        ttkb.Button(
            btn_row, text="Open Chrome", bootstyle="primary",
            command=lambda: chrome_session.launch_chrome(headless=False)
        ).pack(side="left", padx=(0, 8))
        ttkb.Button(
            btn_row, text="Open Chrome (Headless)", bootstyle="secondary-outline",
            command=lambda: chrome_session.launch_chrome(headless=True)
        ).pack(side="left")

        step2 = ttkb.Labelframe(self, text="Step 2 - Continue", padding=16)
        step2.pack(fill="x", pady=(0, 16))
        ttkb.Button(
            step2, text="Continue to Dashboard →", bootstyle="success",
            command=lambda: controller.show_frame(DashboardPage)
        ).pack(fill="x")

        ttkb.Button(
            self, text="Exit", bootstyle="link", command=controller.destroy
        ).pack(pady=(8, 0))


class DashboardPage(ttkb.Frame):
    """Main dashboard: sync follow data, review, and unfollow accounts that don't follow back."""

    def __init__(self, parent, controller):
        super().__init__(parent, padding=24)
        self.controller = controller

        load_logo(self, max_width=200).pack(pady=(0, 8))
        ttkb.Label(self, text="Dashboard", font=HEADER_FONT).pack(pady=(0, 4))

        self.status_var = tk.StringVar(value="Not synced yet.")
        ttkb.Label(
            self, textvariable=self.status_var, bootstyle="secondary",
            wraplength=380, justify="center"
        ).pack(pady=(0, 12))

        self.progress = ttkb.Progressbar(self, mode="indeterminate", bootstyle="info-striped")
        self.progress.pack(fill="x", pady=(0, 16))

        actions = ttkb.Frame(self)
        actions.pack(fill="x", pady=(0, 8))

        self.sync_btn = ttkb.Button(
            actions, text="Sync Data", bootstyle="primary", command=self.sync_data
        )
        self.sync_btn.pack(fill="x", pady=4)

        self.view_btn = ttkb.Button(
            actions, text="View Accounts Not Following Back", bootstyle="info-outline",
            command=self.open_unfollowers_window
        )
        self.view_btn.pack(fill="x", pady=4)

        self.unfollow_btn = ttkb.Button(
            actions, text="Unfollow All That Don't Follow Back", bootstyle="danger",
            command=self.confirm_unfollow_all
        )
        self.unfollow_btn.pack(fill="x", pady=4)

        bottom = ttkb.Frame(self)
        bottom.pack(fill="x", pady=(12, 0))
        ttkb.Button(
            bottom, text="← Back", bootstyle="secondary-outline",
            command=lambda: controller.show_frame(SessionPage)
        ).pack(side="left")
        ttkb.Button(
            bottom, text="Exit", bootstyle="link", command=controller.destroy
        ).pack(side="right")

        self.refresh_status()

    def refresh_status(self):
        following = count_lines(ACC_YOU_FOLLOW_FILE)
        followers = count_lines(ACC_FOLLOWING_YOU_FILE)
        not_back = count_lines(NOT_FOLLOWING_BACK_FILE)
        if following is None:
            self.status_var.set("Not synced yet - click Sync Data to get started.")
        else:
            self.status_var.set(
                f"Following {following} - Followed by {followers} - "
                f"{not_back} don't follow you back"
            )

    def set_busy(self, busy, message=None):
        state = "disabled" if busy else "normal"
        self.sync_btn.config(state=state)
        self.view_btn.config(state=state)
        self.unfollow_btn.config(state=state)
        if busy:
            self.progress.start(10)
        else:
            self.progress.stop()
        if message:
            self.status_var.set(message)

    def sync_data(self):
        self.set_busy(True, "Syncing follow data...")

        def task():
            try:
                follow_actions.make_follow_following_data()
                return None
            except Exception as e:
                return e

        def done(error):
            self.set_busy(False)
            if error:
                Messagebox.show_error(f"Sync failed: {error}", title=APP_TITLE)
            self.refresh_status()

        run_async(self, task, done)

    def confirm_unfollow_all(self):
        not_back = count_lines(NOT_FOLLOWING_BACK_FILE)
        if not not_back:
            Messagebox.show_info("Nothing to unfollow - sync data first.", title=APP_TITLE)
            return
        confirmed = Messagebox.yesno(
            f"Unfollow all {not_back} accounts that don't follow you back?\n"
            "This performs real actions on Instagram and can't be undone automatically.",
            title="Confirm bulk unfollow"
        )
        if confirmed == "Yes":
            self.unfollow_all()

    def unfollow_all(self):
        self.set_busy(True, "Unfollowing accounts...")
        run_async(
            self, follow_actions.unfollow_people,
            lambda _: self.set_busy(False, "Done. Sync again to confirm.")
        )

    def open_unfollowers_window(self):
        if count_lines(NOT_FOLLOWING_BACK_FILE) is None:
            Messagebox.show_info("Nothing to show yet - sync data first.", title=APP_TITLE)
            return
        UnfollowersWindow(self)


class UnfollowersWindow(ttkb.Toplevel):
    """Popup listing accounts that don't follow back, with a per-account unfollow button."""

    def __init__(self, parent):
        super().__init__(title="Accounts Not Following Back")
        self.geometry("420x520")

        header = ttkb.Frame(self, padding=(16, 16, 16, 8))
        header.pack(fill="x")
        ttkb.Label(header, text="Not Following You Back", font=SECTION_FONT).pack(anchor="w")

        container = ttkb.Frame(self, padding=(16, 0))
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttkb.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        rows_frame = ttkb.Frame(canvas)
        canvas.create_window((0, 0), window=rows_frame, anchor="nw")
        rows_frame.bind(
            '<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        try:
            with open(NOT_FOLLOWING_BACK_FILE, 'r') as f:
                usernames = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            usernames = []

        avatar_img = Image.open('resource_data/demo_profile_pic.png').resize((44, 44))
        self._avatar_photo = ImageTk.PhotoImage(avatar_img)

        if not usernames:
            ttkb.Label(rows_frame, text="Nobody here - everyone follows you back!").pack(pady=20)

        for username in usernames:
            self._build_row(rows_frame, username)

        ttkb.Button(
            self, text="Close", bootstyle="secondary", command=self.destroy
        ).pack(pady=12)

    def _build_row(self, parent, username):
        row = ttkb.Frame(parent, padding=(0, 8))
        row.pack(fill="x")

        ttkb.Label(row, image=self._avatar_photo).pack(side="left", padx=(0, 10))
        ttkb.Label(row, text=username, font=(FONT_FAMILY, 10, "bold")).pack(side="left")

        button = ttkb.Button(row, text="Unfollow", bootstyle="danger-outline", width=10)
        button.config(command=lambda: self._start_unfollow(username, button))
        button.pack(side="right")

    def _start_unfollow(self, username, button):
        button.config(state="disabled", text="Working...")

        def task():
            return follow_actions.unfollow_one(username)

        def done(success):
            button.config(
                text="Unfollowed" if success else "Failed",
                bootstyle="secondary" if success else "danger"
            )

        run_async(button, task, done)


class Application(ttkb.Window):
    def __init__(self):
        super().__init__(title=APP_TITLE, themename=THEME, resizable=(False, False))
        icon_path = 'resource_data/ico.ico'
        if os.path.exists(icon_path):
            self.iconbitmap(icon_path)

        container = ttkb.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (SessionPage, DashboardPage):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SessionPage)

    def show_frame(self, page):
        self.frames[page].tkraise()


if __name__ == '__main__':
    app = Application()
    app.mainloop()
