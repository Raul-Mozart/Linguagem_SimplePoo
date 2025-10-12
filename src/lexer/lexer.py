"""
Analisador Léxico (Lexer) - Implementação usando AFD

Este módulo implementa um analisador léxico completo que usa
Autômatos Finitos Determinísticos (AFD) para reconhecer tokens.

O analisador:
1. Recebe código fonte como entrada
2. Identifica tokens usando AFDs compilados a partir de regex
3. Retorna stream de tokens com informações de posição
4. Reporta erros léxicos detalhados

Autor: Sistema de Compiladores
Data: 2025
"""

import sys
import os
from typing import List, Dict, Tuple, Optional, NamedTuple
from dataclasses import dataclass

# Importar módulo de conversão AFN->AFD
# Ajustar path para usar os autômatos do projeto
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../Compiladores'))

try:
    from modulos_lexicos.estruturas import DFA as AFD
    from modulos_lexicos import compile_regex_to_dfa
except ImportError:
    print("❌ Erro: Não foi possível importar módulos de autômatos")
    print("Certifique-se de que o diretório Compiladores/modulos_lexicos existe")
    sys.exit(1)


# ==================== ESTRUTURAS DE DADOS ====================

class Token(NamedTuple):
    """
    Representa um token identificado no código fonte
    
    Atributos:
        tipo: categoria do token (KEYWORD, IDENTIFIER, etc.)
        lexema: texto literal do token
        linha: linha onde o token foi encontrado (1-indexed)
        coluna: coluna onde o token inicia (1-indexed)
    """
    tipo: str
    lexema: str
    linha: int
    coluna: int
    
    def __str__(self):
        return f"<{self.tipo}, '{self.lexema}', {self.linha}:{self.coluna}>"


class ErroLexico(NamedTuple):
    """
    Representa um erro léxico encontrado durante análise
    
    Atributos:
        mensagem: descrição do erro
        linha: linha onde ocorreu o erro
        coluna: coluna onde ocorreu o erro
        caractere: caractere(s) que causou(aram) o erro
    """
    mensagem: str
    linha: int
    coluna: int
    caractere: str
    
    def __str__(self):
        return f"Erro léxico [{self.linha}:{self.coluna}]: {self.mensagem} ('{self.caractere}')"


@dataclass
class ResultadoAnalise:
    """
    Resultado completo da análise léxica
    
    Atributos:
        tokens: lista de tokens identificados
        erros: lista de erros léxicos encontrados
        sucesso: True se não houve erros
    """
    tokens: List[Token]
    erros: List[ErroLexico]
    
    @property
    def sucesso(self) -> bool:
        return len(self.erros) == 0


# ==================== DEFINIÇÃO DE TOKENS DA LINGUAGEM ====================

# Tokens da linguagem proposta (baseado na especificação)
ESPECIFICACAO_TOKENS = {
    # PALAVRAS-CHAVE (ordem importa - mais específicas primeiro)
    "KEYWORD": r"(if|else|for|while|function|var|in|class|return|string|int|float|bool|list|and|or|not|private|public|mutable|inherits|new|as|true|false)",
    
    # IDENTIFICADORES (nomes de variáveis, funções, etc.)
    "IDENTIFIER": r"[A-Za-z_][A-Za-z0-9_]*",
    
    # LITERAIS NUMÉRICOS
    "FLOAT_LITERAL": r"\d+\.\d+([eE][+-]?\d+)?",  # Mais específico que INT
    "INT_LITERAL": r"\d+",
    
    # LITERAIS DE STRING (simplificado para compatibilidade)
    "STRING_LITERAL": r'"[^"]*"',  # String simples entre aspas
    
    # OPERADORES RELACIONAIS (mais específicos primeiro)
    "RELOP": r"(==|!=|<=|>=|<|>)",
    
    # OPERADORES ARITMÉTICOS
    "ARITHOP": r"[+\-*/%]",
    
    # OPERADOR DE ATRIBUIÇÃO
    "ASSIGN": r"=",
    
    # OPERADOR DE RANGE
    "RANGE": r"\.\.",
    
    # DELIMITADORES
    "LPAREN": r"\(",
    "RPAREN": r"\)",
    "LBRACE": r"\{",
    "RBRACE": r"\}",
    "LBRACKET": r"\[",
    "RBRACKET": r"\]",
    
    # PONTUAÇÃO
    "SEMICOLON": r";",
    "COMMA": r",",
    "DOT": r"\.",
    "COLON": r":",
    
    # COMENTÁRIOS
    "COMMENT": r"//[^\n]*",
    
    # ESPAÇOS EM BRANCO (serão ignorados)
    "WHITESPACE": r"[ \t\r]+",
    "NEWLINE": r"\n",
}


