import os
import time

from AppKit import (
    NSPasteboard, NSFilenamesPboardType, NSPasteboardTypePNG,
    NSPasteboardTypeTIFF, NSPasteboardTypeString
)

class WriteFileError(Exception):
    def __init__(self, file_type):
        super(WriteFileError, self).__init__(
            'Write file error!'.format(file_type))


class FileTypeUnsupportedError(Exception):
    def __init__(self, file_type):
        super(FileTypeUnsupportedError, self).__init__(
            'Unsupported file type: {}!'.format(file_type))


class NotImageError(Exception):
    def __init__(self):
        super(NotImageError, self).__init__(
            'No image found!')


ALLOW_FILE_TYPES = ('png', 'jpeg', 'jpg', 'gif', 'tiff')

TYPE_MAP = {
    'png': NSPasteboardTypePNG,
    'tiff': NSPasteboardTypeTIFF,
}

def get_pasteboard_file_path():
    pasteboard = NSPasteboard.generalPasteboard()
    data_type = pasteboard.types()
    if NSFilenamesPboardType in data_type:
        file_path = pasteboard.propertyListForType_(NSFilenamesPboardType)[0]
        return file_path
    now = int(time.time())
    for file_type, pastedboard_file_type in TYPE_MAP.items():
        if pastedboard_file_type not in data_type:
            continue
        filename = '{}.{}'.format(now, file_type)
        file_path = '/tmp/%s' % filename
        data = pasteboard.dataForType_(pastedboard_file_type)
        ret = data.writeToFile_atomically_(file_path, False)
        if not ret:
            raise WriteFileError(file_type)
        return file_path


def get_pasteboard_img_path():
    file_path = get_pasteboard_file_path()
    if not file_path:
        raise NotImageError()
    file_name = os.path.split(file_path)[-1]
    file_type = file_name.split('.')[-1]
    if file_type not in ALLOW_FILE_TYPES:
        raise FileTypeUnsupportedError(file_type)
    return file_path
