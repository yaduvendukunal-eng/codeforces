import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int t = sc.nextInt();

        while (t-- > 0) {
            String s = sc.next();
            int n = s.length();

            int zeros = 0;
            int ones = 0;

            for (char c : s.toCharArray()) {
                if (c == '0') {
                    zeros++;
                } else {
                    ones++;
                }
            }

            int ans = 0;

            for (int i = 0; i < n; i++) {
                if (s.charAt(i) == '0') {
                    if (ones > 0) {
                        ones--;
                    } else {
                        ans = n - i;
                        break;
                    }
                } else {
                    if (zeros > 0) {
                        zeros--;
                    } else {
                        ans = n - i;
                        break;
                    }
                }
            }

            System.out.println(ans);
        }

        sc.close();
    }
}
