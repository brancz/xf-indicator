from gi.repository import Gtk
from repository import Repository

class PreferencesWindow(Gtk.Window):

    def __init__(self, repositories, return_from_preferences_callback):
        self.return_from_preferences_callback = return_from_preferences_callback

        Gtk.Window.__init__(self, title="Preferences")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        self.superlistbox = Gtk.ListBox()
        self.superlistbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(self.superlistbox, True, True, 0)

        ###
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        self.listbox = Gtk.ListBox()
        self.listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        hbox.pack_start(self.listbox, True, True, 0)
        row.add(hbox)

        #only work on a copy of repositories until closing the preferences,
        #thus sumbmitting the change
        self.repositories = repositories.clone()
        self.repositories.add_all_to_listbox(self.listbox)

        self.superlistbox.add(row)

        ###
        self.add_add_repo_button()

        self.connect("delete-event", self.quit)

    def quit(self, a, b):
        self.return_from_preferences_callback(self.repositories)

    def add_add_repo_button(self):
        row = Gtk.ListBoxRow()
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=50)
        row.add(hbox)
        self.entry = Gtk.Entry(xalign=0)
        self.entry.connect("activate", self.add_repo)
        remove_button = Gtk.Button("Add")
        remove_button.connect("clicked", self.add_repo)
        hbox.pack_start(self.entry, True, True, 0)
        hbox.pack_start(remove_button, False, True, 0)

        self.superlistbox.add(row)

    def add_repo(self, widget):
        repo_entry_text = self.entry.get_text()
        if repo_entry_text != "":
            repo = Repository(repo_entry_text)
            repo.add_to_listbox(self.listbox, self.repositories.remove_from_listbox_callback)
            self.repositories.add_repository(repo)
            self.entry.set_text("")
