from fontTools.ttLib import TTFont


def print_font_character(font_path):
    # 使用fontTools加载字体文件
    font = TTFont(font_path)

    # 获取字体支持的字符范围
    supported_chars = set()
    for table in font["cmap"].tables:
        if table.isUnicode():
            supported_chars.update(chr(code) for code in table.cmap.keys())

    # 打印支持的字符范围
    i = 0
    for char in sorted(supported_chars):
        i += 1
        print(char, end="")
        if i % 50 == 0:
            print()
