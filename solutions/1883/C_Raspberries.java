import java.util.*;

public class Main {
    public static int func(int[] arr, int k, int n) {
        if (k == 4) {
            int evenCount = 0;
            int minOperations = 4;

            for (int i = 0; i < n; i++) {
                if (arr[i] % 4 == 0) {
                    return 0;
                }

                if (arr[i] % 2 == 0) {
                    evenCount++;
                }

                int operations = 4 - (arr[i] % 4);
                minOperations = Math.min(minOperations, operations);
            }

            if (evenCount >= 2) {
                return 0;
            }

            if (evenCount == 1) {
                return 1;
            }

            return Math.min(minOperations, 2);
        }

        int ans = k;

        for (int i = 0; i < n; i++) {
            if (arr[i] % k == 0) {
                return 0;
            }

            int operations = k - (arr[i] % k);
            ans = Math.min(ans, operations);
        }

        return ans;
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();

        while (t-- > 0) {
            int n = sc.nextInt();
            int k = sc.nextInt();

            int[] arr = new int[n];

            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }

            System.out.println(func(arr, k, n));
        }

        sc.close();
    }
}
