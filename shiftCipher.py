import string

alfabeto = 'abcdefghijklmnopqrstuvwxyz'

def cifrar(texto):
    texto_cifrado = ''

    for char in texto.lower():
        if char in alfabeto:
            indice = alfabeto.index(char) 
            novo_indice = (indice + 3) % len(alfabeto) #aritmética modular (resto) com k=3
            texto_cifrado += alfabeto[novo_indice]
        else:
            texto_cifrado += char
    return texto_cifrado

def frequencia_letras(texto):
    #dicionário com a frequencia das letras do alfabeto, formato {'a': 0, 'b': 0, ..., 'z': 0}
    freq = {char: 0 for char in string.ascii_lowercase} 
    for char in texto.lower():
        if char in alfabeto:
            freq[char] += 1
    #print(freq)
    return freq

#percentagens de frequência dos caracteres em Português, disponível em https://www.dcc.fc.up.pt/~rvr/naulas/tabelasPT/
frequencias_caracteres = { 'a': 13.9, 'b': 1.0, 'c': 4.4, 'd': 5.4, 'e': 12.2, 'f': 1.0, 'g': 1.2, 'h': 0.8, 'i': 6.9, 
                          'j': 0.4, 'k': 0.1, 'l': 2.8, 'm': 4.2, 'n': 5.3, 'o': 10.8, 'p': 2.9, 'q': 0.9, 'r': 6.9, 
                          's': 7.9, 't': 4.9, 'u': 4.0, 'v': 1.3, 'w': 0.0, 'x': 0.3, 'y': 0.0, 'z': 0.4 }

def ataque_frequencia(texto_cifrado):
    freq_texto_cifrado = frequencia_letras(texto_cifrado)
    print(f"Frequências do texto cifrado: {freq_texto_cifrado}")
    
    #normaliza as frequências do texto: transforma a contagem em porcentagem considerando o total de caracteres
    total_caracteres = sum(freq_texto_cifrado.values())
    if total_caracteres > 0:  
        freq_normalizada = {k: round((v/total_caracteres)*100, 2) for k, v in freq_texto_cifrado.items()} #round para 2 casas decimais X.XX
    print(f"Frequências normalizadas do texto cifrado: {freq_texto_cifrado}")
    
    #instanciando variáveis para encontrar os possíveis deslocamentos (0 a 25)
    menor_diferenca = float('inf')
    melhor_deslocamento = 0
    
    for deslocamento in range(26):
        diferenca_total = 0
        
        for letra in alfabeto:
            #qual letra do texto cifrado corresponde à letra atual após o deslocamento
            indice_original = (alfabeto.index(letra) + deslocamento) % 26
            letra_cifrada = alfabeto[indice_original]
            
            #diferença absoluta entre as frequências
            diferenca = abs(frequencias_caracteres[letra] - freq_texto_cifrado[letra_cifrada])
            # print(f"  Letra '{letra}' -> '{letra_cifrada}':")
            # print(f"    Frequência esperada de '{letra}': {frequencias_caracteres[letra]:.1f}%")
            # print(f"    Frequência encontrada de '{letra_cifrada}': {freq_normalizada[letra_cifrada]:.1f}%")
            # print(f"    Diferença: {diferenca:.1f}")

            diferenca_total += diferenca
            
        #se encontrou uma diferença menor, atualiza o melhor deslocamento
        if diferenca_total < menor_diferenca:
            menor_diferenca = diferenca_total
            melhor_deslocamento = deslocamento

        '''
        Em suma, se o deslocamento testado for o correto:
        As frequências das letras cifradas devem se aproximar das frequências esperadas das letras originais.
        Logo, o deslocamento que resultar na menor diferença total é provavelmente o usado na cifra.
        '''
    #como a cifra original usa k=3, o deslocamento para decifrar será 26-3=23
    deslocamento_original = (26 - melhor_deslocamento) % 26
    #return deslocamento_original
    
    return melhor_deslocamento
    
#decifra o texto cifrado com o deslocamento encontrado acima
def decifrar(texto_cifrado, deslocamento):
    texto_decifrado = ''
    for char in texto_cifrado.lower():
        if char in alfabeto:
            indice = alfabeto.index(char)
            novo_indice = (indice - deslocamento) % len(alfabeto)
            texto_decifrado += alfabeto[novo_indice]
        else:
            texto_decifrado += char
    return texto_decifrado

def ataque_forca_bruta(texto_cifrado):
    print("Tentativas de decifração usando todos os deslocamentos possíveis:\n")
    for deslocamento in range(26):
        texto_decifrado = decifrar(texto_cifrado, deslocamento)
        print(f"Deslocamento {deslocamento}: {texto_decifrado}")

texto_original = "teste de cifra de deslocamento"
print(f"Texto original: {texto_original}")

texto_cifrado = cifrar(texto_original)
print(f"Texto cifrado: {texto_cifrado}")

deslocamento = ataque_frequencia(texto_cifrado)
print(f"Deslocamento encontrado: {deslocamento}")

texto_decifrado = decifrar(texto_cifrado, deslocamento)
print(f"Texto decifrado: {texto_decifrado}")

ataque_forca_bruta(texto_cifrado)