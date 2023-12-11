from tkinter import *
from dataclasses import dataclass

@dataclass
class ContextRow:
    element: any
    data: object

class SearchInterface(Tk):
    def __init__(self, context):
        super().__init__()

        # Initialize main components
        self.initWindow()
        self.frame = self.initFrame()
        self.container = self.initContainer()
        self.input = self.initInput()

        self.filter = None
        self.context = context
        self.renderedContext = []
        self.renderedSelection = None
        self.renderedSelectionIndex = None

        # Render initial texts
        self.renderContext()

        # Render initial selection
        self.renderSelection()


    def initWindow(self):
        self.title('Acrux')
        self.overrideredirect(True)

        # Center the main window relevant to screen size
        screenWidth = self.winfo_screenwidth()
        screenHeight = self.winfo_screenheight()

        windowWidth = 800
        windowHeight = 500

        x = (screenWidth / 2) - (windowWidth / 2)
        y = ((screenHeight / 2) - (windowHeight / 2)) * 0.70 # % of screen height

        self.geometry('%dx%d+%d+%d' % (windowWidth, windowHeight, x, y))
        self.maxsize(windowWidth, windowHeight)
        self.configure(
            background="#FBFAF5"
        )

        self.bind('<KeyPress>', self.handleKeyEvent)
        self.bind('<FocusOut>', self.handleFocusEvent)

    def initFrame(self):
        frame = Frame(self)
        frame.configure(
            background="purple",
            borderwidth=1,
            height=500
        )
        frame.pack(fill="both", expand=True)
        return frame

    def initContainer(self):
        container = Frame(self.frame)
        container.configure(
            background="black",
            borderwidth=10
        )
        container.pack(fill="both", expand=True)
        return container

    def initInput(self):
        inputFrame = Frame(self.container)
        inputFrame.configure(
            background="black",
            pady=6,
        )

        input = Entry(inputFrame)
        input.configure(
            background="black",
            fg="#FBFAF5",
            font="Consolas 15",
            relief="solid",
            insertbackground="#FBFAF5",
            insertwidth=1,
            insertborderwidth=1,
            highlightthickness=1,
            highlightcolor="purple",
            highlightbackground="purple",
        )
        input.focus_set()
        input.bind('<KeyRelease>', self.renderContext)
        input.pack(fill="both")

        inputFrame.pack(fill="x")
        return input

    def handleFocusEvent(self, event):
        self.destroy()

    def handleKeyEvent(self, event):
        key = event.keysym
        if key == None:
            return

        currentIndex = self.renderedSelectionIndex

        if key == "Down":
            self.renderedSelectionIndex = min(
                14, len(self.renderedContext) - 1, self.renderedSelectionIndex + 1
            )

        if key == "Up":
            self.renderedSelectionIndex = max(
                0, self.renderedSelectionIndex - 1
            )

        if key == "Escape":
            self.destroy()

        if key == "Return":
            self.handleSelectionEvent()

        # Only call render if index changed
        if self.renderedSelectionIndex != currentIndex:
            self.renderSelection()

    def handleSelectionEvent(self):
        print(self.renderedSelection['data'])
        self.destroy()


    def renderContext(self, *args):
        # Don't render changes if none happen
        filter = self.input.get()
        if filter == self.filter and self.filter != None:
            return

        self.filter = filter

        # Find matching text based on input value
        filteredContext = [
            str for str in self.context
            if str.capitalize().startswith((self.filter).capitalize())
        ]

        # Render new frames
        renderedContext = []
        for str in filteredContext:
            textFrame = Frame(self.container)
            textFrame.configure(
                background="black",
                pady=2
            )

            name = Label(textFrame, text=str)
            name.pack(side="left")
            name.configure(
                background="black",
                fg="#FBFAF5",
                font="Consolas 12"
            )

            # Render Right label
            #info = Label(textFrame, text=str)
            #info.pack(side="right")
            #info.configure(
            #    background="black",
            #    fg="#FBFAF5",
            #    font="Consolas 12"
            #)

            textFrame.pack(fill="x")

            row: ContextRow = {
                "element": textFrame,
                "data": {
                    "name": str
                }
            }

            renderedContext.append(row)

        # Clear already rendered text
        for text in self.renderedContext:
            text['element'].destroy()

        self.renderedContext = renderedContext

        self.renderedSelectionIndex = 0
        self.renderSelection()

    def renderSelection(self):
        try:
            if self.renderedSelection != None:
                self.renderedSelection['element'].configure(background='black')
                for child in self.renderedSelection['element'].winfo_children():
                    child.configure(
                        fg='#FBFAF5'
                    )
        except:
            self.renderedSelection = None

        try:
            selection = self.renderedContext[
                self.renderedSelectionIndex
            ]

            for child in selection['element'].winfo_children():
                child.configure(
                    fg='purple'
                )

            self.renderedSelection = selection
        except:
            return


if __name__ == "__main__":
    texts = [
        "AAAAAAAA",
        "BBBBBBBB",
        "CCCCCCCC",
        "DDDDDDDD",
        "EEEEEEEE",
        "FFFFFFFF",
        "GGGGGGGG",
        "HHHHHHHH",
        "IIIIIIII",
        "JJJJJJJJ",
        "KKKKKKKK",
        "LLLLLLLL",
        "MMMMMMMM",
        "NNNNNNNN",
        "A2AAAAAAA",
        "B2BBBBBBB",
        "C2CCCCCCC",
        "D2DDDDDDD",
        "E2EEEEEEE",
        "F2FFFFFFF",
        "G2GGGGGGG",
        "H2HHHHHHH",
        "I2IIIIIII",
        "J2JJJJJJJ",
        "K2KKKKKKK",
        "L2LLLLLLL",
        "M2MMMMMMM",
        "N2NNNNNNN",
    ]

    app = SearchInterface(texts)
    app.mainloop()
