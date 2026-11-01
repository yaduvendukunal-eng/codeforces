import java.util.*;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();

        while (t-- > 0) {
            int n = sc.nextInt();
            int k = sc.nextInt();
            int q = sc.nextInt();

            long result = 0;
            int len = 0;

            for (int i = 0; i < n; i++) {
                int temp = sc.nextInt();

                if (temp <= q) {
                    len++;

                    if (len >= k) {
                        result += len - k + 1;
                    }
                } else {
                    len = 0;
                }
            }

            System.out.println(result);
        }
    }
}
