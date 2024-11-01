def countt(texto, inicio, fin):
    frecuencia = {}
    palabra_actual = ""

    for i in range(inicio, fin):
        caracter = texto[i]
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

#by chava