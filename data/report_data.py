from pprint import pprint


class Report(object):
    # all_potions = []

    def __new__(cls, *args, **kwargs):
        print(f"Hello from {Report.__new__}")
        return super().__new__(cls)

    def __init__(self):
        self.report_data: dict[str, str] = {}

    def _print(self):
        pprint(self._report_data)

    @property
    def report_data(self):
        return self._report_data

    @report_data.setter
    def report_data(self, value):
        self._report_data = value
        if value == {}:
            return
        self._print()


report_data = Report().report_data
user_data = Report().report_data
global_reg_form = Report().report_data
