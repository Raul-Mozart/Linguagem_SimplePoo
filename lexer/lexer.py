from AFDS.afd_ident import AFDIdent
from AFDS.afd_keyword import AFDKeyword  
from AFDS.afd_number import AFDNumber
from AFDS.afd_operator import AFDOperator
from AFDS.afd_string import AFDString
from AFDS.afd_char import AFDChar
from AFDS.afd_comment import AFDComment
from AFDS.afd_delimiters import AFDDelimiters
from AFDS.afd_whitespace import AFDWhitespace

class Token:
    """Representa um token reconhecido pelo lexer"""
    def __init__(self, tipo, lexema, linha, coluna):
        self.tipo = tipo
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna
    
    def __str__(self):
        return f"{self.tipo:15} {self.lexema!r:20}"
    
    def __repr__(self):
        return f"Token({self.tipo}, {self.lexema!r}, {self.linha}, {self.coluna})"

class LexicalError:
    """Representa um erro léxico encontrado"""
    def __init__(self, lexema, linha, coluna, mensagem="Token não reconhecido"):
        self.lexema = lexema
        self.linha = linha
        self.coluna = coluna
        self.mensagem = mensagem
    
    def __str__(self):
        return f"Erro léxico na linha {self.linha}, coluna {self.coluna}: {self.mensagem} '{self.lexema}'"

class Lexer:
    """
    Analisador léxico principal que coordena múltiplos AFDs para
    reconhecimento de diferentes tipos de tokens
    """
    
    def __init__(self):
        # Inicializa os AFDs para cada tipo de token
        # Ordem importa para prioridade (keywords antes de ident, etc.)
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
        
        # Palavras-chave para verificação (caso o AFD não cubra todas)
        self.keywords = {
            'class', 'struct', 'interface', 'extends', 'implements', 'new',
            'this', 'super', 'function', 'void', 'var', 'let', 'const', 'return',
            'if', 'else', 'switch', 'case', 'default', 'break', 'continue', 'for',
            'foreach', 'while', 'do', 'true', 'false', 'null', 'public', 'private',
            'protected', 'static', 'int', 'float', 'string', 'bool', 'list', 'dict',
            'print'  # Adicionando print para o exemplo
        }

    def _get_position(self, texto, index):
        """Calcula linha e coluna a partir do índice no texto"""
        linha = texto.count('\n', 0, index) + 1
        ultimo_newline = texto.rfind('\n', 0, index)
        coluna = index - ultimo_newline if ultimo_newline != -1 else index + 1
        return linha, coluna

    def _longest_match(self, texto, start_pos):
        """
        Encontra o maior match válido a partir de uma posição.
        Retorna (tipo_token, lexema, tamanho) ou (None, None, 0) se não encontrar
        """
        melhor_match = (None, None, 0)
        
        # Para cada AFD, encontra seu maior match
        for token_type, afd in self.afds:
            maior_match_afd = 0
            melhor_lexema_afd = ""
            
            # Testa prefixos crescentes para este AFD específico
            for end_pos in range(start_pos + 1, min(len(texto) + 1, start_pos + 100)):  # limite para evitar loop infinito
                substring = texto[start_pos:end_pos]
                
                try:
                    if afd.accepts(substring):
                        # Encontrou um match válido para este AFD
                        if len(substring) > maior_match_afd:
                            maior_match_afd = len(substring)
                            melhor_lexema_afd = substring
                except:
                    # Erro no AFD ou caractere não reconhecido
                    break
            
            # Se este AFD teve um match maior que o atual melhor
            if maior_match_afd > melhor_match[2]:
                melhor_match = (token_type, melhor_lexema_afd, maior_match_afd)
        
        return melhor_match

    def tokenize(self, codigo):
        """
        Tokeniza o código fonte
        Retorna uma lista de tokens e uma lista de erros
        """
        tokens = []
        erros = []
        i = 0
        
        while i < len(codigo):
            # Pula espaços em branco (mas conta posição)
            if codigo[i].isspace():
                i += 1
                continue
            
            # Busca o maior match válido
            token_type, lexema, tamanho = self._longest_match(codigo, i)
            
            if tamanho == 0:
                # Nenhum AFD reconheceu - erro léxico
                linha, coluna = self._get_position(codigo, i)
                
                # Consome caracteres até encontrar espaço ou fim
                j = i
                while j < len(codigo) and not codigo[j].isspace():
                    j += 1
                lexema_erro = codigo[i:j]
                
                erro = LexicalError(lexema_erro, linha, coluna)
                erros.append(erro)
                i = j
                continue
            
            # Token reconhecido
            linha, coluna = self._get_position(codigo, i)
            
            # Verifica se é keyword
            if token_type == 'IDENT' and lexema.lower() in self.keywords:
                token_type = 'KEYWORD'
            
            # Pula whitespace e comentários na saída
            if token_type not in ['WHITESPACE', 'COMMENT']:
                token = Token(token_type, lexema, linha, coluna)
                tokens.append(token)
            
            i += tamanho
        
        return tokens, erros

    def analisar(self, codigo):
        """
        Método principal para análise léxica
        Imprime a tabela de tokens e erros se houver
        """
        tokens, erros = self.tokenize(codigo)
        
        # Imprime tabela de tokens
        if tokens:
            print("TOKENS RECONHECIDOS:")
            print("=" * 50)
            print(f"{'TIPO':15} {'LEXEMA':20}")
            print("-" * 50)
            for token in tokens:
                print(token)
            print("=" * 50)
        
        # Imprime erros se houver
        if erros:
            print("\nERROS LÉXICOS ENCONTRADOS:")
            print("=" * 50)
            for erro in erros:
                print(erro)
            print("=" * 50)
        else:
            print(f"\nAnálise concluída com sucesso! {len(tokens)} tokens reconhecidos.")
        
        return tokens, erros

def main():
    """Função principal para teste"""
    
    # Código de teste fornecido pelo usuário
    codigo_teste = '''float numero = 10.0;

function parImpar(num)

{

if (num % 2 == 0)

{

return "É par";

} else

{

return "É impar"

}

}

print(parImpar(numero));'''
    
    print("ANALISADOR LÉXICO - LINGUAGEM SIMPLEPOO")
    print("=" * 60)
    print("Código a ser analisado:")
    print("-" * 30)
    print(codigo_teste)
    print("-" * 30)
    
    lexer = Lexer()
    tokens, erros = lexer.analisar(codigo_teste)

if __name__ == "__main__":
    main()