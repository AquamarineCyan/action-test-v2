from .utils import Package, check_package


class TanSuo(Package):
    resource_path = "tansuo"
    resource_list = [
        "boss_finish",
        "chuzhanxiaohao",
        "fighting",
        "fighting_boss",
        "kunnan_big",
        "kunnan_small",
        "putong_big",
        "putong_small",
        "quit_true",
        "quit_true_false",
        "tansuo",
        "tansuo_28",
        "tansuo_28_0",
        "tansuo_28_title",
        "treasure_box",
        "zidonglunhuan",
    ]


def test_tansuo():
    check_package(TanSuo)
