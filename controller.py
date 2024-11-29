from UI import View
import event_handler as event


class Controller:
    view = None

    def add_view(self, view: View):
        self.view = view

    def on_exit(self):
        event.handle_exit(self.view)

    @staticmethod
    def on_entry_click(textfield_string, textfield):
        event.handle_entry_click(textfield_string, textfield)

    @staticmethod
    def on_focus_out(textfield_string, textfield):
        event.handle_focus_out(textfield_string, textfield)

    def on_player_search(self):
        event.handle_player_search(self.view)

    def on_second_player_search(self):
        event.handle_second_player_search(self.view)

    def on_match_search(self):
        event.handle_match_search(self.view)

    def on_hero_search(self):
        event.handle_hero_search(self.view)

    def on_tab_changed(self):
        event.handle_tab_change(self.view)


def main():
    controller = Controller()
    view = View(controller)
    controller.add_view(view)
    view.run()


if __name__ == "__main__":
    main()
