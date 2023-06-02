from .models import LogFile
from glob import iglob
from django.conf import settings
import magic


def fail_vailed(file):

    format_file = magic.from_file(file, mime=True)
    file_name = file.split('/')[-1]

    if format_file != 'text/plain':
        return f'Файл {file_name} не соответствует формату text/plain'

    with open(file, "r") as f:
        file_path = f.name
        file_contents = f.readlines()
        number_entries = f.tell()
        file_log, create = LogFile.objects.get_or_create(file_path=file_path)

        # Добавили ли новые данные
        start_line = number_entries - file_log.last_position
        
        # Если файл со старым именем но новыми данными.
        if not create and file_log.first_line != file_contents[0]:
            return f'Файл с именем {file_name}, уже записан в базу, переименуйте файл'
            
        # Если файл со старым нозванием.
        if not create and (start_line) > 0:
            f.seek(file_log.last_position, 0)
            file_contents = f.readlines()
            file_log.last_line = file_contents[-1]
            file_log.first_line = file_contents[0]
            file_log.last_position = number_entries
            file_log.save()
            print(f'Запись файла {file_name} обновлена')
            return file_contents

    # Если новый файл
        if create:
            file_log.last_line = file_contents[-1]
            file_log.first_line = file_contents[0]
            file_log.last_position = number_entries
            file_log.save()
            print(f'Новый файл {file_name} дбавлен')
            return file_contents

    # Если тот же самый файл
        if not create and (file_log.last_line == file_contents[-1] or file_log.first_line == file_contents[0]):
            return f'Данные файла {file_name} уже были записаны'


def par():
    files = iglob(settings.PARSER_LOG_PATH)
    for file in files:
        result = fail_vailed(file)
        if type(result) != list:
            print(result)
        else:
            for i in result:
                print(i)
