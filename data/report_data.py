from pprint import pprint


class Report(object):
    # all_potions = []

    def __init__(self):
        self.report_data: dict[str, str] = {}
        # Report.all_potions.append(self)
        # pprint(f"Report all_potions {Report.all_potions}")

    def _print(self):
        pprint(self._report_data)

    @property
    def report_data(self):
        return self._report_data

    @report_data.setter
    def report_data(self, value):
        self._report_data = value
        self._print()

    def __getattr__(self, attr):
        return getattr(self.report_data, attr)

    # def __setattr__(self, attr, val):
    #     if attr == 'report_data':
    #         super(Report, self).__setattr__('report_data', val)
    #         pprint(f"установлен атрибут __setattr__ {attr}")
    #     else:
    #         setattr(self._wrapped, 'old_' + attr, getattr(self._wrapped, attr))
    #         setattr(self._wrapped, attr, val)
    #         pprint(f"установлен атрибут __setattr__ {attr}")


# import collections
#
# class Report(object):
#     all_potions = []
#
#     def __init__(self):
#         self.report_data: dict[str, str] = {}
#         Report.all_potions.append(self)
#         pprint(f"Report all_potions {Report.all_potions}")
#
#
#     def __getattribute__(self, name):
#         attr = object.__getattribute__(self, name)
#         if attr == {}:
#             return {}
#         if isinstance(attr, collections.MutableSequence):
#             attr = TrackableSequence(self, attr)
#         if isinstance(attr, collections.MutableMapping):
#             attr = TrackableMapping(self, attr)
#         return attr
#
#     def __setattr__(self, name, value):
#         object.__setattr__(self, name, value)
#         pprint(f"установлен атрибут __setattr__ name {name} value {value}")
#         # add change tracking
#
#
# class TrackableSequence(collections.MutableSequence):
#     def __init__(self, tracker, trackee):
#         self.tracker = tracker
#         self.trackee = trackee
#
#     # override all MutableSequence's abstract methods
#     # override the the mutator abstract methods to include change tracking
#
#
# class TrackableMapping(collections.MutableMapping):
#     def __init__(self, tracker, trackee):
#         self.tracker = tracker
#         self.trackee = trackee
#
#     # override all MutableMapping's abstract methods
#     # override the the mutator abstract methods to include change tracking


report_data = Report().report_data
