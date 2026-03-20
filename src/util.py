"""
工具函数集合

主要功能：
- 文件 MD5 计算 (get_file_md5)
- MD5 重复检查 (check_md5)
- MD5 记录保存 (save_md5)

用于实现文档上传的幂等性，避免重复向量化已处理的文件。
"""
import hashlib
import os
import config


def check_md5(md5_str:str):
    """检查传入的md5字符串是否被处理过"""
    if not os.path.exists(config.md5_path):
        open(config.md5_path,'w',encoding="utf-8").close()
        return False
    else:
        for line in open(config.md5_path,'r',encoding="utf-8").readlines():
            line = line.strip()
            if line == md5_str:
                return True
        return False

def save_md5(md5_str:str):
    """将传入的md5字符串，记录到文件中保存"""
    with open(config.md5_path,'a',encoding="utf-8") as f:
        f.write(md5_str + "\n")

def get_file_md5(path: str) -> str:
    hash_md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()