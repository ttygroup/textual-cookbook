"""This file demonstrates how to use the `select_node` method
of the Tree widget to programmatically select a node. It is not
super obvious how to use it from the documentation. The method takes
a `TreeNode` object as its argument. However, there is no obvious
way to get the desired node from the Tree. This means you have to
save a reference to any node that you might want to programmatically
select, at the time the node is created and added to the tree.

Recipe by Edward Jazzhands"""

import sys
from textual.app import App, ComposeResult
from textual.widgets import Tree, Button


class TextualApp(App[None]):

    def compose(self) -> ComposeResult:
        tree: Tree[str] = Tree("Dune")
        tree.root.expand()
        self.characters = tree.root.add("Characters", expand=True)
        self.characters.add_leaf("Paul")
        self.characters.add_leaf("Jessica")
        self.characters.add_leaf("Chani")
        yield tree
        yield Button("Select Characters Node")
        
    def on_button_pressed(self):
        tree: Tree[str] = self.query_one(Tree)
        tree.select_node(self.characters)


if __name__ == "__main__":
    app = TextualApp()
    app.run()
    sys.exit(app.return_code)