import json


def write_to_json(json_data: dict, filepath: str):
    """dictデータをjsonに書き込み．

    Args:
        json_data (dict): 保存したいdictデータ．
        filepath (str): 保存するファイルパス．
    """
    with open(filepath, 'w') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)


def load_json(filepath: str) -> dict:
    """jsonファイルをロード．

    Args:
        filepath (str): ロードするjsonファイルパス．

    Returns:
        dict: jsonから取り出した辞書データ．
    """
    with open(filepath, 'r') as f:
        return json.load(f)
