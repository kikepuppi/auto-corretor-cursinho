def compare_resp(respostas_aluno, gabarito):
    """
    Compara as respostas do aluno com o gabarito.
    
    Args:
        respostas_aluno (dict): Dicionário com as respostas do aluno
        gabarito (dict): Dicionário com o gabarito
        
    Returns:
        dict: Resultados da comparação
    """
    total_corretas = 0
    total_incorretas = 0
    detalhes = {}
    
    for questao, resposta_correta in gabarito.items():
        resposta_aluno = respostas_aluno.get(questao, '')
        
        if resposta_aluno == resposta_correta:
            total_corretas += 1
            status = 'correto'
        else:
            total_incorretas += 1
            status = 'incorreto'
        
        detalhes[questao] = {
            'resposta_aluno': resposta_aluno,
            'resposta_correta': resposta_correta,
            'status': status
        }
    
    return {
        'total_corretas': total_corretas,
        'total_incorretas': total_incorretas,
        'total_questoes': len(gabarito),
        'detalhes': detalhes
    }