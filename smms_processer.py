import os
import time

import clipboard
import smms_uploader


CLIPBOARD_EXCEPTIONS = (
    clipboard.WriteFileError,
    clipboard.FileTypeUnsupportedError,
    clipboard.NotImageError
)


class ImgSizeError(Exception):
    def __init__(self):
        super(ImgSizeError, self).__init__('Figure size error!')


def process():
    try:
        img_path = clipboard.get_pasteboard_img_path()
    except CLIPBOARD_EXCEPTIONS as error:
        notice(str(error))
        return

    file_name = os.path.split(img_path)[-1]
    file_type = file_name.split('.')[-1]
    if file_type == 'tiff':
        new_img_path = '/tmp/{}.png'.format(int(time.time()))
        _convert_to_png(img_path, new_img_path)
        img_path = new_img_path
    try:
        tool = smms_uploader.SmmsUtils()
        upload_status, upload_msg, image = tool.upload(img_path)
        if upload_status == 0:
            img_uri = image.url
        else:
            notice('Upload failure:', upload_msg)
            return
        notice('Upload success!')
    except Exception as error:
        notice('Unknow error: {}'.format(str(error)))
        return
    write_to_pasteboard(img_uri)


def _convert_to_png(src_path, dest_path):
    os.system('sips -s format png {} --out {}'.format(src_path, dest_path))


def write_to_pasteboard(text):
    os.system('echo \'{}\' | pbcopy'.format(text))


def notice(msg, title='SM.MS'):
    os.system('osascript -e \'display notification "{}" with title "{}"\''.format(msg, title))


def main():
    process()


if __name__ == '__main__':
    main()
