import java.util.Scanner;

public class m {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        int n = sc.nextInt();
        int sereja = 0;
        int dema = 0;
        int left = 0;
        int right = n - 1;
        int[] arr = new int[n];

        for (int i = 0; i < n; i++) {
            arr[i] = sc.nextInt();
        }

        for (int i = 0; i < n; i++) {
            if (i % 2 == 0) {
                if (arr[left] < arr[right]) {
                    sereja += arr[right];
                    right--;
                } else {
                    sereja += arr[left];
                    left++;
                }
            } else {
                if (arr[left] < arr[right]) {
                    dema += arr[right];
                    right--;
                } else {
                    dema += arr[left];
                    left++;
                }
            }
        }

        System.out.println(sereja);
        System.out.println(dema);
    }
}
