def countt(texto):
    frecuencia = {}
    palabra_actual = ""

    for caracter in texto:
        if caracter.isspace() or not caracter.isalnum():
            if palabra_actual:
                palabra_actual = palabra_actual.lower()
                if palabra_actual in frecuencia:
                    frecuencia[palabra_actual] += 1
                else:
                    frecuencia[palabra_actual] = 1
                palabra_actual = ""
        else:
            palabra_actual += caracter

    if palabra_actual:
        palabra_actual = palabra_actual.lower()
        if palabra_actual in frecuencia:
            frecuencia[palabra_actual] += 1
        else:
            frecuencia[palabra_actual] = 1

    return frecuencia
