import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import chrome_session
import follow_actions


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Logo
        img = Image.open('resource_data/logo.png')
        # img = img.resize((200, 100))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo

        # Labels
        label1 = tk.Label(self, text="If you are logged in", font="Times", padx=56.5)
        label2 = tk.Label(self, text="If you are not logged in", font="Times")
        label3 = tk.Label(self, text="Open Session", font="Times")

        # Buttons
        button1 = tk.Button(self, text="Click Here", font="Times",
                            command=lambda: logged_in_windows())

        button2 = tk.Button(self, text="Click Here", font="Times",
                            command=lambda: threading.Thread(target=login_window).start())

        button3 = tk.Button(self, text="Click Here", font="Times",
                            command=lambda: threading.Thread(target=chrome_driver_headless).start())

        exit_program_button = tk.Button(self, text="Exit", font="Times",
                                        command=lambda: exit_program_function())

        # Text
        text = tk.Text(self, height=1, width=49, pady=2)
        text.insert(tk.END, "NOTE: 1st open session, and use whatever u want!")

        # Interface
        logo_label.grid(row=0, columnspan=2)

        label1.grid(row=1, column=0)
        button1.grid(row=1, column=1)

        label2.grid(row=2, column=0)
        button2.grid(row=2, column=1)

        label3.grid(row=3, column=0)
        button3.grid(row=3, column=1)

        text.grid(row=4, columnspan=2, padx=1, pady=15)

        exit_program_button.grid(row=5, column=1, pady=(0, 10))

        def logged_in_windows():
            controller.show_frame(SecondPage)

        def login_window():
            chrome_driver_with_head()

        def chrome_driver_headless():
            chrome_session.launch_chrome(headless=True)

        def chrome_driver_with_head():
            chrome_session.launch_chrome(headless=False)

        def exit_program_function():
            app.destroy()


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # Logo
        img = Image.open('resource_data/logo.png')
        # img = img.resize((200, 100))
        logo = ImageTk.PhotoImage(img)
        logo_label = tk.Label(self, image=logo)
        logo_label.image = logo

        # Progress Bar
        my_progress = ttk.Progressbar(self, orient="horizontal", length=397, mode="determinate")

        # Labels
        label1 = tk.Label(self, text="Sync Data", font="Times")
        label2 = tk.Label(self, text="See ppl not following you back", font="Times")
        label3 = tk.Label(self, text="Unfollow all pl not following you back", font="Times")

        # Buttons
        button1 = tk.Button(self, text="Click Here", font="Times",
                            command=lambda: threading.Thread(target=sync_data).start())

        button2 = tk.Button(self, text="Click Here", font="Times",
                            command=lambda: new_windows())
        #                    command=lambda: see_not_following_back())

        button3 = tk.Button(self, text="Click Here", font="Times",
                            command=lambda: threading.Thread(target=unfollow_ppl).start())

        back = tk.Button(self, text="Back", font="Times",
                         command=lambda: back_button_function())

        text_box = tk.Text(self, height=5, width=52)

        exit_program_button = tk.Button(self, text="Exit", font="Times",
                                        command=lambda: app.destroy())

        # Interface
        logo_label.grid(row=0, columnspan=2)

        label1.grid(row=1, column=0)
        button1.grid(row=1, column=1)

        label2.grid(row=2, column=0)
        button2.grid(row=2, column=1)

        label3.grid(row=3, column=0)
        button3.grid(row=3, column=1)

        my_progress.grid(row=4, columnspan=2, padx=1, pady=15)

        back.grid(row=5, column=0, pady=(0, 10))

        exit_program_button.grid(row=5, column=1, pady=(0, 10))

        # New Window
        def new_windows():
            # global logo_img, logo_label, label1, label2, label3, button1, button2, top

            top = tk.Toplevel()
            top.title("Unfollowers")

            # Logo
            img = Image.open('resource_data/logo.png')
            # img = img.resize((200, 100))
            logo = ImageTk.PhotoImage(img)
            logo_label = tk.Label(top, image=logo)
            logo_label.image = logo

            # Buttons
            exit_program_buttonn = tk.Button(top, text="Exit", font="Times",
                                             command=lambda: top.destroy())

            # Interface
            logo_label.grid(row=0, column=0, columnspan=4)

            # Create A Main Frame
            main_frame = tk.Frame(top)
            main_frame.grid(row=1, column=0, rowspan=4, columnspan=4)
            # main_frame.pack(fill="both", expand=1)

            # Create A Canvas
            my_canvas = tk.Canvas(main_frame)
            my_canvas.grid(row=0, column=0, rowspan=3, columnspan=3, sticky="w")
            # my_canvas.pack(side="left", fill="both", expand=1)

            # Add A Scrollbar To The Canvas
            my_scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=my_canvas.yview)
            my_scrollbar.grid(row=1, column=3, sticky="e")
            # my_scrollbar.pack(side="right", fill="y")

            # Configure The Canvas
            my_canvas.configure(yscrollcommand=my_scrollbar.set)
            my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion=my_canvas.bbox("all")))

            # Create ANOTHER Frame INSIDE the Canvas
            second_frame = tk.Frame(my_canvas)

            # Add that New frame To a Window In The Canvas
            my_canvas.create_window((0, 0), window=second_frame, anchor="nw")

            with open(r'synced_data\not_following_back.txt', 'r') as assholes:
                # global inc_in_progress
                total_user_names = len(assholes.readlines())
                # inc_in_progress = 100 / total_user_names
                assholes.seek(0)
                gui_line_no = 1
                for i in range(total_user_names):
                    user_name = assholes.readline()
                    user_name_without_newline = user_name[:-1]

                    # Get name V tough, instead make csv file n read from there
                    """driver.get('https://www.instagram.com/' + user_name_without_newline)
                    name = driver.find_element_by_xpath('//*[@class="rhpdm"][0]').get_attribute("src")"""

                    name = 'Name'
                    u_name = tk.Label(second_frame, text=user_name_without_newline, font="Times")
                    name = tk.Label(second_frame, text=name, font="Times")
                    # pic = tk.Label(second_frame, text="UserPic", font="Times")

                    # Profile Picture
                    pic = Image.open('resource_data/demo_profile_pic.png')
                    # pic = Image.open('Profile Data/'+user_name_without_newline+'.png')
                    pic = pic.resize((50, 50))
                    profilepic = ImageTk.PhotoImage(pic)
                    profilepic_label = tk.Label(second_frame, image=profilepic)
                    profilepic_label.image = profilepic

                    unfollow_button = tk.Button(second_frame, text="Unfollow", font="Times",
                                                command=lambda: unfollow_button_by_id())

                    profilepic_label.grid(row=gui_line_no, column=0)
                    # pic.grid(row=gui_line_no, column=0)
                    u_name.grid(row=gui_line_no, column=1)
                    name.grid(row=gui_line_no + 1, column=1, pady=(0, 20))
                    unfollow_button.grid(row=gui_line_no, column=2, sticky='E')

                    gui_line_no += 2

            # here both rows should be last
            exit_program_buttonn.grid(row=5, column=2, pady=(0, 10))

        # Functions
        def back_button_function():
            controller.show_frame(FirstPage)
            text_box.destroy()

        def sync_data():
            my_progress.start(10)
            follow_actions.make_follow_following_data()
            my_progress.stop()

        def see_not_following_back():
            file = open(r'synced_data\not_following_back.txt').read()
            text_box.grid(row=6, columnspan=2)
            text_box.insert(tk.END, file)

        def unfollow_ppl():
            my_progress.start(10)
            follow_actions.unfollow_people()
            my_progress.stop()

        def unfollow_button_by_id():
            pass


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Creating a Window
        window = tk.Frame(self)
        window.grid()

        # To specify minimum size of windows irrespective to buttons, labels, logos etc
        """window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)"""

        self.frames = {}
        for F in (FirstPage, SecondPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Instagram Tool")
        self.iconbitmap('resource_data/ico.ico')


app = Application()
app.mainloop()
