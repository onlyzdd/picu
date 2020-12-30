import os
import requests


class ImageUrl:
    """Path and delete-path of uploaded pictures"""
    def __init__(self, filename, url, delete):
        self.filename = filename
        self.url = url
        self.delete = delete

    def __str__(self):
        return self.filename + '\t' + self.url + '\t' + self.delete


class SmmsUtils:
    '''SM.MS uploader utils'''
    @staticmethod
    def upload(filepath):
        """Upload pictures"""
        uploadUrl = 'https://sm.ms/api/v2/upload'
        files = {
            'smfile': open(filepath, 'rb')
        }
        params = {
            'ssl': True
        }
        res = requests.post(uploadUrl, params=params, files=files).json()
        code = res['code']
        if code == "success":
            filename = res['data']['filename']
            url = res['data']['url']
            delete = res['data']['delete']
            img = ImageUrl(filename, url, delete)
            os.system('echo \'{}\' >> ~/.picu_history.log'.format(img))
            return [0, "Upload success", img]
        elif code == "error":
            msg = res['msg']
            return [-1, msg, None]
        else:
            return [-2, "Unknown error", None]
