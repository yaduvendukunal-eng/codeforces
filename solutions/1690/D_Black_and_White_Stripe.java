import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();

        while (t-- > 0) {
            int n = sc.nextInt();
            int k = sc.nextInt();

            String s = sc.next();

            int w = 0;

            for (int i = 0; i < k; i++) {
                if (s.charAt(i) == 'W') {
                    w++;
                }
            }

            int minW = w;

            for (int i = k; i < n; i++) {
                if (s.charAt(i - k) == 'W') {
                    w--;
                }

                if (s.charAt(i) == 'W') {
                    w++;
                }

                minW = Math.min(minW, w);
            }

            System.out.println(minW);
        }

        sc.close();
    }
}
