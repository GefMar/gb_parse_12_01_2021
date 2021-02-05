"""
Файлы: PDF, IMG
Данные в файле могут отсутсвовать
Шаблоны данных в изображениях различны
ФОРМАТ извлекаемых данных: Символы могут быть только латиницы
Поле хранящее данные различно
"""
from typing import List
import re
from pathlib import Path
import PyPDF2
from PyPDF2.utils import PdfReadError
from PIL import Image
import pytesseract


images_path = Path(__file__).parent.joinpath('images')
if not images_path.exists():
    images_path.mkdir()

#TODO: ПРИВЕТСИ PDF к IMG
def pdf_image_extract(pdf_path:Path) -> List[Path]:
    results = []
    with pdf_path.open('rb') as file:
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError as e:
            #TODO: Записать информацию о ошибке в БД
            return results
        for page_num, page in enumerate(pdf_file.pages):
            file_name = f'{pdf_path.name}.{page_num}'
            img_data = page['/Resources']['/XObject']['/Im0']._data
            img_path = images_path.joinpath(file_name)
            img_path.write_bytes(img_data)
            results.append(img_path)
        return results


#TODO: ИЗВЛЕЧЬ (РАСПОЗНАТЬ) Данные из изображения
def get_serial_number(img_path:Path) -> List[str]:
    numbers = []
    pattern = re.compile(r"(заводской.*номер)")
    image = Image.open(img_path)
    text_rus = pytesseract.image_to_string(image, 'rus')
    matchs = len(re.findall(pattern, text_rus))
    if not matchs:
        return numbers
    text_eng = pytesseract.image_to_string(image, 'eng').split('\n')
    for idx, line in enumerate(text_rus.split('\n')):
        if re.match(pattern, line):
            numbers.append(text_eng[idx].split()[-1])
        if matchs == len(numbers):
            break
    return numbers

if __name__ == '__main__':
    pdf_temp = Path(__file__).parent.joinpath('8416_4.pdf')
    images = pdf_image_extract(pdf_temp)
    numbers = list(map(get_serial_number, images))
    print(1)
