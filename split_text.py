def dividir_partes(texto, inicio, partes):
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
        print(f"Inicio: {inicio} Fin: {fin}")

        inicio = fin + 1
        fin = fin + rango

    listaPartes.append([inicio, len(texto) - 1])
    print(f"Inicio: {inicio} Fin: {len(texto) - 1}")

    return listaPartes

#by sebastian