"""
Module to represent the description of the configuration file.
"""
import json
from json import JSONDecodeError
import os
from source.exceptions import ConfigError


class VideosCollection(object):
    """Class to describe entity for video in the configuration file.
        i.e. in the configuration file video are described as:
            { "reference_video": "./test.mov",
            "compressed_video": ".//test.mp4",
            "threshold": 10
            }
            then VideosCollection instance has the attributes: reference_video, compressed_video, threshold
            and can be reached instance.reference_video, etc
    """

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)


class Config(object):
    """
    Class to represent the configuration file, this class supports json format
    """

    def __init__(self, file_name):
        """
        Parameterized constructor with file_name parameter to instantiate class instance
        :param file_name:   path to the configuration file to instantiate class instance
        :raise              FileNotFoundError or JSONDecodeError in the file was not found
                            or can not be read as json dictionary
        """
        self.file_name = file_name
        # names of mandatory entities (1st level) in the configuration file
        self._videos = "videos"
        self._report_folder = "report_folder"
        self._report_name = "report_name"
        self._reference_video = "reference_video"
        self._compressed_video = "compressed_video"
        try:
            with open(file_name, 'r') as config:
                self._data = json.load(config)
        except FileNotFoundError:
            raise FileNotFoundError("{} is not found or the path is incorrect".format(self.file_name))
        except JSONDecodeError as json_exc:
            raise JSONDecodeError("{} invalid json file".format(self.file_name), json_exc.doc, json_exc.pos)

    @property
    def videos(self) -> list:
        """
        Returns list with videos to work with, it's assumed that each video entity described as a dictionary
        :return:    list of entities with videos description
        :raise:     ConfigError is raised if video entity is not a dictionary or
                    video entity doesn't contain keys: self._reference_video, self._compressed_video
        """
        video_list = []
        if not self._data[self._videos]:
            raise ConfigError("no videos in the configuration file")
        if not isinstance(self._data[self._videos], list):
            self._data[self._videos] = list(self._data[self._videos])
        for item in self._data[self._videos]:
            if not isinstance(item, dict):
                raise ConfigError("parameters of the video shall be presented as dictionary")
            if self._reference_video not in item.keys() or self._compressed_video not in item.keys():
                raise ConfigError("reference or/and compressed is not found")
            video_list.append(VideosCollection(**item))
        return video_list

    @property
    def report_folder(self) -> str:
        """
        Returns folder name, which supposed to be used to save/process  reports or other artifacts
        :return:    Folder name specified in the configuration file otherwise the current working directory
        """
        if self._report_folder not in self._data or not os.path.isdir(self._data[self._report_folder]):
            self._data[self._report_folder] = os.getcwd()
        return self._data[self._report_folder]
