from datetime import datetime


def to_localtime(date):
    str_month = {
        "1": "Januari",
        "2": "Februari",
        "3": "Maret",
        "4": "April",
        "5": "Mei",
        "6": "Juni",
        "7": "Juli",
        "8": "Agustus",
        "9": "September",
        "10": "Oktober",
        "11": "November",
        "12": "Desember"
    }

    day, month, year = str(date.day), str(date.month), str(date.year)
    return f"{day} {str_month[month]} {year}"
