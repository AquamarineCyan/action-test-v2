from pathlib import Path


class APPLICATION:

    VERSION: str = "1.7.4"
    APP_NAME: str = "Onmyoji_Python"
    APP_EXE_NAME: str = f"{APP_NAME}.exe"

    APP_PATH: Path = Path().cwd()
    CONFIG_PATH: Path = APP_PATH / "config.yaml"
    LOG_DIR_PATH: Path = APP_PATH / "log"
    RESOURCE_DIR_PATH: Path = APP_PATH / "resource"


app = APPLICATION()
