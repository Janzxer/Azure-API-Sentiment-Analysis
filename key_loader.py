from pathlib import Path
import base64

BASE_DIR = Path(__file__).resolve().parent

FILES = {
    "API_KEY": "news.txt",
    "AZURE_API_KEY": "azure.txt"
}

def _read_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Missing expected file: {path.name}")
    return path.read_text(encoding="utf-8").strip()

def _b64_decode_safe(b64text: str, source_name: str) -> str:
    try:
        return base64.b64decode(b64text).decode("utf-8")
    except Exception as e:
        raise RuntimeError(f"Failed to base64-decode {source_name}: {e}") from e

_phrase_path = BASE_DIR / "phrase.txt"
if _phrase_path.exists():
    _passphrase = _read_file(_phrase_path)
else:
    _passphrase = None

def _load_token(filename: str) -> str:
    path = BASE_DIR / filename
    if not path.exists():
        return "MISSING_SECRET"
    
    raw = _read_file(path)
    decoded = _b64_decode_safe(raw, filename)

    if _passphrase and decoded.endswith(_passphrase):
        return decoded[:-len(_passphrase)]
    else:
        return decoded

API_KEY = _load_token(FILES["API_KEY"]) if (BASE_DIR / FILES["API_KEY"]).exists() else "MISSING_KEY"
AZURE_API_KEY = _load_token(FILES["AZURE_API_KEY"]) if (BASE_DIR / FILES["AZURE_API_KEY"]).exists() else "MISSING_KEY"

_endpoint_path = BASE_DIR / "azure_e.txt"
if _endpoint_path.exists():
    AZURE_END = _read_file(_endpoint_path)
else:
    AZURE_END = "https://placeholder-endpoint.cognitive.microsoft.com/"