# Ordem de prioridade para matching (evitar ambiguidade)
ORDEM_TOKENS = [
    # Comentários primeiro (para não confundir // com divisão)
    "COMMENT",
    
    # Literais de string (para não interpretar conteúdo)
    "STRING_LITERAL",
    
    # Números (float antes de int)
    "FLOAT_LITERAL",
    "INT_LITERAL",
    
    # Keywords antes de identificadores
    "KEYWORD",
    "IDENTIFIER",
    
    # Operadores multi-caractere antes de simples
    "RANGE",
    "RELOP",
    
    # Resto dos tokens
    "ASSIGN",
    "ARITHOP",
    "LPAREN", "RPAREN",
    "LBRACE", "RBRACE",
    "LBRACKET", "RBRACKET",
    "SEMICOLON", "COMMA", "COLON", "DOT",
    
    # Whitespace por último
    "WHITESPACE",
    "NEWLINE",
]


# ==================== ANALISADOR LÉXICO ====================

class AnalisadorLexico:
    """
    Analisador Léxico que usa AFDs para reconhecer tokens
    
    Funcionamento:
    1. Compila cada regex de token para um AFD
    2. Para cada posição no código:
       - Tenta fazer match com cada AFD
       - Escolhe o match mais longo
       - Emite token correspondente
    3. Reporta erros para caracteres não reconhecidos
    """
    
    def __init__(self, especificacao: Optional[Dict[str, str]] = None):
        """
        Inicializa o analisador léxico
        
        Args:
            especificacao: dicionário opcional de tokens {nome: regex}
                         Se None, usa ESPECIFICACAO_TOKENS padrão
        """
        self.especificacao = especificacao or ESPECIFICACAO_TOKENS
        self.ordem_matching = ORDEM_TOKENS
        self.afds: Dict[str, AFD] = {}
        self.tokens_ignorados = {"WHITESPACE", "COMMENT"}  # Não aparecem no resultado
        
        # Compilar todos os tokens para AFDs
        self._compilar_tokens()
    
    def _compilar_tokens(self):
        """Compila todos os padrões de tokens para AFDs"""
        print("🔄 Compilando tokens para AFDs...")
        
        for nome_token in self.ordem_matching:
            if nome_token not in self.especificacao:
                continue
            
            regex = self.especificacao[nome_token]
            
            try:
                # Tentar importar função de compilação
                if 'compile_regex_to_dfa' in globals():
                    afd = compile_regex_to_dfa(regex)
                else:
                    print(f"  ⚠️  {nome_token}: AFD não compilado (função não disponível)")
                    continue
                
                self.afds[nome_token] = afd
                print(f"  ✅ {nome_token}: {len(afd.states)} estados")
                
            except Exception as e:
                print(f"  ❌ {nome_token}: Erro -> {e}")
        
        print(f"📊 Total compilado: {len(self.afds)}/{len(self.especificacao)} tokens\n")
    
    def _encontrar_match_mais_longo(
        self, 
        codigo: str, 
        posicao: int
    ) -> Optional[Tuple[str, str]]:
        """
        Encontra o token que faz o match mais longo a partir da posição
        
        Args:
            codigo: código fonte completo
            posicao: posição atual no código
            
        Returns:
            Tupla (tipo_token, lexema) ou None se não houver match
        """
        melhor_match = None
        maior_tamanho = 0
        
        # Tentar cada tipo de token na ordem de prioridade
        for tipo_token in self.ordem_matching:
            if tipo_token not in self.afds:
                continue
            
            afd = self.afds[tipo_token]
            
            # Tentar fazer match começando da posição atual
            tamanho_match = self._tamanho_match(afd, codigo, posicao)
            
            if tamanho_match > maior_tamanho:
                maior_tamanho = tamanho_match
                lexema = codigo[posicao:posicao + tamanho_match]
                melhor_match = (tipo_token, lexema)
        
        return melhor_match
    
    def _tamanho_match(self, afd: AFD, codigo: str, inicio: int) -> int:
        """
        Calcula o tamanho do maior match que o AFD consegue fazer
        
        Args:
            afd: Autômato Finito Determinístico
            codigo: código fonte
            inicio: posição inicial
            
        Returns:
            Tamanho do match (0 se não houver)
        """
        try:
            estado_atual = afd.start
            tamanho = 0
            ultimo_aceito = 0
            
            pos = inicio
            while pos < len(codigo):
                char = codigo[pos]
                
                # Verificar se há transição para este caractere
                if estado_atual not in afd.trans:
                    break
                if char not in afd.trans[estado_atual]:
                    break
                
                # Fazer transição
                estado_atual = afd.trans[estado_atual][char]
                tamanho += 1
                pos += 1
                
                # Se chegou em estado de aceitação, marcar
                if estado_atual in afd.accept_states:
                    ultimo_aceito = tamanho
            
            return ultimo_aceito
            
        except Exception:
            return 0
    
    def analisar(self, codigo: str) -> ResultadoAnalise:
        """
        Analisa código fonte e retorna tokens e erros
        
        Args:
            codigo: código fonte como string
            
        Returns:
            ResultadoAnalise contendo tokens e erros encontrados
        """
        tokens: List[Token] = []
        erros: List[ErroLexico] = []
        
        linha = 1
        coluna = 1
        posicao = 0
        
        while posicao < len(codigo):
            # Tentar fazer match
            match = self._encontrar_match_mais_longo(codigo, posicao)
            
            if match:
                tipo_token, lexema = match
                
                # Criar token (se não for ignorado)
                if tipo_token not in self.tokens_ignorados:
                    token = Token(
                        tipo=tipo_token,
                        lexema=lexema,
                        linha=linha,
                        coluna=coluna
                    )
                    tokens.append(token)
                
                # Atualizar posição
                for char in lexema:
                    if char == '\n':
                        linha += 1
                        coluna = 1
                    else:
                        coluna += 1
                    posicao += 1
            
            else:
                # Caractere não reconhecido - erro léxico
                char = codigo[posicao]
                erro = ErroLexico(
                    mensagem=f"Caractere inválido",
                    linha=linha,
                    coluna=coluna,
                    caractere=char
                )
                erros.append(erro)
                
                # Avançar posição
                if char == '\n':
                    linha += 1
                    coluna = 1
                else:
                    coluna += 1
                posicao += 1
        
        return ResultadoAnalise(tokens=tokens, erros=erros)
    
    def analisar_arquivo(self, caminho: str) -> ResultadoAnalise:
        """
        Analisa um arquivo de código fonte
        
        Args:
            caminho: caminho para o arquivo
            
        Returns:
            ResultadoAnalise
        """
        try:
            with open(caminho, 'r', encoding='utf-8') as f:
                codigo = f.read()
            return self.analisar(codigo)
        except FileNotFoundError:
            return ResultadoAnalise(
                tokens=[],
                erros=[ErroLexico(f"Arquivo não encontrado: {caminho}", 0, 0, "")]
            )
        except Exception as e:
            return ResultadoAnalise(
                tokens=[],
                erros=[ErroLexico(f"Erro ao ler arquivo: {e}", 0, 0, "")]
            )


