import java.util.Scanner;

public class App {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Digite a mensagem: ");
        String mensagem = sc.nextLine();

        System.out.print("Digite o número (positivo) para deslocamento: ");
        int deslocamento = sc.nextInt();

        System.out.print("Digite 'c' para cifrar ou 'd' para decifrar: ");
        char opcao = sc.next().charAt(0);

        String mensagemTransformada = transformarMensagem(mensagem, deslocamento, opcao);
        System.out.println("Mensagem transformada: " + mensagemTransformada);
    }

    public static String transformarMensagem(String mensagem, int deslocamento, char opcao) {
        String mensagemTransformada = "";
        if (opcao == 'c' || opcao == 'd') {
            if (opcao == 'd') {
                deslocamento = 26 - (deslocamento % 26);
            }
            for (int i = 0; i < mensagem.length(); i++) {
                char caractere = mensagem.charAt(i);
                if (Character.isLetter(caractere)) {
                    char base = 'a';
                    if (Character.isUpperCase(caractere)) {
                        base = 'A';
                    }
                    int codigo = ((int) caractere - base + deslocamento + 26) % 26 + base;
                    mensagemTransformada += (char) codigo;
                } else {
                    mensagemTransformada += caractere;
                }
            }
        } else {
            System.out.println("Opção inválida. Por favor, digite 'c' para cifrar ou 'd' para decifrar.");
        }
        return mensagemTransformada;
    }
}
