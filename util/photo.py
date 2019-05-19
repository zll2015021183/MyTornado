import os
from uuid import uuid4
from PIL import Image


#  生成缩略图
def make_thumb(path):
    im = Image.open(path)
    im.thumbnail((200, 200))
    im.save('statics/upload/thumb_{}.jpg'.format('abc', 'JPEG'))


class UploadImage(object):
    """
    保存上传的图片，生成对应的缩略图，保存图片的url
    """
    upload_dir = 'upload'
    thumb_dir = 'thumbs'
    thumb_size = (200, 200)

    def __init__(self, name, static_path):
        self.new_name = self.gen_new_name(name)
        self.static_path = static_path

    # 生成uuid格式图片名字
    def gen_new_name(self, name):
        # ext获取文件后缀名
        _, ext = os.path.splitext(name)
        return uuid4().hex + ext

    @property
    # 设置图片路径
    def image_url(self):
        return os.path.join(self.upload_dir, self.new_name)

    @property
    # 设置图片路径
    def save_path(self):
        return os.path.join(self.static_path, self.image_url)

    # 图片保存本地位置
    def save_upload(self, content):
        with open(self.save_path, 'wb') as fh:
            fh.write(content)

    @property
    # 缩略图保存路径，名字设置
    def thumb_url(self):
        name, ext = os.path.splitext(self.new_name)
        thumb_name = '{}_{}x{}{}'.format(name,
                                         self.thumb_size[0],
                                         self.thumb_size[1],
                                         ext)

        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)

    # 生成缩略图
    def make_thumb(self):
        im = Image.open(self.save_path)
        im.thumbnail(self.thumb_size)
        save_path = os.path.join(self.static_path, self.thumb_url)
        im.save(save_path, 'JPEG')
