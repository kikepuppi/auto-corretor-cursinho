// Funções utilitárias para o sistema

// Formata número com uma casa decimal
function formatarNota(nota) {
    return nota.toFixed(1);
}

// Retorna a classe CSS baseada na nota
function getClasseNota(nota) {
    if (nota < 5) return 'nota-baixa';
    if (nota < 7) return 'nota-media';
    return 'nota-alta';
}

// Valida formato de questões (ex: "1-10" ou "1,2,3,4,5")
function validarFormatoQuestoes(questoes) {
    const partes = questoes.split(',');
    for (const parte of partes) {
        const trim = parte.trim();
        if (trim.includes('-')) {
            const [inicio, fim] = trim.split('-').map(Number);
            if (isNaN(inicio) || isNaN(fim) || inicio < 1 || fim > 60 || inicio > fim) {
                return false;
            }
        } else {
            const numero = Number(trim);
            if (isNaN(numero) || numero < 1 || numero > 60) {
                return false;
            }
        }
    }
    return true;
}

// Converte string de questões em lista de números
function parseQuestoes(questoes) {
    const numeros = new Set();
    const partes = questoes.split(',');
    
    for (const parte of partes) {
        const trim = parte.trim();
        if (trim.includes('-')) {
            const [inicio, fim] = trim.split('-').map(Number);
            for (let i = inicio; i <= fim; i++) {
                numeros.add(i);
            }
        } else {
            numeros.add(Number(trim));
        }
    }
    
    return Array.from(numeros).sort((a, b) => a - b);
}

// Verifica se todas as questões foram atribuídas
function verificarQuestoesAtribuidas(disciplinas) {
    const todasQuestoes = new Set();
    for (let i = 1; i <= 60; i++) {
        todasQuestoes.add(i);
    }

    const questoesAtribuidas = new Set();
    for (const questoes of Object.values(disciplinas)) {
        const parsedQuestoes = parseQuestoes(questoes);
        parsedQuestoes.forEach(q => questoesAtribuidas.add(q));
    }

    const questoesFaltando = Array.from(todasQuestoes).filter(q => !questoesAtribuidas.has(q));
    if (questoesFaltando.length > 0) {
        return false;
    }

    return true;
}

// Exporta funções para uso em outros arquivos
window.utils = {
    formatarNota,
    getClasseNota,
    validarFormatoQuestoes,
    parseQuestoes,
    verificarQuestoesAtribuidas
};