import base64
from datetime import datetime

from textual.app import App, ComposeResult
from textual.screen import Screen
from textual.widgets import Header, Footer, Input, Button, Label, Static
from textual.containers import Vertical, Horizontal, VerticalScroll

from db import Database, ShopEntryTypes
from graphify import show_graph

db = Database("database.db")

class ShopEntryScreen(Screen):
    def __init__(self, product_id) -> None:
        super().__init__()
        self.product_id = product_id
        self.result = db.getInfoForShopEntry(self.product_id)
        self.price_history = db.getPriceHistoryForShopEntry(self.product_id)
    def compose(self) -> ComposeResult:
        from_date = datetime.strptime(self.price_history[0]["date"], "%Y%m%d").strftime("%d-%m-%Y")
        to_date = datetime.strptime(self.price_history[-1]["date"], "%Y%m%d").strftime("%d-%m-%Y")
        yield Label(f"""
            Name: {self.result["name"]}
            Price: {self.result["price"]}
            Additional Info {self.result["additional_info"]}
            Type: {self.result["type"]}
            History Data from: {from_date} to {to_date}
            Price Entries: {len(self.price_history)}
        """)
        yield Button("Back",id="back")
        yield Button("Show History Graph",id="history_graph")
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "back":
            self.app.pop_screen()
        elif event.button.id == "history_graph":
            show_graph(self.price_history,self.result["type"])

class SearchScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Input(placeholder="Enter search query", id="search_input")
        yield Button("Search", id="search_button")
        yield Label("Search Results:", id="results_label")
        yield VerticalScroll(id="results_display")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_button":
            self.perform_search()
        elif event.button.id.startswith("result_"):
            product_id = event.button.id.split("_")[1]
            self.app.push_screen(ShopEntryScreen(product_id))
    def perform_search(self):
        search_input = self.query_one("#search_input", Input).value
        results = db.searchShopEntry(search_input)
        results_display = self.query_one("#results_display", VerticalScroll)
        results_display.remove_children()
        for result in results:
            extension = ""
            type = result["type"]
            if type == str(ShopEntryTypes.GRAMM):
                extension = "g"
            elif type == str(ShopEntryTypes.LITER):
                extension = "l"
            elif type == str(ShopEntryTypes.STUECK):
                extension = " Stueck"
            elif type == str(ShopEntryTypes.METER):
                extension = "m"
            elif type == str(ShopEntryTypes.KISTE):
                extension = " Kisten"
            result_button = Button(result['name'] + " " + result['additional_info'] + extension, id=f"result_{result['product_link'].split("/")[-1]}")
            results_display.mount(result_button)
    def on_mount(self) -> None:
        self.set_interval(0.1, self.update_results_display)
    def update_results_display(self) -> None:
        self.query_one("#results_display", VerticalScroll).refresh()
    def display_product_details(self, product_id):
        self.notify(f"Product: {product_id}")


class ShopAnalyzerApp(App):
    CSS = """
    Screen {
        align: center middle;
    }
    Static, Input, Button {
        margin: 1;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Label("Main Menu")
        yield Button("Go to Search", id="search_screen_button")
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search_screen_button":
            self.push_screen(SearchScreen())

if __name__ == "__main__":
    ShopAnalyzerApp().run()