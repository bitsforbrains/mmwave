import logging
import os
from time import time


class FileWriter(object):

    def __init__(self, output_filename='output.bin', overwrite=False,):
        self._logger = logging.getLogger(__name__)
        self._output_filename = output_filename
        self._overwrite = overwrite
        self._initialized = False

    def receive(self, data):
        if self._initialized is False:
            self._initialized = True
            if os.path.isfile(self.output_filename) and not self.overwrite:
                file_path, file_name = os.path.split(self.output_filename)
                file_base, file_ext = os.path.splitext(file_name)
                self.output_filename = os.path.join(file_path, '{0}-{1}{2}'.format(file_base, int(time()), file_ext))
            with open(self.output_filename, 'wb') as out_file:
                out_file.write(data)
        else:
            with open(self.output_filename, 'ab') as out_file:
                out_file.write(data)

    @property
    def output_filename(self):
        return self._output_filename

    @output_filename.setter
    def output_filename(self, value):
        file_path, file_name = os.path.split(value)
        self._output_filename = value
        if file_path is not '':
            if not os.path.exists(file_path):
                raise ValueError('Error setting output filename (path does not exist!)')
                self._output_filename = value

    @property
    def overwrite(self):
        return self._overwrite

    @overwrite.setter
    def overwrite(self, value):
        if value is not True or value is not False:
            raise ValueError('Error setting overwrite property (must be True or False)')
        self._overwrite = value
