from .models import Log, LogFile
from glob import iglob
from django.conf import settings
from apachelogs import LogParser, COMBINED


def parser():
    parser = LogParser(COMBINED)
    files = iglob(settings.PARSER_LOG_PATH)

    for file in files:
        with open(file, "r",) as fp:

            logs = fp.readlines()
            file_last_line = (logs[-1])
            is_present = LogFile.objects.filter(
                last_line=file_last_line
            ).exists()

            if is_present:
                continue

            else:
                log_file = LogFile(
                    file_path=fp.name,
                    last_line=logs[-1],
                )
                LogFile.save(log_file)

                log_list = []
                for log in logs:
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
                Log.objects.bulk_create(log_list)