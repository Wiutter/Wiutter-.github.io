using System;
using System.Collections.Generic;
using System.Linq; // Necessário para .Any() e .Max()

namespace SistemaChamadosConsole
{
    // Classe para representar um chamado (Ticket)
    public class Chamado
    {
        public int Id { get; set; }
        public string Solicitante { get; set; }
        public string Descricao { get; set; }
        public string Status { get; set; }
        public DateTime DataAbertura { get; set; }

        // Construtor para facilitar a criação
        public Chamado(int id, string solicitante, string descricao)
        {
            Id = id;
            Solicitante = solicitante ?? "Não informado"; // Garante que não seja nulo
            Descricao = descricao ?? "Não informada";   // Garante que não seja nulo
            Status = "Aberto"; // Status inicial padrão
            DataAbertura = DateTime.Now; // Data e hora atuais
        }

        // Método para exibir o chamado de forma formatada
        public override string ToString()
        {
            return $"ID: {Id} | Data: {DataAbertura:dd/MM/yyyy HH:mm} | Solicitante: {Solicitante} | Status: {Status}\n" +
                   $"   Descrição: {Descricao}\n" +
                   $"   --------------------------------------------------";
        }
    }

    // Classe principal do programa
    class Program
    {
        // Lista para armazenar os chamados em memória
        static List<Chamado> listaDeChamados = new List<Chamado>();
        // Contador para gerar IDs únicos simples
        static int proximoId = 1;

        // Método principal - Ponto de entrada do aplicativo
        static void Main(string[] args)
        {
            Console.WriteLine("=============================================");
            Console.WriteLine("   Sistema Simples de Chamados de TI (Console) ");
            Console.WriteLine("=============================================");

            bool executando = true;

            // Loop principal do menu
            while (executando)
            {
                ExibirMenu();
                string opcao = Console.ReadLine() ?? ""; // Lê a opção do usuário

                switch (opcao)
                {
                    case "1":
                        AbrirNovoChamado();
                        break;
                    case "2":
                        ListarChamados();
                        break;
                    case "3":
                        executando = false; // Termina o loop
                        Console.WriteLine("\nSaindo do sistema...");
                        break;
                    default:
                        Console.ForegroundColor = ConsoleColor.Red;
                        Console.WriteLine("\nOpção inválida! Pressione Enter para tentar novamente.");
                        Console.ResetColor();
                        Console.ReadLine(); // Pausa para o usuário ler a mensagem
                        break;
                }
            }

            Console.WriteLine("\nAplicação encerrada. Pressione qualquer tecla para fechar.");
            Console.ReadKey(); // Mantém o console aberto até o usuário pressionar uma tecla
        }

        // Exibe as opções do menu
        static void ExibirMenu()
        {
            Console.Clear(); // Limpa a tela do console para exibir o menu novamente
            Console.WriteLine("\n--- Menu Principal ---");
            Console.WriteLine("1. Abrir Novo Chamado");
            Console.WriteLine("2. Listar Chamados Abertos");
            Console.WriteLine("3. Sair");
            Console.Write("Escolha uma opção: ");
        }

        // Lógica para adicionar um novo chamado
        static void AbrirNovoChamado()
        {
            Console.Clear();
            Console.WriteLine("\n--- Abrir Novo Chamado ---");

            Console.Write("Nome do Solicitante: ");
            string solicitante = Console.ReadLine() ?? ""; // Lê o nome

            Console.Write("Descrição do Problema: ");
            string descricao = Console.ReadLine() ?? ""; // Lê a descrição

            // Validação simples (poderia ser mais robusta)
            if (string.IsNullOrWhiteSpace(solicitante) || string.IsNullOrWhiteSpace(descricao))
            {
                 Console.ForegroundColor = ConsoleColor.Yellow;
                 Console.WriteLine("\nErro: Solicitante e Descrição não podem estar vazios.");
                 Console.ResetColor();
            }
            else
            {
                // Cria o novo chamado com o próximo ID disponível
                Chamado novoChamado = new Chamado(proximoId, solicitante, descricao);
                listaDeChamados.Add(novoChamado); // Adiciona à lista
                proximoId++; // Incrementa o ID para o próximo chamado

                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine($"\nChamado ID {novoChamado.Id} aberto com sucesso!");
                Console.ResetColor();
            }

            Console.WriteLine("\nPressione Enter para voltar ao menu...");
            Console.ReadLine();
        }

        // Lógica para listar os chamados existentes
        static void ListarChamados()
        {
            Console.Clear();
            Console.WriteLine("\n--- Lista de Chamados Abertos ---");

            // Verifica se a lista está vazia usando Linq.Any()
            if (!listaDeChamados.Any()) // Mais eficiente que Count == 0 para verificar existência
            {
                Console.WriteLine("Nenhum chamado aberto no momento.");
            }
            else
            {
                // Itera sobre a lista e exibe cada chamado usando o método ToString()
                foreach (Chamado chamado in listaDeChamados)
                {
                    Console.WriteLine(chamado.ToString());
                }
            }

            Console.WriteLine("\nPressione Enter para voltar ao menu...");
            Console.ReadLine(); // Pausa para o usuário ler a lista
        }
    }
}
