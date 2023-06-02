from .models import Log, LogFile
from glob import iglob
from django.conf import settings
from apachelogs import LogParser, COMBINED, errors
import magic


def file_vailed(file):
    '''
    Функции fail_vailed принимает на вход файл.
    Проверяет его на соответствие формата text/plain,
    если файл соответствует формату, тогда читает его,
    и проверяет.

    Если у файла новое имя, сиcтема распознаёт его как новый файл, запишет
    данные и сообщит "Данные файла {file_name} записываются".

    Если у файла имя, которое уже записано в базу, но новые данные
    (новая первая строка), система обновит данные о файле, запишет
    новые данные и сообщит - "Запись файла {file_name} обновлена"

    Если в ранее записанный файл добавить новые строки система распознает это,
    обновит данные о файле, запишет новые данные и сообщит
    - "Запись файла {file_name} обновлена"

    Если начать записывать файл, который был записан ранее,
    система сообщит - "Данные файла {file_name} были записаны ранее"
    '''

    format_file = magic.from_file(file, mime=True)
    file_name = file.split('/')[-1]

    if format_file != 'text/plain':
        return f'Файл {file_name} не соответствует формату text/plain'

    with open(file, "r") as f:
        file_path = f.name
        file_contents = f.readlines()
        number_entries = f.tell()
        file_log, create = LogFile.objects.get_or_create(file_path=file_path)
        new_line = number_entries - file_log.last_position

        # Если в ранее записанном файле полностью изменили данные.
        if (not create and file_log.first_line != file_contents[0]) or create:
            file_log.last_line = file_contents[-1]
            file_log.first_line = file_contents[0]
            file_log.last_position = number_entries
            file_log.save()
            if not create:
                print(f'Запись файла {file_name} обновлена')
            else:
                print(f'Данные файла {file_name} записываются')
            return file_contents

        # Если в ранее записанный файл добавили информацию,
        # и хотят её записать.
        if not create and (new_line > 0):
            f.seek(file_log.last_position, 0)
            file_contents = f.readlines()
            file_log.last_line = file_contents[-1]
            file_log.last_position = number_entries
            file_log.save()
            print(f'Запись файла {file_name} обновлена')
            return file_contents

        # Если хотят записать, ранее записанный файл, со старыми данными.
        if not create and (file_log.last_line == file_contents[-1]
                           or file_log.first_line == file_contents[0]):
            return f'Данные файла {file_name} были записаны ранее'


def log_creat(file_contents):
    """
    Функция log_creat принимает на вход список строк, каждая строка - это лог.
    В цикле проходим по списку.
    Строка преобразуется в запись журнала согласно формату.
    Создаётся объект класса Log и добавляется в список log_list.
    После завершения цикла список log_list записывается в базу.
    """
    parser = LogParser(COMBINED)
    log_list = []
    for log in file_contents:
        try:
            entry = parser.parse(log)
            instance_log = Log(
                        remote_host=entry.remote_host,
                        remote_logname=entry.remote_logname,
                        remote_user=entry.remote_user,
                        request_time=entry.request_time,
                        request_line=entry.request_line,
                        final_status=entry.final_status,
                        bytes_sent=entry.bytes_sent,
                        referer=entry.headers_in["Referer"],
                        user_agent=entry.headers_in["User-Agent"],
                    )
            log_list.append(instance_log)

        except errors.InvalidEntryError:
            print(f'Лог {log} не был записан, так как не соответствует формату.')

        except errors.InvalidDirectiveError:
            print('Недопустимая или неправильно сформированная директива')

        except errors.UnknownDirectiveError:
            print('Неизвестная или неподдерживаемая директива')

    Log.objects.bulk_create(log_list)
    print('Запись файла прошла успешно')


def parser():
    files = iglob(settings.PARSER_LOG_PATH)

    for file in files:
        file_contents = file_vailed(file)
        if type(file_contents) != list:
            print(file_contents)
            continue
        else:
            log_creat(file_contents)
