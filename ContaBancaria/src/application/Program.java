package application;

import entities.Account;

import java.util.Locale;
import java.util.Scanner;

public class Program {
    public static void main(String[] args) {
        Locale.setDefault(Locale.US);
        Scanner sc = new Scanner(System.in);
        Account acc = new Account();
        Double balance;
        System.out.print("Enter account number: ");
        int accountNumber = sc.nextInt();
        System.out.print("Enter account holder: ");
        sc.nextLine();
        String name = sc.nextLine();
        acc.setAccountHolder(name);
        System.out.print("Is there na initial deposit (y/n)? ");
        char option = sc.next().charAt(0);
        if(option == 'y') {
            System.out.print("Enter initial deposit value: ");
            balance = sc.nextDouble();
            acc.depositValue(balance);
        }
        System.out.println("Accont data:");
        System.out.printf("Accont %d, Holder: %s, Balance: $ %.2f", accountNumber, acc.getAccountHolder(), acc.getBalance());
        //System.out.printf(acc.toString());

        System.out.println();
        System.out.print("Enter a deposit value: ");
        double deposit = sc.nextDouble();
        acc.depositValue(deposit);

        System.out.println("Accont data:");
        System.out.printf("Accont %d, Holder: %s, Balance: $ %.2f", accountNumber, acc.getAccountHolder(), acc.getBalance());

        System.out.println();
        System.out.print("Enter a withdraw value: ");
        double withdraw = sc.nextDouble();
        acc.withdrawValue(withdraw);

        System.out.println("Accont data:");
        System.out.printf("Accont %d, Holder: %s, Balance: $ %.2f", accountNumber, acc.getAccountHolder(), acc.getBalance());

        sc.close();
    }
}