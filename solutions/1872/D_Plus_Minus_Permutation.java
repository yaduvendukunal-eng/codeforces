import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();

        while (t-- > 0) {
            long n = sc.nextLong();
            long x = sc.nextLong();
            long y = sc.nextLong();

            long a = x;
            long b = y;

            while (b != 0) {
                long temp = a % b;
                a = b;
                b = temp;
            }

            long gcd = a;
            long lcm = (x / gcd) * y;

            long positive = n / x - n / lcm;
            long negative = n / y - n / lcm;

            long sum1 = positive * (2 * n - positive + 1) / 2;
            long sum = negative * (negative + 1) / 2;

            System.out.println(sum1 - sum);
        }
    }
}
