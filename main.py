import json
import os

from kivy.app import App
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton


class PlaceButton(ToggleButton):
    place_name = StringProperty("")


class StartScreen(Screen):
    pass


class FareScreen(Screen):
    route_key = StringProperty("sm_to_sj")
    fare_type = StringProperty("regular")
    selected_start = StringProperty("")
    selected_end = StringProperty("")
    total_fare = StringProperty("0")
    commuter_count = StringProperty("0")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._places_data = self._load_places()
        self._fare_by_km = self._places_data["fare_by_km"]
        self._start_button = None
        self._end_button = None

    def on_pre_enter(self, *args):
        if not self.ids.places_grid.children:
            self.populate_places()
        self.update_fare_display()

    def _load_places(self):
        data_path = os.path.join(os.path.dirname(__file__), "data", "routes.json")
        with open(data_path, "r", encoding="utf-8") as handle:
            return json.load(handle)

    def set_route(self, route_key):
        if self.route_key == route_key:
            return
        self.route_key = route_key
        self.reset_selections()
        self.populate_places()

    def set_fare_type(self, fare_type):
        self.fare_type = fare_type
        self.update_fare_display()

    def reset_fare_type_selection(self, default=None):
        for key in ("fare_regular", "fare_student", "fare_senior", "fare_pwd"):
            if key in self.ids:
                self.ids[key].state = "normal"
        if default == "regular" and "fare_regular" in self.ids:
            self.ids["fare_regular"].state = "down"
            self.fare_type = "regular"
        else:
            self.fare_type = ""

    def populate_places(self):
        route_places = self._places_data["routes"][self.route_key]
        self.ids.places_grid.clear_widgets()

        for place in route_places:
            place_btn = PlaceButton(
                text=place["name"].upper(),
                place_name=place["name"],
            )
            place_btn.bind(on_release=self.select_place)
            self.ids.places_grid.add_widget(place_btn)

    def select_place(self, button):
        if not self.selected_start:
            self.selected_start = button.place_name
            self._start_button = button
            button.state = "down"
        elif not self.selected_end and button.place_name != self.selected_start:
            self.selected_end = button.place_name
            self._end_button = button
            button.state = "down"
        else:
            self.reset_selections(keep_totals=True)
            self.selected_start = button.place_name
            self._start_button = button
            button.state = "down"
        self.update_fare_display()

    def increment_count(self):
        self.ids.count_label.text = str(int(self.ids.count_label.text) + 1)
        self.update_fare_display()

    def decrement_count(self):
        current = int(self.ids.count_label.text)
        if current > 1:
            self.ids.count_label.text = str(current - 1)
            self.update_fare_display()

    def reset_selections(self, keep_totals=False):
        self.selected_start = ""
        self.selected_end = ""
        if not keep_totals:
            self.total_fare = "0"
            self.commuter_count = "0"
        self._start_button = None
        self._end_button = None
        for widget in list(self.ids.places_grid.children):
            if isinstance(widget, ToggleButton):
                widget.state = "normal"

    def reset_all(self):
        self.reset_selections()
        self.reset_fare_type_selection(default="regular")
        self.update_fare_display()

    def update_fare_display(self):
        if not self.selected_start or not self.selected_end:
            self.ids.fare_label.text = "Select two places"
            if self.commuter_count == "0":
                self.ids.total_label.text = ""
            else:
                self.ids.total_label.text = (
                    f"Total: {self.total_fare} pesos • {self.commuter_count} commuters"
                )
            return

        if not self.fare_type:
            self.ids.fare_label.text = "Select fare type"
            return

        km_distance = self._get_distance_km(self.selected_start, self.selected_end)
        base_fare = self._get_base_fare(km_distance)
        fare = self._apply_discount(base_fare)
        self.ids.fare_label.text = (
            f"{fare} pesos • {km_distance} km • {self.fare_type.upper()}"
        )
        running_total = int(self.total_fare)
        if running_total:
            self.ids.total_label.text = (
                f"Total: {running_total} pesos • {self.commuter_count} commuters"
            )
        else:
            self.ids.total_label.text = ""

    def add_commuter_fare(self):
        if not self.selected_start or not self.selected_end:
            self.ids.fare_label.text = "Select two places"
            return

        if not self.fare_type:
            self.ids.fare_label.text = "Select fare type"
            return

        km_distance = self._get_distance_km(self.selected_start, self.selected_end)
        base_fare = self._get_base_fare(km_distance)
        fare = self._apply_discount(base_fare)

        self.total_fare = str(int(self.total_fare) + fare)
        self.commuter_count = str(int(self.commuter_count) + 1)
        self.ids.total_label.text = (
            f"Total: {self.total_fare} pesos • {self.commuter_count} commuters"
        )

        # Keep start selected for the next commuter, clear end only.
        self.selected_end = ""
        if self._end_button is not None:
            self._end_button.state = "normal"
            self._end_button = None

        self.reset_fare_type_selection(default=None)
        self.update_fare_display()

    def calculate_total(self):
        if not self.selected_start or not self.selected_end:
            if int(self.total_fare) > 0:
                self.ids.total_label.text = (
                    f"Total: {self.total_fare} pesos • {self.commuter_count} commuters"
                )
            else:
                self.ids.fare_label.text = "Select two places"
            return

        if not self.fare_type:
            self.ids.fare_label.text = "Select fare type"
            return

        km_distance = self._get_distance_km(self.selected_start, self.selected_end)
        base_fare = self._get_base_fare(km_distance)
        fare = self._apply_discount(base_fare)

        running_total = int(self.total_fare)
        combined_total = running_total + fare
        combined_count = int(self.commuter_count) + 1
        self.ids.total_label.text = (
            f"Total: {combined_total} pesos • {combined_count} commuters"
        )

    def _get_distance_km(self, start, end):
        km_map = {
            item["name"]: item["km"]
            for item in self._places_data["routes"][self.route_key]
        }
        return abs(km_map[start] - km_map[end])

    def _get_base_fare(self, km_distance):
        key = str(km_distance)
        if key in self._fare_by_km:
            return self._fare_by_km[key]
        if km_distance <= 4:
            return 13
        return 13 + (km_distance - 4)

    def _apply_discount(self, base_fare):
        if self.fare_type == "regular":
            return base_fare
        return max(11, base_fare - 2)


class RootManager(ScreenManager):
    pass


class JeepneyFareApp(App):
    def build(self):
        return Builder.load_file("jeepney.kv")

    def animate_press(self, widget):
        Animation.cancel_all(widget, "opacity")
        (Animation(opacity=0.85, duration=0.05) + Animation(opacity=1, duration=0.1)).start(
            widget
        )


if __name__ == "__main__":
    JeepneyFareApp().run()
