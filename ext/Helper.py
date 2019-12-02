from datetime import datetime as dt


def url_to_date(url):
    year, month, day = url.split('/')[-1][:4], url.split('/')[-1][4:6], url.split('/')[-1][6:8]
    return dt.strptime('{}/{}/{}'.format(day, month, year), "%d/%m/%Y")

