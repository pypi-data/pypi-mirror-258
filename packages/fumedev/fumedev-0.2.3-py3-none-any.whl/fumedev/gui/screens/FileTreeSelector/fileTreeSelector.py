from textual.app import App, ComposeResult
from textual.widgets import Static, Label, Button, DirectoryTree, Footer
from textual.containers import Container, ScrollableContainer
from textual.screen import Screen

class FileCardRemoveButton(Static):
    def __init__(self, removeAction):
        super().__init__()
        self.removeAction = removeAction

    def on_click(self):
        self.removeAction()

    def compose(self) -> ComposeResult:
        yield Container(Label('X'), id="fileCardRemove")

class FileCard(Static):
    def __init__(self, file_path):
        super().__init__() 
        self.file_path = file_path

    def remove_file_card(self):
        self.remove()

    def compose(self) -> ComposeResult:
        yield Container(Label(self.file_path, id="fileCardLabel"), FileCardRemoveButton(removeAction=self.remove_file_card), id="fileCard")

class SelectedFiles(Static):
    def compose(self) -> ComposeResult:
        yield ScrollableContainer(Label("Selected Files", id="title"), id="selectedFilesScroll")

class FileTreeSelector(Screen[list]):

    CSS_PATH = "./fileTreeSelector.tcss"

    BINDINGS = [
        ("d", "done", "Done"),
        ("x", "exit", "Exit"),
    ]

    def action_done(self):
        self.dismiss(self.selected_files)
    
    def action_exit(self):
        self.dismiss([])

    def on_directory_tree_file_selected(self, node):
        file_path = str(node.path)
        file_name = node.path.name
        if not (file_path in self.selected_files):
            self.selected_files.append(file_path)
            new_file_card = FileCard(file_name)
            self.query_one("#selectedFilesScroll").mount(new_file_card)
            new_file_card.scroll_visible()

    def compose(self) -> ComposeResult:
        self.selected_files = []
        yield Container(DirectoryTree("./"), SelectedFiles(id="selectedFiles"), id="container")
        yield Footer()