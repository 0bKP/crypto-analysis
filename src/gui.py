import tkinter as tk

bgColor = "#01000A"
labelBgColor = "#03010F"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1440x1024+250+20")
        self.configure(bg=bgColor)
        #self.overrideredirect(True)
        self.resizable(False, False)

        # Logo bar
        self.logo_bar = tk.Frame(background=bgColor, borderwidth=2, highlightbackground="red",
                                 highlightthickness=2, height=100)
        self.logo_bar.pack(side="top", fill="x")
        self.logo_bar.pack_propagate(False)

        # Nav bar
        self.nav_bar = tk.Frame(background=bgColor, width=70, highlightbackground="blue", highlightthickness=2)
        self.nav_bar.pack(side="left", fill="y", padx=5, pady=5)
        self.nav_bar.pack_propagate(False)

        # Main screen
        self.main_screen = tk.Frame(background=labelBgColor, width=220, highlightbackground="yellow", highlightthickness=2)
        self.main_screen.pack(expand=True, fill="both", padx=5, pady=5)
        self.main_screen.pack_propagate(False)

        self.exit = tk.Button(self.main_screen, text='X', command=self.destroy)
        self.exit.pack(side="right")


if __name__ == '__main__':
    app = App()
    app.mainloop()
