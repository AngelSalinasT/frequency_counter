# dividir_partes debe devolver una lista como [[inicio1, fin1], [inicio2, fin2], ...]
def splitt(texto, inicio, partes):
    rango = int(len(texto) / partes)
    fin = rango
    listaPartes = []

    for i in range(1, partes):
        Plus = fin
        Minus = fin

        while(True):
            if (texto[Plus].isspace() or not texto[Plus].isalnum()):
                fin = Plus
                break
            elif(texto[Minus].isspace() or not texto[Minus].isalnum()):
                fin = Minus
                break
            else:
                Plus = Plus + 1
                Minus = Minus - 1            

        listaPartes.append([inicio, fin])
        inicio = fin + 1
        fin = fin + rango

    listaPartes.append([inicio, len(texto) - 1])
    return listaPartes


#by sebastian