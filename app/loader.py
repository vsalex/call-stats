import json
from os import listdir, rename
from os.path import isfile, isdir, join, getctime
from abc import ABCMeta, abstractmethod

from app.models import Call, Duration


class AsyncQueue(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def anync_load_call(self):
        """Abstract async method for calls loading"""

    @abstractmethod
    def anync_load_duration(self):
        """Abstract async method for duration loading"""


class Loader(object):
    """Loads json data from input dirs - one for calls and one for duration"""

    @staticmethod
    def _load_file(filename, _class):
        """
        Create from concrete json file Call or Duration object depends on
        _class.

        :param filename: <str> json input filename.
        :param _class: <type> Call or Duration class.
        :return: <object> Call or Duration.
        """

        with open(filename, 'r') as f:
            try:
                json_data = json.load(f)
            except ValueError:
                # I think in production here should be some logging
                raise ValueError("Error! Can't load json file %s!" % filename)

            try:
                obj = _class(**json_data)
            except TypeError as e:
                raise TypeError("Error during parsing json into Call or "
                                "Duration object: %s!" % e)

            if obj.errors:
                raise ValueError(
                    "There are some errors in %s object: %s!" %
                    (_class.__name__, obj.errors))

        # Rename file for now, in production we shall delete it
        rename(filename, "%s.ok" % filename)

        return obj

    def _get_files(self, path, _class):
        """
        Makes from json input data Call and Duration objects list and return
        it.

        :param path: <str> path to input directory for concrete type of data.
        :param _class: <object> Call or Duration object.
        :return: <list> of all Call and Duration objects.
        """

        if not isdir(path):
            raise FileNotFoundError("Can't open directory %s!" % path)

        files = [join(path, f) for f in listdir(path) if
                 isfile(join(path, f)) and join(path, f).endswith(".json")]

        # Sort files by ctime
        files = sorted(files, key=getctime)

        files_list = []

        for filename in files:
            try:
                new_obj = self._load_file(filename, _class)
            except (ValueError, PermissionError, TypeError) as e:
                # I think in production here should be some logging
                print(e)
                # And we must go to next file
                continue

            files_list.append(new_obj)

        return files_list

    def load(self):
        """
        Loads call and duration files from input dirs.

        :returns <list> of all Call and Duration objects.
        """

        all_list = []

        all_list.extend(self._get_files(join('input', 'call'), Call))
        all_list.extend(self._get_files(join('input', 'duration'), Duration))

        return all_list
