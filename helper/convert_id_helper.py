import re

code = open("TileID.cs", "r", encoding="utf-8").read()

def cs_constants_to_python(cs_code: str) -> str:
    """
    Преобразует C# const поля в Python константы (UPPER_CASE)
    """
    lines = cs_code.split('\n')
    result = []

    # Ищем строки вида: public const тип ИМЯ = значение;
    pattern = re.compile(
        r'^\s*public\s+const\s+(?:ushort|int|byte|float|double|string)\s+'
        r'([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([^;]+);',
        re.MULTILINE
    )

    for match in pattern.finditer(cs_code):
        name = match.group(1)
        value = match.group(2).strip()

        # Преобразуем имя в UPPER_CASE стиль Python
        py_name = name.upper()

        # Убираем лишние пробелы и приводим значение к читаемому виду
        value = value.replace('f', '')   # float
        value = value.strip()

        # Если строка — оставляем кавычки
        if value.startswith('"') and value.endswith('"'):
            result.append(f"{py_name} = {value}")
        else:
            # Числовые значения
            result.append(f"{py_name} = {value}")

    if result:
        result.insert(0, "# Константы из Terraria TileID (автогенерация)")
        result.append("")

    return "\n".join(result)


# Пример использования
if __name__ == "__main__":
    # Вставьте сюда ваш .cs код как строку
    cs_text = """
public const ushort Dirt = 0;
public const ushort Stone = 1;
public const ushort Grass = 2;
public readonly static ushort Count = 753;
    """

    python_code = cs_constants_to_python(cs_text)
    print(python_code)