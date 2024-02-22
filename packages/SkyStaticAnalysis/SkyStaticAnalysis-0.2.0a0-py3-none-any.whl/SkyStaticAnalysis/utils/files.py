import base64
import mimetypes
import os


def parse_dataurl(dataurl: str):
    """
    解析前端传来的dataurl
    """
    if not dataurl.startswith("data:"):
        raise ValueError("Invalid DataURL")

    # 提取 MIME 类型和编码后的数据
    mime_type, encoded_data = dataurl[5:].split(";base64,", 1)

    # 解码数据
    decoded_data = base64.b64decode(encoded_data)

    return mime_type, decoded_data


def file_to_dataurl(file_path: str):
    """
    将文件转为dataurl
    """
    mimetype, _ = mimetypes.guess_type(file_path, strict=True)
    with open(file_path, "rb") as file:
        file_content = file.read()
        data_url = base64.b64encode(file_content).decode("ascii")

        return f"data:{mimetype};base64,{data_url}"


def abspath_from_current_file(rel_path: str, current_file: str) -> str:
    """
    Convert the relative path to absolute path.
    """
    return os.path.abspath(
        os.path.join(
            os.path.dirname(current_file),
            rel_path,
        )
    )
