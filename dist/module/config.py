import os,json
from typing import Tuple
_CONFIG_PATH=os.path.join(os.path.dirname(__file__),'config.json')
def load_config():
	with open(_CONFIG_PATH,'r')as A:return json.load(A)
def load_and_validate_paths():
	E='MUSIC_FOLDER';D='PY_DOWNLOAD_FOLDER';C=load_config();A=os.getenv(D,C.get(D,'./download/'));B=os.getenv(E,C.get(E,'./music/'))
	if not os.path.exists(A):raise FileNotFoundError(f"Download folder does not exist: {A}")
	if not os.path.exists(B):raise FileNotFoundError(f"Music folder does not exist: {B}")
	if not os.access(A,os.W_OK):raise PermissionError(f"No write access to download folder: {A}")
	if not os.access(B,os.W_OK):raise PermissionError(f"No write access to music folder: {B}")
	return A,B