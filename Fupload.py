# 使用 pip 安装sdk：pip install -U cos-python-sdk-v5

from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


class COSHelper:
    def __init__(self, secret_id, secret_key, region, token=None):
        """初始化COS客户端"""
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.region = region
        self.token = token
        self.config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Token=token)
        self.client = CosS3Client(self.config)

    def upload_bytes(self, bucket, key, content_bytes):
        """上传二进制内容到COS"""
        try:
            response = self.client.put_object(
                Bucket=bucket,
                Body=content_bytes,
                Key=key,
                EnableMD5=False
            )
            logging.info(f"上传成功: {response['ETag']}")
            return True
        except Exception as e:
            logging.error(f"上传失败: {e}")
            return False

    def upload_file(self, bucket, key, local_file_path):
        """上传文件到COS"""
        try:
            with open(local_file_path, 'rb') as file:
                content = file.read()
                return self.upload_bytes(bucket, key, content)
        except Exception as e:
            logging.error(f"读取文件失败: {e}")
            return False

    def download_file(self, bucket, key, local_file_path):
        """从COS下载文件"""
        try:
            response = self.client.get_object(
                Bucket=bucket,
                Key=key
            )
            response['Body'].get_stream_to_file(local_file_path)
            logging.info(f"下载成功，已保存至: {local_file_path}")
            return True
        except Exception as e:
            logging.error(f"下载失败: {e}")
            return False

    def list_objects(self, bucket, prefix=''):
        """列出存储桶中的对象"""
        try:
            response = self.client.list_objects(
                Bucket=bucket,
                Prefix=prefix
            )
            if 'Contents' in response:
                return [item['Key'] for item in response['Contents']]
            return []
        except Exception as e:
            logging.error(f"列出对象失败: {e}")
            return []


if __name__ == "__main__":
    # 配置信息
    secret_id = 'AKID86FF4f2FG6kFYjkiW9YklcHk6PXVJuIU'
    secret_key = 'BJl25wcAVTFtMpEQPCpusdBWnuR4qaKu'
    region = 'ap-guangzhou'  # 替换为存储桶所属地域
    bucket = 'xiaodao-1331856197'  # 替换为你的存储桶名称

    # 初始化类
    cos_helper = COSHelper(secret_id, secret_key, region)

    # 示例1：上传二进制内容
    cos_helper.upload_bytes(
        bucket=bucket,
        key='exampleobject',
        content_bytes=b'Hello, COS!'
    )

    # 示例2：上传文件
    cos_helper.upload_file(
        bucket=bucket,
        key='test_upload.txt',
        local_file_path='./test.txt'
    )

    # 示例3：下载文件
    cos_helper.download_file(
        bucket=bucket,
        key='exampleobject',
        local_file_path='./downloaded_example.txt'
    )

    # 示例4：列出对象
    objects = cos_helper.list_objects(bucket)
    print(f"存储桶中的对象: {objects}")