import java.util.*;

public class code {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();

        while (t-- > 0) {
            int n = sc.nextInt();
            int[] arr = new int[n];

            for (int i = 0; i < n; i++) {
                arr[i] = sc.nextInt();
            }

            int p = arr[n - 1] * 2;

            for (int i = n - 2; i >= 0; i--) {
                p = arr[i] - (p - arr[i]);
            }

            System.out.println(p / 2);
        }

        sc.close();
    }
}
