#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define MIN_STRING_LEN 4 // Tamanho mínimo para ser considerado uma string

int main(int argc, char *argv[]) {
    // 1. Validação de argumentos
    if (argc != 2) {
        fprintf(stderr, "Uso: %s <arquivo>\n", argv[0]);
        return EXIT_FAILURE;
    }

    // 2. Tratamento de erro ao abrir o arquivo
    FILE *fp = fopen(argv[1], "rb");
    if (fp == NULL) {
        perror("Erro ao abrir o arquivo");
        return EXIT_FAILURE;
    }

    unsigned char byte;
    char buffer[1024]; // Buffer para armazenar a string temporariamente
    int count = 0;

    // 3. Leitura e filtragem
    while (fread(&byte, sizeof(byte), 1, fp)) {
        // Verifica se o caractere é imprimível (tabela ASCII) ou tabulação
        if (isprint(byte) || byte == '\t') {
            if (count < sizeof(buffer) - 1) {
                buffer[count++] = byte;
            }
        } else {
            // Se encontrou um caractere não imprimível, verifica se o que lemos até agora forma uma string
            if (count >= MIN_STRING_LEN) {
                buffer[count] = '\0'; // Finaliza a string
                printf("%s\n", buffer);
            }
            count = 0; // Reseta o contador para a próxima sequência
        }
    }

    // 4. Verifica se sobrou alguma string no final do arquivo
    if (count >= MIN_STRING_LEN) {
        buffer[count] = '\0';
        printf("%s\n", buffer);
    }

    fclose(fp);
    return EXIT_SUCCESS;
}
