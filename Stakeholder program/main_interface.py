from tkinter import *
from tkinter import colorchooser
from backend_functions import *
import re


class App(Frame):
    def __init__(self, window):
        self.colourHex = grey
        super().__init__(window, bg=self.colourHex)

        # information needed in most of the classes
        self.account_type = ""
        self.username = ""
        self.name = ""
        self.quiz_title = ""
        self.current_score = ""
        self.temporary_frame = []

        self.main_frame = self
        self.main_frame.pack(fill=BOTH, expand=True)
        # making the whole window into one row and column
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        self.frames = {}
        Pages = (
            StartPage,
            LoginPage,
            RegisterPage,
            TeacherPage,
            StudentPage,
            QuizPage,
            QuizMaker,
            AssignPage,
            LeaderboardPage,
            AssignmentPage,
            ReportPage,
            EditPage,
        )

        for Page in Pages:
            # Page is the name from the tuple
            name = Page.__name__
            frame = Page(self.main_frame, self)
            self.frames[name] = frame
            # putting page in the dictionaryS
            frame.grid(row=0, column=0, sticky="nsew")

        self.current_page = None
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        self.current_page = page_name
        frame = self.frames[page_name]
        frame.tkraise()
        return frame

    def label(self, parent, text, size, x, y):
        label = Label(
            parent,
            text=text,
            font=("Arial", size),
            bg=self.colourHex,
            fg=white,
            wraplength=1100,
            justify="left",
            anchor="w",
        )
        label.place(x=x, y=y)
        return label

    def entry(self, parent, size, x, y, width=None):
        entry = Entry(
            parent, font=("Arial", size), bg=white, fg=self.colourHex, width=width
        )
        if width is not None:
            entry.config(width=width)
        entry.place(x=x, y=y)
        return entry

    def button(self, parent, text, size, x, y, command, width=None):
        button = Button(
            parent,
            text=text,
            font=("Arial", size),
            activebackground=self.colourHex,
            bg=self.colourHex,
            fg=white,
            width=width,
            command=command,
            activeforeground=white,
        )
        if width is not None:
            button.config(width=width)
        button.place(x=x, y=y)

    def set_colour(self):
        self.colour = colorchooser.askcolor()
        if self.colour[1] is None:
            return
        self.colourHex = self.colour[1]
        for page in self.frames:
            frame = self.frames[page]
            frame.configure(bg=self.colourHex)
            for widget in frame.winfo_children():
                if isinstance(widget, Entry):
                    widget.configure(fg=self.colourHex)
                elif isinstance(widget, Radiobutton):
                    widget.configure(
                        selectcolor=self.colourHex,
                        bg=self.colourHex,
                        activebackground=self.colourHex,
                    )
                elif isinstance(widget, Button):
                    widget.configure(activebackground=self.colourHex, bg=self.colourHex)
                else:
                    widget.configure(bg=self.colourHex)
        for i in self.temporary_frame:
            # prevents accessing frames that dont exist
            if i.winfo_exists():
                for widget in i.winfo_children():
                    if isinstance(widget, Entry):
                        widget.configure(fg=self.colourHex)
                    elif isinstance(widget, Radiobutton):
                        widget.configure(
                            selectcolor=self.colourHex,
                            bg=self.colourHex,
                            activebackground=self.colourHex,
                        )
                    elif isinstance(widget, Button):
                        widget.configure(
                            activebackground=self.colourHex, bg=self.colourHex
                        )
                    elif isinstance(widget, Text):
                        widget.configure(fg=self.colourHex)
                    else:
                        widget.configure(bg=self.colourHex)

    def radio_button(self, parent, list, x, y, size, width, p=None):
        a = IntVar(value=-1)
        for i in range(len(list)):
            r = Radiobutton(
                parent,
                text=list[i],
                variable=a,
                value=i,
                padx=10,
                font=("Arial", size),
                indicatoron=0,
                activebackground=self.colourHex,
                bg=self.colourHex,
                selectcolor=self.colourHex,
                foreground=white,
                activeforeground=white,
                width=width,
                justify="left",
                anchor="w",
            )
            if p == None:
                r.place(x=x, y=(y + (55 * i)))
            else:
                r.pack(anchor="w")
        return a

    def scrollable_frame(self, container, width, relheight, y, x):
        scroll_container = Frame(container, bg=self.colourHex)
        scroll_container.place(
            relx=x, rely=y, anchor="center", width=width, relheight=relheight
        )

        canvas = Canvas(
            scroll_container,
            bg=self.colourHex,
            highlightthickness=0,
            width=30,
            height=30,
        )
        scrollbar = Scrollbar(scroll_container, orient="vertical", command=canvas.yview)

        scrollable_frame = Frame(canvas, bg=self.colourHex)
        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        self.temporary_frame.append(canvas)
        self.temporary_frame.append(scrollable_frame)
        self.temporary_frame.append(scroll_container)

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return scrollable_frame


class StartPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)

        can = Canvas(self, width=400, height=400, bg=grey, highlightthickness=0)
        can.place(x=0, y=0)
        can.create_polygon(
            (0, 0, 300, 0, 0, 300), fill=charcoal_grey, outlineoffset=grey
        )

        can = Canvas(self, width=400, height=400, bg=grey, highlightthickness=0)
        can.place(x=800, y=400)
        can.create_polygon(
            (400, 100, 100, 400, 400, 400), fill=charcoal_grey, outlineoffset=grey
        )

        start_label = Label(
            self, text="Welcome to Quizzy!", font=("Arial", 50), bg=grey, fg=white
        )
        start_label.pack(pady=100)

        button = Button(
            self,
            text="Start",
            font=("Arial", 20),
            bg=white,
            width=10,
            height=20,
            activebackground=charcoal_grey,
            background=charcoal_grey,
            fg=white,
            command=lambda: App.show_frame("LoginPage"),
        )
        button.pack(pady=200)


class LoginPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.attempts = 0
        self.App = App

        App.label(self, "Login Page", 30, 500, 50)
        App.label(self, "Username", 30, 300, 200)
        self.username_entry = App.entry(self, 30, 300, 250)

        App.label(self, "Password", 30, 300, 350)
        self.password_entry = App.entry(self, 30, 300, 400)

        App.label(self, f"Number of attempts: {self.attempts}", 30, 300, 470)

        App.label(self, "Need an account? Click here to register", 30, 0, 750)

        # did not put this in a function as this button requires to be underlined
        register_button = Button(
            self,
            text="here",
            font=("Arial", 30, "underline"),
            bg=App.colourHex,
            width=3,
            fg=white,
            bd=0,
            activebackground=App.colourHex,
            activeforeground=white,
            command=lambda: App.show_frame("RegisterPage"),
        )
        register_button.place(x=431, y=738)
        self.error_label = App.label(self, "", 30, 300, 630)

        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)
        App.button(self, "Login", 20, 300, 550, self.login_check)

    def login_check(self):
        if self.username_entry.get() == "" or self.password_entry.get() == "":
            self.error_label.config(text="Error: Enter all details")
        else:
            l = login(
                self.username_entry.get().strip(),
                self.password_entry.get().strip(),
                self.attempts,
            )
            if l == None:
                self.error_label.config(text="Error: Username dosen't exist")
            elif l == False:
                self.error_label.config(text="Error: Wrong Password")
                self.attempts += 1
                self.App.label(
                    self, f"Number of attempts: {self.attempts}", 30, 300, 470
                )
            elif l == "Lock":
                self.password_entry.config(fg=red)
                self.password_entry.config(state=DISABLED)
                self.error_label.config(text="Attempt limit exceeded: Login locked ")

            elif l[0][0] == "student":
                self.App.account_type = "student"
                self.App.frames["StudentPage"].refresh_name(l[0][1])
                self.App.username = (
                    self.username_entry.get().strip()
                )  # prevent trail spacing
                self.App.show_frame("StudentPage")
                self.App.frames["StudentPage"].refresh_total(
                    get_score(self.App.username)
                )
                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")
            elif l[0][0] == "teacher":
                self.App.account_type = "teacher"
                self.App.frames["TeacherPage"].refresh_name(l[0][1])
                self.App.username = (
                    self.username_entry.get().strip()
                )  # prevent trail spacing
                self.App.show_frame("TeacherPage")
                self.username_entry.delete(0, "end")
                self.password_entry.delete(0, "end")


class RegisterPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App

        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)

        App.label(self, "Register Page", 30, 500, 50)

        App.label(self, "Name", 25, 250, 100)
        self.name_entry = App.entry(self, 25, 250, 150)

        App.label(self, "Age", 25, 250, 200)
        self.age_entry = App.entry(self, 25, 250, 250)

        App.label(self, "Username", 25, 250, 300)
        self.username_entry = App.entry(self, 25, 250, 350)

        App.label(self, "Password", 25, 250, 400)
        self.password_entry = App.entry(self, 25, 250, 450)

        App.button(self, "Register", 20, 250, 500, self.register_check)

        App.button(
            self, "Back to Login", 20, 20, 20, lambda: App.show_frame("LoginPage")
        )

        App.label(self, "Account Type", 25, 800, 100)
        self.options = ["Teacher", "Student"]
        self.account_type = App.radio_button(self, self.options, 800, 150, 25, 10)

        self.error_label = App.label(self, "", 30, 250, 600)

    def register_check(self):
        list = ["teacher", "student"]
        if (
            not self.name_entry.get().strip()
            or not self.age_entry.get().strip()
            or not self.username_entry.get().strip()
            or not self.password_entry.get().strip()
            or self.account_type.get() == -1
        ):
            self.error_label.config(text="Error: Insufficient information")
        elif len(self.password_entry.get()) < 8:
            self.error_label.config(text="Password too short")
        else:
            if (
                register(
                    self.name_entry.get(),
                    int(self.age_entry.get()),
                    self.username_entry.get(),
                    self.password_entry.get(),
                    list[self.account_type.get()],
                )
                is True
            ):
                self.username = self.username_entry.get()
                if self.account_type.get() == 0:
                    self.App.account_type = "teacher"
                    self.App.username = self.username_entry.get()
                    self.App.show_frame("TeacherPage")
                    self.App.frames["TeacherPage"].refresh_name(self.name_entry.get())
                else:
                    self.App.account_type = "student"
                    self.App.username = self.username_entry.get()
                    self.App.show_frame("StudentPage")
                    self.App.frames["StudentPage"].refresh_total(0)
                    self.App.frames["StudentPage"].refresh_name(self.name_entry.get())
            else:
                self.error_label.config(text="Error: Username already in use")

            self.App.name = self.name_entry.get()


class TeacherPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App
        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)
        self.welcome = App.label(
            self, "", 30, 350, 50
        )  # welcome label, text will be added using the method
        App.button(
            self, "Create Quiz", 30, 200, 200, lambda: App.show_frame("QuizMaker"), 10
        )
        App.button(
            self,
            "Edit Quiz",
            30,
            200,
            350,
            lambda: App.show_frame("EditPage").load_page(App.username),
            10,
        )
        App.button(
            self,
            "Assign Quiz",
            30,
            200,
            500,
            lambda: App.show_frame("AssignPage").load_page(),
            10,
        )  # creating buttons for each page
        App.button(
            self,
            "Reports",
            30,
            700,
            200,
            lambda: App.show_frame("ReportPage").load_page(App.account_type),
            10,
        )
        App.button(
            self,
            "Leaderboard",
            30,
            700,
            350,
            lambda: App.show_frame("LeaderboardPage").load_page(),
            10,
        )
        App.button(
            self,
            "Test Quiz",
            30,
            700,
            500,
            lambda: App.show_frame("QuizPage").load_page(),
            10,
        )
        App.button(self, "Logout", 20, 20, 20, lambda: App.show_frame("LoginPage"))

    def refresh_name(self, name):
        self.welcome.config(text=f"Welcome, {name}")  # adding text to welcome label


class StudentPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)
        self.score = App.label(self, "", 25, 20, 80)
        self.welcome = App.label(self, "", 30, 400, 50)
        # creating main buttons
        App.button(
            self,
            "Practice Quiz",
            30,
            200,
            200,
            lambda: App.show_frame("QuizPage").load_page(),
            12,
        )
        App.button(
            self,
            "Enter Code",
            30,
            200,
            500,
            lambda: App.show_frame("AssignmentPage"),
            12,
        )
        App.button(
            self,
            "View Reports",
            30,
            700,
            200,
            lambda: App.show_frame("ReportPage").load_page(App.account_type),
            12,
        )
        App.button(
            self,
            "Leaderboard",
            30,
            700,
            500,
            lambda: App.show_frame("LeaderboardPage").load_page(),
            12,
        )
        App.button(self, "Logout", 20, 20, 20, lambda: App.show_frame("LoginPage"))

    def refresh_name(self, name):
        # update welcome label to display name
        self.welcome.config(text=f"Welcome, {name}")

    def refresh_total(self, score):
        # update score
        self.score.config(text=f"Score: {score}")


class QuizPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App

        # allowing me to sperate my repeated labels and entrys so i can delete them and reuse them
        self.content = Frame(self, bg=App.colourHex)
        self.content.pack(fill=BOTH, expand=True)
        self.App.temporary_frame.append(self.content)
        self.content.lower()

        # creating scrollable frame
        self.scrollable_frame = App.scrollable_frame(self, 600, 0.65, 0.5, 0.5)

        # creating the widgets of the page
        App.label(self, "Select quiz", 30, 260, 80)
        App.button(self, "Back to Homepage", 20, 20, 20, lambda: self.homepage())
        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)

        App.button(
            self, "Start", 30, 200, 700, lambda: self.valdiate_select_input(), 10
        )
        # be careful of character of quiz title
        self.error_label = App.label(self, "", 30, 500, 720)

    def load_page(self):
        # extracting list of all quizzes
        self.quiz_list = num_quiz()
        self.quiz_title = self.App.radio_button(
            self.scrollable_frame, self.quiz_list, 0, 0, 25, 29, 0
        )

    def homepage(self):
        # destroying widgets from scroll frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        if self.App.account_type == "student":
            self.App.show_frame("StudentPage")
        elif self.App.account_type == "teacher":
            self.App.show_frame("TeacherPage")

    def valdiate_select_input(self):
        if self.quiz_title.get() == -1:
            self.error_label.config(text="Select a quiz")
        else:
            self.quiz_name = self.quiz_list[self.quiz_title.get()]
            self.quiz_start(access_questions(self.quiz_name), 0)

    def validate_answer_input(self, num, answers, question_list):
        # input validation for mcq and true false questions
        if self.type == "MCQ" or self.type == "TrueFalse":
            # checking radio button value
            if self.answer_option.get() == -1:
                self.App.label(self, "Select an answer", 30, 450, 720)
            else:
                self.check_answer(num, answers, question_list)
        # input validation for long answer
        elif self.type == "LongAnswer":
            # checking text box for any input
            if self.long_answer.get("1.0", "end-1c") == "":
                self.App.label(self, "Enter an answer", 30, 450, 720)
            else:
                self.check_answer(num, answers, question_list)
        else:
            # only short answer remains and it checks entry field
            if self.short_answer.get() == "":
                self.App.label(self, "Enter an answer", 30, 450, 720)
            else:
                self.check_answer(num, answers, question_list)

    def assignment(self, quiz_title):
        # being used by assign attempt page
        self.quiz_name = quiz_title
        self.quiz_start(access_questions(quiz_title), 0)

    def quiz_start(self, question_list, num):
        # starting the quiz so previous value are being reset
        if num == 0:
            self.App.current_score = 0
        self.content.tkraise()
        for widget in self.content.winfo_children():
            widget.destroy()
        # question list stores [[questions text,question_id,question type]]
        if num < len(question_list):
            answers = access_answers(question_list[num][1])
            answer_list = [row[0] for row in answers]
            self.type = question_list[num][2]
            # generating mcq question page
            if self.type == "MCQ":
                self.answer_option = self.App.radio_button(
                    self.content, answer_list, 200, 300, 25, 20
                )
            # generating truefalse question page
            elif self.type == "TrueFalse":
                self.answer_option = self.App.radio_button(
                    self.content, ["True", "False"], 200, 300, 25, 5
                )
            # generating long answer page
            elif self.type == "LongAnswer":
                self.long_answer = Text(
                    self.content,
                    width=40,
                    height=5,
                    fg=self.App.colourHex,
                    bg=white,
                    font=("Arial", 30),
                    wrap="word",
                )
                self.long_answer.place(x=100, y=250)
            # generating short answer page
            elif self.type == "ShortAnswer":
                self.short_answer = self.App.entry(self.content, 30, 100, 200, 15)

            # creating widgets common to all quiz types
            self.App.button(
                self.content, "Colour Selector", 20, 980, 30, self.App.set_colour
            )
            self.App.label(
                self.content, str(num + 1) + ". " + question_list[num][0], 30, 100, 100
            )
            self.App.button(
                self.content,
                "Confirm",
                30,
                200,
                700,
                lambda: self.validate_answer_input(num, answers, question_list),
            )
        else:
            # closing quiz page
            self.content.lower()
            # destroying widgets from scroll frame
            for widget in self.scrollable_frame.winfo_children():
                widget.destroy()
            # redirecting users their homepages
            if self.App.account_type == "student":
                self.App.show_frame("StudentPage")
                save_score(self.quiz_name, self.App.current_score, self.App.username)
                update_score(self.App.username)
                self.App.frames["StudentPage"].refresh_total(
                    get_score(self.App.username)
                )
            else:
                self.App.show_frame("TeacherPage")

    def check_answer(self, num, answers, question_list):
        # checking mcq page answers
        if self.type == "MCQ":
            # accessing the boolean element which indicates it is correct
            if answers[self.answer_option.get()][1] == 1:
                self.App.current_score += 1
        # checking tru flase page answer
        elif self.type == "TrueFalse":
            picked = ["True", "False"][self.answer_option.get()]
            # is selecting the user answer and treating their answer as index value
            if answers[0][0] == picked:
                self.App.current_score += 1
        # checking the long answer page
        elif self.type == "LongAnswer":
            # splitting the text text into words by using puncatation marks as separators
            words = re.split(r"[,\s;.]+", self.long_answer.get("1.0", "end-1c").strip())
            for i in range(len(words)):
                for a in range(len(answers)):
                    if words[i].lower() == answers[a][0].lower():
                        answers[a][0] = ""
                        self.App.current_score += 1
        # checking the short answer page
        elif self.type == "ShortAnswer":
            if self.short_answer.get().lower() == answers[0][0].lower():
                self.App.current_score += 1
        # redirecting to generate next question
        self.quiz_start(question_list, num + 1)


