def string_formatter(text):
    text_split = text.split(",")
    temp = [d.strip() for d in text_split]

    peserta = []

    for data in temp:
        data_split = data.split(">")
        result = {
            "nama": data_split[0].strip(),
            "jurusan": data_split[1].strip()
        }
        peserta.append(result)

    return peserta
