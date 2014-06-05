from gi.repository import Gtk
from repository import Repository

class PreferencesWindow(Gtk.Window):

    def __init__(self, repositories, return_from_preferences_callback):
        Gtk.Window.__init__(self, title="Preferences")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(self.listbox, True, True, 0)

        self.repositories = repositories
        self.repositories.add_all_to_listbox(self.listbox)

        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.entry = Gtk.Entry(xalign=0)
        remove_button = Gtk.Button("Add")
        remove_button.connect("clicked", self.add_repo_clicked)
        remove_button.connect("enter", self.add_repo_clicked)
        hbox.pack_start(self.entry, True, True, 0)
        hbox.pack_start(remove_button, False, True, 0)

        self.listbox.add(row)

        self.connect("delete-event", return_from_preferences_callback)

    def add_repo_clicked(self, widget):
        repo = Repository(self.entry.get_text())
        repo.add_to_listbox(self.listbox)
        self.repositories.add_repository(repo)
        self.entry.set_text("")
