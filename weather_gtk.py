import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
import weather


class WeatherInterface(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Stay Dry")
        self.set_border_width(10)
        self.set_icon_name("weather-clear")

        box_outer = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box_outer)

        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        box_outer.pack_start(listbox, True, True, 0)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        row.add(hbox)
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        hbox.pack_start(vbox, True, True, 0)

        label1 = Gtk.Label("Where are you located?:", xalign=0)
        vbox.pack_start(label1, True, True, 0)

        self.entry = Gtk.SearchEntry()
        self.entry.set_placeholder_text("Where are you?")
        icon_name = "system-search-symbolic"
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, icon_name)
        # self.entry.connect("search-changed", self.on_search_clicked)
        vbox.pack_start(self.entry, True, True, 0)

        searchButton = Gtk.Button.new_with_mnemonic("_Search")
        searchButton.connect("clicked", self.on_search_clicked)
        hbox.pack_start(searchButton, True, True, 0)

        self.label2 = Gtk.Label("", xalign=0)
        vbox.pack_start(self.label2, True, True, 0)

        listbox.add(row)

    def on_search_clicked(self, button):
        city = self.entry.get_text()
        # TODO: this should be added to the UI
        searchTerm = [city, 7, 8, 15, 16]

        if city:
            self.result = weather.WeatherModel(searchTerm).fetchWeather()
            if self.result > 0:
                self.label2.set_text(str(self.result) + "mm of rain expected tomorrow!")
                icon_name = "weather-showers-symbolic"
            else:
                self.label2.set_text("No rain in tomorrow!")
                icon_name = "weather-clear-symbolic"
        else:
            self.label2.set_text("Location not set")
        self.entry.set_icon_from_icon_name(Gtk.EntryIconPosition.PRIMARY, icon_name)


class WeatherContainer(Gtk.ListBoxRow):

    def __init__(self, data):
        super(Gtk.ListBoxRow).self.__init__()
        self.data = data
        self.add(Gtk.Label(data))


win = WeatherInterface()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
