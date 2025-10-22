"""
Analisador Léxico Aprimorado - Versão Simplificada
Implementa: Match mais longo, Estrutura de Token, Bufferização e Interface para Parser
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'AFDS'))

from AFDS.afd_ident import AFDIdent
from AFDS.afd_keyword import AFDKeyword  
from AFDS.afd_number import AFDNumber
from AFDS.afd_operator import AFDOperator
from AFDS.afd_string import AFDString
from AFDS.afd_char import AFDChar
from AFDS.afd_comment import AFDComment
from AFDS.afd_delimiters import AFDDelimiters
from AFDS.afd_whitespace import AFDWhitespace

# ============= ESTRUTURA DE TOKEN APRIMORADA ============= 

class Token:
    """Token com informações completas para análise sintática"""
    def __init__(self, tipo, lexema, linha, coluna, valor=None):
        self.tipo = tipo          # Tipo do token
        self.lexema = lexema      # Texto literal
        self.linha = linha        # Linha no código
        self.coluna = coluna      # Coluna no código
        self.valor = valor        # Valor processado (números, etc.)
    
    def __str__(self):
        return f"{self.tipo:15} {self.lexema!r:20} [linha {self.linha}, col {self.coluna}]"
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.lexema!r}, {self.linha}, {self.coluna})"

class LexicalError:
    """Erro léxico com informações de posição"""
    def __init__(self, lexema, linha, coluna, mensagem="Token não reconhecido"):
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna
        self.mensagem = mensagem
    
    def __str__(self):
        return f"Erro léxico na linha {self.linha}, coluna {self.coluna}: {self.mensagem} '{self.lexema}'"

# BUFFER SIMPLES COM LOOK-AHEAD

class SimpleBuffer:
    """Buffer simples com suporte a look-ahead para o lexer"""
    
    def __init__(self, texto):
        self.texto = texto
        self.posicao = 0
        self.tamanho = len(texto)
        self.linha = 1
        self.coluna = 1
        
    def peek(self, offset=0):
        """Olha caractere à frente sem consumir"""
        pos = self.posicao + offset
        if pos < self.tamanho:
            return self.texto[pos]
        return None
    
    def next_char(self):
        """Consome e retorna próximo caractere"""
        if self.posicao >= self.tamanho:
            return None
        
        char = self.texto[self.posicao]
        self.posicao += 1
        
        # Atualiza posição de linha/coluna
        if char == '\n':
            self.linha += 1
            self.coluna = 1
        else:
            self.coluna += 1
            
        return char
    
    def get_position(self):
        """Retorna posição atual (linha, coluna)"""
        return (self.linha, self.coluna)
    
    def get_offset(self):
        """Retorna offset atual no texto"""
        return self.posicao

# ============= LEXER APRIMORADO =============

class EnhancedLexer:
    """
    Analisador Léxico Aprimorado com:
    - Princípio do match mais longo
    - Buffer otimizado
    - Estrutura de token completa
    - Interface para análise sintática
    """
    
    def __init__(self):
        # Inicializa AFDs na ordem de prioridade
        self.afds = [
            ('KEYWORD', AFDKeyword()),
            ('NUMBER', AFDNumber()), 
            ('IDENT', AFDIdent()),
            ('STRING', AFDString()),
            ('CHAR', AFDChar()),
            ('COMMENT', AFDComment()),
            ('OPERATOR', AFDOperator()),
            ('DELIMITERS', AFDDelimiters()),
            ('WHITESPACE', AFDWhitespace())
        ]
        
        # Tabela de palavras-chave (hash table para classificação)
        self.keywords = {
            'class', 'struct', 'interface', 'extends', 'implements', 'new',
            'this', 'super', 'function', 'void', 'var', 'let', 'const', 'return',
            'if', 'else', 'switch', 'case', 'default', 'break', 'continue', 'for',
            'foreach', 'while', 'do', 'true', 'false', 'null', 'public', 'private',
            'protected', 'static', 'int', 'float', 'string', 'bool', 'list', 'dict',
            'print'
        }
        
        # Estado interno para interface com parser
        self.tokens_gerados = []
        self.erros_encontrados = []
        self.token_atual_index = 0
        self.buffer = None

    def _longest_match(self, buffer, start_linha, start_coluna):
        """
        PRINCÍPIO DO MATCH MAIS LONGO
        Implementa o algoritmo de correspondência máxima:
        - Tenta todos os AFDs
        - Para cada AFD, encontra o maior match possível
        - Retorna o maior match entre todos os AFDs
        - Inclui backtracking se necessário
        """
        melhor_match = None
        melhor_tamanho = 0
        melhor_tipo = None
        
        posicao_inicial = buffer.get_offset()
        linha_inicial = buffer.linha
        coluna_inicial = buffer.coluna
        
        # Para cada AFD, tenta encontrar o maior match
        for token_type, afd in self.afds:
            lexema_atual = ""
            ultimo_match_valido = None
            ultimo_tamanho = 0
            
            # Salva estado completo para restaurar depois
            pos_salva = buffer.get_offset()
            linha_salva = buffer.linha
            coluna_salva = buffer.coluna
            
            # Tenta formar tokens cada vez maiores
            while True:
                char = buffer.next_char()
                if char is None:
                    break
                
                lexema_atual += char
                
                try:
                    # Verifica se o lexema atual é válido
                    if afd.accepts(lexema_atual):
                        # Match válido encontrado - salva
                        ultimo_match_valido = lexema_atual
                        ultimo_tamanho = len(lexema_atual)
                    
                    # Verifica se ainda pode continuar
                    # (existe alguma transição válida para o próximo char?)
                    proximo_char = buffer.peek()
                    if proximo_char:
                        teste = lexema_atual + proximo_char
                        # Se não aceita e não pode continuar, para
                        if not self._pode_continuar(afd, teste):
                            break
                    else:
                        break
                        
                except:
                    # Erro no AFD - para de tentar este AFD
                    break
            
            # Restaura estado completo do buffer
            buffer.posicao = pos_salva
            buffer.linha = linha_salva
            buffer.coluna = coluna_salva
            
            # Se este AFD teve um match maior, atualiza o melhor
            if ultimo_tamanho > melhor_tamanho and ultimo_match_valido:
                melhor_match = ultimo_match_valido
                melhor_tamanho = ultimo_tamanho
                melhor_tipo = token_type
        
        return melhor_tipo, melhor_match, melhor_tamanho
    
    def _pode_continuar(self, afd, lexema):
        """Verifica se o AFD pode continuar processando"""
        try:
            # Tenta processar - se não lançar exceção, pode continuar
            afd.process_string(lexema)
            return True
        except:
            return False

    def _processar_valor(self, tipo, lexema):
        """Processa e extrai valor de literais"""
        if tipo == 'NUMBER':
            try:
                # Tenta converter para int primeiro
                if '.' not in lexema and 'e' not in lexema.lower():
                    return int(lexema)
                else:
                    return float(lexema)
            except:
                return None
        elif tipo == 'STRING':
            # Remove aspas
            return lexema[1:-1] if len(lexema) >= 2 else lexema
        elif tipo == 'CHAR':
            # Remove aspas simples
            return lexema[1:-1] if len(lexema) >= 2 else lexema
        elif tipo == 'KEYWORD':
            # Valores booleanos e null
            if lexema == 'true':
                return True
            elif lexema == 'false':
                return False
            elif lexema == 'null':
                return None
        
        return None

    def tokenize(self, codigo):
        """
        TOKENIZAÇÃO COM BUFFER
        Processa o código fonte usando buffer otimizado
        Retorna lista de tokens e erros
        """
        self.buffer = SimpleBuffer(codigo)
        tokens = []
        erros = []
        
        while self.buffer.get_offset() < self.buffer.tamanho:
            linha, coluna = self.buffer.get_position()
            
            # Pula espaços em branco manualmente
            char_atual = self.buffer.peek()
            if char_atual and char_atual.isspace():
                self.buffer.next_char()
                continue
            
            # Busca o maior match usando PRINCÍPIO DO MATCH MAIS LONGO
            token_type, lexema, tamanho = self._longest_match(
                self.buffer, linha, coluna
            )
            
            if tamanho == 0:
                # ERRO LÉXICO - nenhum AFD reconheceu
                # Consome caracteres até encontrar espaço
                char_erro = self.buffer.next_char()
                lexema_erro = char_erro if char_erro else ""
                
                while True:
                    proximo = self.buffer.peek()
                    if not proximo or proximo.isspace():
                        break
                    lexema_erro += self.buffer.next_char()
                
                erro = LexicalError(lexema_erro, linha, coluna)
                erros.append(erro)
                continue
            
            # Avança buffer pelo tamanho do match
            for _ in range(tamanho):
                self.buffer.next_char()
            
            # Classifica identificadores vs palavras-chave (tabela hash)
            if token_type == 'IDENT' and lexema.lower() in self.keywords:
                token_type = 'KEYWORD'
            
            # Pula comentários na saída (mas reconhece)
            if token_type == 'COMMENT':
                continue
            
            # Processa valor se necessário
            valor = self._processar_valor(token_type, lexema)
            
            # Cria token com estrutura completa
            token = Token(token_type, lexema, linha, coluna, valor)
            tokens.append(token)
        
        # Armazena para interface com parser
        self.tokens_gerados = tokens
        self.erros_encontrados = erros
        self.token_atual_index = 0
        
        return tokens, erros

    # ============= INTERFACE PARA ANÁLISE SINTÁTICA =============
    
    def next_token(self):
        """
        Interface para parser: retorna próximo token
        Usado pelo analisador sintático para consumir tokens sequencialmente
        """
        if self.token_atual_index < len(self.tokens_gerados):
            token = self.tokens_gerados[self.token_atual_index]
            self.token_atual_index += 1
            return token
        return None
    
    def peek_token(self, offset=0):
        """
        Interface para parser: olha tokens à frente sem consumir
        Útil para decisões de parsing (lookahead)
        """
        index = self.token_atual_index + offset
        if index < len(self.tokens_gerados):
            return self.tokens_gerados[index]
        return None
    
    def current_token(self):
        """Retorna token atual sem avançar"""
        if self.token_atual_index > 0:
            return self.tokens_gerados[self.token_atual_index - 1]
        return None
    
    def expect(self, tipo_esperado):
        """
        Interface para parser: consome token esperado ou gera erro
        Usado para verificação sintática
        """
        token = self.next_token()
        if token is None:
            raise SyntaxError(f"Esperado {tipo_esperado}, encontrado EOF")
        if token.tipo != tipo_esperado:
            raise SyntaxError(
                f"Esperado {tipo_esperado}, encontrado {token.tipo} "
                f"na linha {token.linha}, coluna {token.coluna}"
            )
        return token
    
    def match(self, tipo):
        """
        Interface para parser: verifica se próximo token é do tipo esperado
        Não consome o token
        """
        token = self.peek_token()
        return token and token.tipo == tipo
    
    def reset(self):
        """Reinicia o índice de tokens para reanálise"""
        self.token_atual_index = 0
    
    def has_errors(self):
        """Verifica se há erros léxicos"""
        return len(self.erros_encontrados) > 0
    
    def get_all_tokens(self):
        """Retorna todos os tokens gerados"""
        return self.tokens_gerados
    
    def get_all_errors(self):
        """Retorna todos os erros encontrados"""
        return self.erros_encontrados

    # ============= MÉTODO DE ANÁLISE PRINCIPAL =============
    
    def analisar(self, codigo):
        """
        Método principal para análise léxica
        Imprime tabela de tokens e erros
        """
        tokens, erros = self.tokenize(codigo)
        
        # Imprime tokens reconhecidos
        if tokens:
            print("\n" + "="*70)
            print("TOKENS RECONHECIDOS")
            print("="*70)
            print(f"{'TIPO':<15} {'LEXEMA':<20} {'POSIÇÃO':<20} {'VALOR'}")
            print("-"*70)
            for token in tokens:
                valor_str = str(token.valor) if token.valor is not None else ""
                print(f"{token.tipo:<15} {token.lexema!r:<20} "
                      f"[L{token.linha}:C{token.coluna}]{'':<8} {valor_str}")
            print("="*70)
        
        # Imprime erros se houver
        if erros:
            print("\n" + "="*70)
            print("ERROS LÉXICOS ENCONTRADOS")
            print("="*70)
            for erro in erros:
                print(erro)
            print("="*70)
        else:
            print(f"\n✓ Análise concluída com sucesso! {len(tokens)} tokens reconhecidos.")
        
        return tokens, erros

# ============= TESTE DO LEXER =============

def main():
    """Função de teste"""
    
    codigo_teste = '''float numero = 10.0;

function parImpar(num)
{
    if (num % 2 == 0)
    {
        return "É par";
    } else
    {
        return "É impar";
    }
}

print(parImpar(numero));'''
    
    print("="*70)
    print("ANALISADOR LÉXICO APRIMORADO - LINGUAGEM SIMPLEPOO")
    print("="*70)
    print("Características implementadas:")
    print("  ✓ Princípio do match mais longo")
    print("  ✓ Estrutura de token completa (tipo, lexema, posição, valor)")
    print("  ✓ Bufferização com look-ahead")
    print("  ✓ Interface para análise sintática")
    print("="*70)
    print("\nCódigo a ser analisado:")
    print("-" * 70)
    print(codigo_teste)
    print("-" * 70)
    
    lexer = EnhancedLexer()
    tokens, erros = lexer.analisar(codigo_teste)
    
    # Demonstra interface para parser
    print("\n" + "="*70)
    print("DEMONSTRAÇÃO DA INTERFACE PARA PARSER")
    print("="*70)
    
    lexer.reset()  # Reinicia para demonstração
    
    print("\n1. Usando next_token():")
    print(f"   Primeiro token: {lexer.next_token()}")
    print(f"   Segundo token: {lexer.next_token()}")
    
    print("\n2. Usando peek_token():")
    print(f"   Próximo token (peek): {lexer.peek_token()}")
    print(f"   Token seguinte (peek): {lexer.peek_token(1)}")
    print(f"   Consumindo: {lexer.next_token()}")
    
    print("\n3. Usando match():")
    if lexer.match('OPERATOR'):
        print(f"   Match de OPERATOR: {lexer.next_token()}")
    
    print("\n" + "="*70)

if __name__ == "__main__":
    main()
