package entities;

public class Account {
    private int accountNumber;
    private String accountHolder;
    private double balance;

    public int getAccountNumber() {
        return accountNumber;
    }

    public String getAccountHolder() {
        return accountHolder;
    }

    public void setAccountHolder(String accountHolder) {
        this.accountHolder = accountHolder;
    }

    public double getBalance() {
        return balance;
    }

    public Account (){
    }

    public Account(int accountNumber, String accountHolder) {
        this.accountNumber = accountNumber;
        this.accountHolder = accountHolder;
    }

    public void depositValue(double deposit){
        balance += deposit;
    }

    public void withdrawValue(double withdraw){
        balance -= withdraw + 5.00;
        //balance -= 5.00;
    }
}
