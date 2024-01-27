from src.gui.searchInterface import SearchInterface

class GuiProvider():

    def search(map):
        items = list(map.keys())

        gui = SearchInterface(items)
        gui.mainloop()

        result = gui.getSelection()
        if not result:
            return None

        chosenItem = map[result['name']]
        return chosenItem