# ==================== FUNÇÕES DE UTILIDADE ====================

def imprimir_tokens(tokens: List[Token]):
    """Imprime lista de tokens de forma formatada"""
    print("\n" + "="*70)
    print("TOKENS IDENTIFICADOS")
    print("="*70)
    print(f"{'Tipo':<20} {'Lexema':<25} {'Posição':<10}")
    print("-"*70)
    
    for token in tokens:
        print(f"{token.tipo:<20} {token.lexema:<25} {token.linha}:{token.coluna}")
    
    print("-"*70)
    print(f"Total: {len(tokens)} tokens\n")


def imprimir_erros(erros: List[ErroLexico]):
    """Imprime lista de erros de forma formatada"""
    if not erros:
        return
    
    print("\n" + "="*70)
    print("ERROS LÉXICOS")
    print("="*70)
    
    for erro in erros:
        print(f"❌ {erro}")
    
    print("="*70 + "\n")


def imprimir_resultado(resultado: ResultadoAnalise):
    """Imprime resultado completo da análise"""
    if resultado.sucesso:
        print("✅ Análise léxica concluída com SUCESSO!")
        imprimir_tokens(resultado.tokens)
    else:
        print("❌ Análise léxica encontrou ERROS!")
        imprimir_erros(resultado.erros)
        if resultado.tokens:
            imprimir_tokens(resultado.tokens)


# ==================== EXEMPLO DE USO ====================

if __name__ == "__main__":
    """Exemplo de uso do analisador léxico"""
    
    # Código de exemplo
    codigo_exemplo = """
    // Programa de exemplo
    var int x as 10;
    var float y as 3.14;
    var string nome as "João";
    
    if (x > 5) {
        y = y + 1.5;
    }
    
    for i in 0..10 {
        x = x + i;
    }
    """
    
    print("ANALISADOR LÉXICO - Demonstração")
    print("="*70)
    print("\nCódigo de entrada:")
    print("-"*70)
    print(codigo_exemplo)
    print("-"*70)
    
    # Criar analisador
    lexer = AnalisadorLexico()
    
    # Analisar código
    resultado = lexer.analisar(codigo_exemplo)
    
    # Mostrar resultado
    imprimir_resultado(resultado)
    
    # Teste com erro léxico
    print("\n\nTestando com erro léxico:")
    print("="*70)
    codigo_com_erro = "var int x as 10; @ # $"
    print(f"Código: {codigo_com_erro}")
    
    resultado_erro = lexer.analisar(codigo_com_erro)
    imprimir_resultado(resultado_erro)