class QuizMaker(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App

        # allowing me to sperate my repeated labels and entrys so i can delete them and reuse them

        self.content = Frame(self, bg=App.colourHex)
        # putting in self.app so colour changer can access the widgets inside it
        self.App.temporary_frame.append(self.content)
        self.content.pack(fill=BOTH, expand=True)
        self.content.lower()

        # used to save answers and question so they can be saved together
        self.question_list = []
        self.answer_list = []
        self.mcq_options = []

        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)
        App.label(self, "Select the type of quiz", 30, 350, 50)
        # different quiz types
        App.button(self, "MCQ", 30, 200, 200, lambda: self.quiz_page_check("MCQ"), 12)
        App.button(
            self,
            "True&False",
            30,
            200,
            400,
            lambda: self.quiz_page_check("TrueFalse"),
            12,
        )
        App.button(
            self,
            "Short Questions",
            30,
            700,
            400,
            lambda: self.quiz_page_check("ShortAnswer"),
            12,
        )
        App.button(
            self,
            "Long Questions",
            30,
            700,
            200,
            lambda: self.quiz_page_check("LongAnswer"),
            12,
        )
        App.label(self, "Number of Questions", 30, 700, 550)
        App.label(self, "Enter Quiz Title", 30, 100, 550)
        # switches fram to teacher homepage
        App.button(
            self, "Back to Homepage", 20, 20, 20, lambda: App.show_frame("TeacherPage")
        )
        self.name = App.entry(self, 30, 100, 600, 20)
        # creating scale for number of questions
        self.scale = Scale(
            self,
            from_=5,
            to=25,
            orient=HORIZONTAL,
            length=400,
            font=("Arial", 30),
            tickinterval=5,
            fg=white,
            bg=self.App.colourHex,
        )
        self.scale.place(x=700, y=600)

    def quiz_page_check(self, quiz_type):
        self.quiz_maker_name = self.name.get()
        # used to track loop
        q_num, total_q_num = self.scale.get(), self.scale.get()
        error_label = self.App.label(self, "", 25, 100, 700)
        # checking label
        if self.quiz_maker_name == "":
            error_label.config(text="Please enter quiz title")
        elif len(self.quiz_maker_name) < 3:
            error_label.config(text="Title should be at least 3 character")
        else:
            self.quiz_construction(quiz_type, q_num, total_q_num, False)

    def clear(self):
        # destroying each widget in frame
        for widget in self.content.winfo_children():
            widget.destroy()

    def quiz_construction(self, quiz_type, q_num, total_q_num, edit):
        self.clear()
        self.content.tkraise()

        self.App.button(
            self.content, "Colour Selector", 20, 980, 30, self.App.set_colour
        )
        self.App.label(
            self.content, f"Enter Question {(total_q_num-q_num)+1}", 30, 100, 100
        )
        self.question = self.App.entry(self.content, 30, 100, 150, 25)
        if quiz_type == "MCQ":
            # creating mcq page
            self.App.label(self.content, "Option 1", 25, 100, 350)
            self.option_1 = self.App.entry(self.content, 25, 100, 400, 8)
            self.App.label(self.content, "Option 2", 25, 400, 350)
            self.option_2 = self.App.entry(self.content, 25, 400, 400, 8)
            self.App.label(self.content, "Option 3", 25, 700, 350)
            self.option_3 = self.App.entry(self.content, 25, 700, 400, 8)
            self.App.label(self.content, "Option 4", 25, 1000, 350)
            self.option_4 = self.App.entry(self.content, 25, 1000, 400, 8)
            self.App.label(self.content, "Enter correct option no.", 30, 700, 100)
            self.correct_option = self.App.entry(self.content, 30, 700, 150)
        elif quiz_type == "TrueFalse":
            # creating true false page
            self.App.label(self.content, "Correct answer:", 30, 100, 300)
            self.correct_option = self.App.radio_button(
                self.content, ["True", "False"], 100, 400, 30, 10
            )
        elif quiz_type == "ShortAnswer":
            # creating short answer page
            self.App.label(self.content, "Enter one word answer", 30, 100, 400)
            self.short_answer = self.App.entry(self.content, 30, 100, 500, 15)
        elif quiz_type == "LongAnswer":
            # creatin long answer page
            self.App.label(self.content, "Keyword 1", 25, 100, 350)
            self.key_1 = self.App.entry(self.content, 25, 100, 400, 8)
            self.App.label(self.content, "Keyword 2", 25, 400, 350)
            self.key_2 = self.App.entry(self.content, 25, 400, 400, 8)
            self.App.label(self.content, "Keyword 3", 25, 700, 350)
            self.key_3 = self.App.entry(self.content, 25, 700, 400, 8)
        # creating confirm button
        self.App.button(
            self.content,
            "Confirm",
            30,
            500,
            700,
            lambda: self.quiz_maker_check(quiz_type, q_num, total_q_num, edit),
        )

    def quiz_maker_check(self, type, q_num, total_q_num, edit):
        self.error_label = self.App.label(self.content, "", 30, 400, 600)
        if type == "MCQ":
            if (
                self.question.get() == ""
                or self.option_1.get() == ""
                or self.option_2.get() == ""
                or self.option_3.get() == ""
                or self.option_4.get() == ""
                or self.correct_option.get() == ""
            ):
                self.error_label.config(text="Fill in all spaces")
            else:
                try:
                    correct_option = int(self.correct_option.get())
                except ValueError:
                    self.error_label.config(
                        text="Correct option no. should be an integer"
                    )
                    return
                if correct_option < 5 and correct_option > 0:
                    self.question_list.append(self.question.get())
                    answer_text = [
                        self.option_1.get(),
                        self.option_2.get(),
                        self.option_3.get(),
                        self.option_4.get(),
                    ]
                    self.mcq_options.append(answer_text)
                    # save index no. of correct answer
                    self.answer_list.append(int(self.correct_option.get()))
                    self.save_question(type, q_num, total_q_num, edit)
                else:
                    self.error_label.config(text="Please enter a valid option number")

        elif type == "TrueFalse":
            if self.question.get() == "" or self.correct_option.get() == -1:
                self.App.label(self.content, "Provide all information", 30, 400, 600)
            else:
                self.question_list.append(self.question.get())
                list = ["True", "False"]
                self.answer_list.append(list[self.correct_option.get()])
                self.save_question(type, q_num, total_q_num, edit)

        elif type == "ShortAnswer":
            if self.question.get() == "" or self.short_answer.get() == "":
                self.App.label(self.content, "Fill in all spaces", 30, 400, 600)
            else:
                self.question_list.append(self.question.get())
                self.answer_list.append(self.short_answer.get())
                self.save_question(type, q_num, total_q_num, edit)

        elif type == "LongAnswer":
            if (
                self.question.get() == ""
                or self.key_1.get() == ""
                or self.key_2.get() == ""
                or self.key_3.get() == ""
            ):
                self.App.label(self.content, "Provide all information", 30, 400, 600)
            else:
                keywords = [self.key_1.get(), self.key_2.get(), self.key_3.get()]
                self.question_list.append(self.question.get())
                self.answer_list.append(keywords)
                self.save_question(type, q_num, total_q_num, edit)

    def save_question(self, quiztype, q_num, total_q_num, edit):
        # checking to see if all input is acquired
        if q_num > 1:
            self.quiz_construction(quiztype, q_num - 1, total_q_num, edit)
        else:
            # creating quiz, checking if edit mode
            if edit is not False:
                delete_quiz_data(self.App.username, edit)
            else:
                create_quiz(self.quiz_maker_name.strip(), self.App.username)

            for i in range(0, len(self.question_list)):
                question_id = save_question(
                    self.quiz_maker_name,
                    self.App.username,
                    quiztype,
                    self.question_list[i],
                )
                # saving mcq quetions
                if quiztype == "MCQ":
                    for a in range(0, 4):
                        if a + 1 == self.answer_list[i]:
                            save_answer(question_id, self.mcq_options[i][a].strip(), 1)
                        else:
                            save_answer(question_id, self.mcq_options[i][a].strip(), 0)

                # saving long answer questions
                elif quiztype == "LongAnswer":
                    for a in range(0, 3):
                        save_answer(question_id, self.answer_list[i][a].strip(), 1)

                # saving short answer and true false questions
                else:
                    save_answer(question_id, self.answer_list[i].strip(), 1)

            self.clear()
            self.content.lower()
            # reseting the temporary list so it can be used next time
            self.question_list = []
            self.answer_list = []
            self.mcq_options = []
            self.App.show_frame("TeacherPage")


class AssignPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App

        # creating temporary frame
        self.content = Frame(self, bg=App.colourHex)
        self.content.pack(fill=BOTH, expand=True)
        self.content.lower()
        self.App.temporary_frame.append(self.content)

        # creating scrollable area
        self.scrollable_frame = App.scrollable_frame(self, 600, 0.65, 0.5, 0.6)

        # creating widgets
        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)
        App.label(self, "Select quiz to assign", 30, 400, 50)
        App.label(self, "No. of days", 30, 20, 150)
        App.button(self, "Back to Homepage", 20, 20, 20, lambda: self.home())

        time_limit = App.entry(self, 30, 20, 200, 10)
        App.button(
            self,
            "Assign",
            30,
            400,
            700,
            lambda: self.generate_code(self.quiz_title.get(), time_limit.get()),
            0,
        )
        self.error_label = App.label(self, "", 30, 50, 600)

    def load_page(self):
        # extracting list of all quizzes
        self.quiz_list = num_quiz()
        self.quiz_title = self.App.radio_button(
            self.scrollable_frame, self.quiz_list, 100, 150, 25, 29, 2
        )

    def generate_code(self, quiz_title, time_limit):
        # presence check
        if quiz_title == -1 or time_limit == "":
            self.error_label.config(text="Enter all information")
        else:
            # confirming input has numeric values
            try:
                time_limit = int(time_limit)
            except ValueError:
                self.error_label.config(text="Enter a number")
                return
            self.content.tkraise()
            # saving data and getting code
            code = assignment(self.quiz_list[quiz_title], time_limit, self.App.username)
            # creating widgets
            self.App.label(self.content, f"Your Assignment Code: {code}", 40, 200, 200)
            self.App.button(
                self, "Colour Selector", 20, 980, 30, lambda: self.App.set_colour()
            )
            self.App.button(self, "Back to Homepage", 20, 20, 20, lambda: self.home())

    def home(self):
        # destroying widgets from scroll frame
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for widget in self.content.winfo_children():
            widget.destroy()
        self.content.lower()
        # redirecting to teacher homepage
        self.App.show_frame("TeacherPage")


class LeaderboardPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App

        # creating widgets
        App.button(self, "Colour Selector", 20, 980, 20, App.set_colour)
        App.button(self, "Back to Homepage", 20, 20, 20, lambda: self.home())
        App.label(self, "Leaderboard", 30, 500, 50)
        App.label(self, "Rank      Username      Score", 30, 380, 150)

        # scrollable area creation
        self.scrollable_frame = App.scrollable_frame(self, 500, 0.65, 0.6, 0.55)

    def load_page(self):
        # getting list of users rank
        leaderboard_list = leaderboard()

        # displaying leaderboard
        for i in range(len(leaderboard_list)):
            username = leaderboard_list[i][0]
            score = str(leaderboard_list[i][1])
            self.App.label(self.scrollable_frame, str(i + 1), 25, 0, 0).grid(
                row=i,
                column=0,
            )
            self.App.label(self.scrollable_frame, username, 25, 0, 0).grid(
                row=i, column=1, padx=120
            )
            self.App.label(self.scrollable_frame, score, 25, 0, 0).grid(
                row=i, column=2, padx=45
            )

    def home(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        # redirecting users
        if self.App.account_type == "student":
            self.App.show_frame("StudentPage")
        elif self.App.account_type == "teacher":
            self.App.show_frame("TeacherPage")


class AssignmentPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App
        # creating widgets for the page
        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)
        App.label(self, "Enter your 5 digit assignment code", 30, 300, 200)
        self.code = App.entry(self, 30, 300, 300, 25)
        App.button(self, "Start Assignment", 30, 400, 400, self.check)
        App.button(
            self,
            "Back to Homepage",
            20,
            20,
            20,
            lambda: self.App.show_frame("StudentPage"),
        )
        self.error_label = self.App.label(self, "", 30, 430, 500)

    def check(self):
        # creating label to be used
        # checking the code has all numeric values
        try:
            code = int(self.code.get())
        except ValueError:
            self.error_label.config(text="Enter a number")
            return
        # checking if code is five digits
        if len(str(code).strip()) != 5:
            self.error_label.config(text="Enter a 5 digit number")
        else:
            quiz_title = quiz_fetcher(self.code.get())
            # checking if it is a valid code
            if quiz_title is None:
                self.error_label.config(text="Code does not exist")
            # checking if the code is expired
            elif quiz_title == 0:
                self.error_label.config(text="Code has expired")
            else:
                self.code.delete(0, "end")
                self.App.show_frame("QuizPage").assignment(quiz_title)


class ReportPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App

        # create widgets
        App.button(self, "Colour Selector", 20, 980, 20, App.set_colour)
        App.button(self, "Back to Homepage", 20, 20, 20, lambda: self.home())
        self.title = App.label(self, "Select quiz to view its report", 30, 380, 80)

        # allowing me to sperate my repeated labels and entrys so i can delete them and reuse them
        self.content = Frame(self, bg=App.colourHex)
        self.content.pack(fill=BOTH, expand=True)
        self.App.temporary_frame.append(self.content)
        self.content.lower()

        # creating scrollable frame
        self.scroll_frame = App.scrollable_frame(self, 600, 0.55, 0.5, 0.55)

        App.button(self, "View", 30, 200, 700, lambda: self.valdiate_select_input(), 10)

    def load_page(self, type):
        # checking account type is student
        if type == "student":
            self.quiz_list = student_reports(self.App.username)[1]
            # checking if student has completed any quizes
            if len(self.quiz_list) == 0:
                self.title.configure(text="Complete quizzes to view records")
            self.quiz_title = self.App.radio_button(
                self.scroll_frame, self.quiz_list, 0, 0, 25, 29, 0
            )
        # if not student then it is teacher
        else:
            self.quiz_list = teacher_quizzes(self.App.username)[0]
            # checking if teacher has created quizzes
            if len(self.quiz_list) == 0:
                self.title.configure(text="Create quizzes to view its record")
            self.quiz_title = self.App.radio_button(
                self.scroll_frame, self.quiz_list, 0, 0, 25, 29, 0
            )

    def valdiate_select_input(self):
        # checking if a radio button is selected
        if self.quiz_title.get() == -1:
            self.App.label(self, "Select quiz", 30, 500, 700)
        else:
            # start next process
            self.report_generate(self.quiz_list[self.quiz_title.get()])

    def report_generate(self, quiz_title):
        self.content.tkraise()
        # generating widgets for consistency
        self.App.button(
            self.content, "Colour Selector", 20, 980, 20, self.App.set_colour
        )
        self.App.button(
            self.content, "Back to select page", 20, 20, 20, lambda: self.select()
        )

        # splitiing quiz
        quiz = quiz_title.split("by")

        # will be used to calcualte average score
        count = 0
        score = 0

        self.App.label(self.content, f"History of {quiz_title}", 30, 300, 80)

        if self.App.account_type == "student":
            # getting quiz attempt details
            user_log = student_reports(self.App.username)[0]
            scroll = self.App.scrollable_frame(self.content, 400, 0.55, 0.6, 0.55)
            self.App.label(self.content, "Score      Date of completion", 30, 400, 180)
            # generating score and date completed for each attempt
            for i in range(len(user_log)):
                if (
                    quiz[0].strip() == user_log[i][0].strip()
                    and quiz[1].strip() == user_log[i][3].strip()
                ):
                    self.App.label(scroll, user_log[i][1], 25, 0, 0).grid(
                        row=i,
                        column=0,
                    )
                    self.App.label(scroll, user_log[i][2], 25, 0, 0).grid(
                        row=i, column=1, padx=120
                    )
                    count += 1
                    score += user_log[i][1]
        else:
            self.App.label(
                self.content, "Username     Score      Date of completion", 30, 270, 180
            )
            scroll = self.App.scrollable_frame(self.content, 600, 0.55, 0.6, 0.55)
            # getting student attempt details
            data = teacher_quizzes(self.App.username)
            user_log = data[1]
            # generating score, username and date completed for each attempt
            for i in range(len(user_log)):
                if quiz[0].strip() == user_log[i][1].strip():
                    self.App.label(scroll, user_log[i][0], 25, 0, 0).grid(
                        row=i, column=0
                    )
                    self.App.label(scroll, user_log[i][2], 25, 0, 0).grid(
                        row=i, column=1, padx=140
                    )
                    self.App.label(scroll, user_log[i][3], 25, 0, 0).grid(
                        row=i, column=2
                    )
                    count += 1
                    score += user_log[i][2]
        # displaying average score
        if count != 0:
            self.App.label(
                self.content, f"Average Score: {score // count}", 25, 20, 140
            )
        else:
            self.App.label(self.content, "Average Score: 0", 25, 20, 140)

    def select(self):
        for widget in self.content.winfo_children():
            widget.destroy()
        self.content.lower()

    def home(self):
        # destroying widgets from scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # checking user account type to redirect
        if self.App.account_type == "student":
            self.App.show_frame("StudentPage")
        elif self.App.account_type == "teacher":
            self.App.show_frame("TeacherPage")


class EditPage(Frame):
    def __init__(self, window, App):
        super().__init__(window, bg=App.colourHex)
        self.App = App

        # interface widgets
        App.button(self, "Back to Homepage", 20, 20, 20, lambda: self.home())
        App.button(self, "Colour Selector", 20, 980, 30, App.set_colour)

        # creating scroll frame
        self.scroll_frame = App.scrollable_frame(self, 600, 0.55, 0.5, 0.55)

        App.label(self, "Select a quiz to edit", 30, 380, 80)
        App.button(self, "Edit", 30, 350, 700, lambda: self.valdiate_select_input(), 10)

    def load_page(self, username):
        # fetching quizzes created by teacher
        self.quiz_list = tquiz_list(username)
        # displaying quizzes
        self.quiz_title = self.App.radio_button(
            self.scroll_frame, self.quiz_list, 0, 0, 25, 29, 0
        )

    def valdiate_select_input(self):
        # checking if a radio button is selected
        if self.quiz_title.get() == -1:
            self.App.label(self, "Select a quiz", 30, 600, 700)
        else:
            # start next process
            quiz_title = self.quiz_list[self.quiz_title.get()]
            details = quiz_details(quiz_title, self.App.username)
            self.App.show_frame("QuizMaker").quiz_construction(
                details[1], int(details[0]), int(details[0]), quiz_title
            )

    def home(self):
        # destroying widgets from scroll frame
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
        # redirecting to teacher homepage
        self.App.show_frame("TeacherPage")


window = Tk()
window.title("Quizzy")
window.geometry("1200x800")
# dosen't allow the window to be resized manually
window.resizable(height=False, width=False)
app = App(window)
window.mainloop()
