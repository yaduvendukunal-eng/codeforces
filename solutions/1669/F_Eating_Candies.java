import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        int t = sc.nextInt();

        while (t-- > 0) {
            int n = sc.nextInt();

            int[] wt = new int[n];

            for (int i = 0; i < n; i++) {
                wt[i] = sc.nextInt();
            }

            int left = 0;
            int right = n - 1;
            int rw = 0;
            int lw = 0;
            int candy = 0;
            int maxcandy = 0;

            do {
                if (rw <= lw) {
                    rw += wt[right];
                    right--;
                    candy++;
                } else {
                    lw += wt[left];
                    left++;
                    candy++;
                }

                if (rw == lw) {
                    maxcandy = candy;
                }
            } while (left <= right);

            System.out.println(maxcandy);
        }
    }
}
