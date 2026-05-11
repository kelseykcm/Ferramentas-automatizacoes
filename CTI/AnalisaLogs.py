import re
import os
import glob
from collections import defaultdict
import argparse
import sys

class LogAnalyzer:
    """
    Analisa arquivos de log para identificar, agrupar e contar mensagens de erro,
    gerando um relatório consolidado.
    """
    def __init__(self, log_path, recursive=False, extensions=None):
        self.log_path = log_path
        self.recursive = recursive
        # Garante que as extensões comecem com '.' e estejam em minúsculas
        self.extensions = [f".{ext.lower().strip('.')}" for ext in extensions] if extensions else []
        self.processed_files = 0
        
        # Padrões de regex aprimorados e flexíveis.
        # O padrão (?:[:\s]+(.*))? torna a parte da mensagem (após os dois-pontos) opcional.
        # Isso permite que ele capture tanto "ERROR: Mensagem" quanto apenas "ERROR".
        self._error_pattern_strs = {
            'ERROR':     r'ERROR(?:[:\s]+(.*))?',
            'EXCEPTION': r'Exception in thread ".*?".*?(?:[:\s]+(.*))?',
            'FATAL':     r'Fatal error(?:[:\s]+(.*))?',
            'WARNING':   r'WARNING(?:[:\s]+(.*))?',
            'CRITICAL':  r'CRITICAL(?:[:\s]+(.*))?',
            'NOTICE':    r'NOTICE(?:[:\s]+(.*))?',
            'ALERT':     r'ALERT(?:[:\s]+(.*))?',
            'EMERGENCY': r'EMERGENCY(?:[:\s]+(.*))?',
            'FAILED':    r'FAILED(?:[:\s]+(.*))?'
        }
        
        # Compila os padrões com IGNORECASE e armazena o tipo de erro associado
        self.error_patterns = {
            err_type: re.compile(pattern, re.IGNORECASE)
            for err_type, pattern in self._error_pattern_strs.items()
        }
        
        self.error_report = defaultdict(int)

    def analyze(self):
        """Analisa os arquivos de log com base no caminho fornecido."""
        self.error_report.clear()
        self.processed_files = 0
        
        files_to_process = self._find_log_files()

        if not files_to_process:
            raise FileNotFoundError(f"Nenhum arquivo correspondente encontrado para o caminho: {self.log_path}")

        for filepath in files_to_process:
            self._analyze_file(filepath)

    def _find_log_files(self):
        """Encontra todos os arquivos de log que correspondem aos critérios de busca."""
        # Se o caminho for um arquivo direto
        if os.path.isfile(self.log_path):
            if self._matches_extension(self.log_path):
                return [self.log_path]
            return []

        # Usa glob para lidar com diretórios e padrões (ex: /var/log/*.log)
        # O '**' com recursive=True permite a busca em subdiretórios
        pathname = os.path.join(self.log_path, '**' if self.recursive else '', '*')
        
        # Itera sobre todos os arquivos encontrados pelo glob
        return [
            f for f in glob.glob(pathname, recursive=self.recursive)
            if os.path.isfile(f) and self._matches_extension(f)
        ]

    def _matches_extension(self, filename):
        """Verifica se o nome do arquivo corresponde a uma das extensões permitidas."""
        if not self.extensions:
            return True  # Se nenhuma extensão for especificada, todos os arquivos são válidos
        return os.path.splitext(filename)[1].lower() in self.extensions

    def _analyze_file(self, filepath):
        """Lê e analisa um único arquivo de log."""
        try:
            # Tenta ler com UTF-8, que é o mais comum
            with open(filepath, 'r', encoding='utf-8', errors='strict') as file:
                print(f"Analisando: {filepath}")
                for line in file:
                    self._check_for_errors(line)
                self.processed_files += 1
        except (UnicodeDecodeError, IOError):
            try:
                # Se falhar, tenta com latin-1, um fallback comum
                with open(filepath, 'r', encoding='latin-1', errors='replace') as file:
                    print(f"Analisando (fallback latin-1): {filepath}")
                    for line in file:
                        self._check_for_errors(line)
                    self.processed_files += 1
            except IOError as e:
                print(f"AVISO: Não foi possível ler o arquivo '{filepath}'. Erro: {e}", file=sys.stderr)
        except Exception as e:
            print(f"AVISO: Ocorreu um erro inesperado ao processar '{filepath}'. Erro: {e}", file=sys.stderr)


    def _check_for_errors(self, line):
        """Verifica se uma linha contém um padrão de erro e o registra."""
        for err_type, pattern in self.error_patterns.items():
            match = pattern.search(line)
            if match:
                # O grupo 1 pode não existir se apenas a palavra-chave for encontrada (ex: "ERROR").
                # Se match.group(1) for None, usamos uma string vazia.
                error_message = (match.group(1) or "").strip()
                
                # Se a mensagem estiver vazia, o relatório mostrará apenas o tipo de erro.
                report_key = f"[{err_type}] {error_message}".strip()
                self.error_report[report_key] += 1
                break # Para de procurar outros padrões na mesma linha

    def generate_report(self, save_to=None):
        """Gera e opcionalmente salva o relatório de erros."""
        if not self.error_report:
            report = f"Relatório de Análise de Logs\n\nArquivos processados: {self.processed_files}\n\nNenhum erro encontrado."
        else:
            # Ordena o relatório pela quantidade de ocorrências (do maior para o menor)
            sorted_errors = sorted(self.error_report.items(), key=lambda item: item[1], reverse=True)
            
            report_lines = [
                "Relatório de Análise de Logs\n",
                f"Total de arquivos processados: {self.processed_files}",
                f"Total de tipos de erro únicos: {len(sorted_errors)}\n",
                "--- Ocorrências de Erro (ordenado por frequência) ---\n"
            ]
            
            for (error, count) in sorted_errors:
                report_lines.append(f"Ocorrências: {count:<5} | {error}")
            
            report = "\n".join(report_lines)
            
        if save_to:
            with open(save_to, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\nRelatório salvo em: {save_to}")
            
        return report

def parse_extensions(ext_str):
    """Converte a string de extensões separadas por vírgula em uma lista."""
    if not ext_str:
        return None
    return [ext.strip() for ext in ext_str.split(',')]

def main(argv=None):
    """Função principal para executar o analisador via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Analisa arquivos de log para identificar padrões de erro e gerar relatórios.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("path", help="Caminho para o arquivo, diretório ou padrão glob a ser analisado.\nExemplos:\n'errors.log'\n'/var/log/'\n'./logs/*.log'")
    parser.add_argument("-r", "--recursive", action="store_true", help="Pesquisar recursivamente em subdiretórios.")
    parser.add_argument("-e", "--extensions", help="Extensões de arquivo a serem consideradas, separadas por vírgula (ex: log,txt).")
    parser.add_argument("-s", "--save", help="Caminho do arquivo para salvar o relatório final.")
    
    args = parser.parse_args(argv or sys.argv[1:])

    try:
        extensions = parse_extensions(args.extensions)
        analyzer = LogAnalyzer(args.path, recursive=args.recursive, extensions=extensions)
        analyzer.analyze()
        
        report = analyzer.generate_report(save_to=args.save)
        print("\n" + report)
        
    except FileNotFoundError as e:
        print(f"Erro: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()