package ME;

import java.util.*;

public class FCFS {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Enter no. of process: ");
        int n = scanner.nextInt();

        int[] pid = new int[n];
        int[] at = new int[n];
        int[] bt = new int[n];
        int[] ct = new int[n];
        int[] tat = new int[n];
        int[] wt = new int[n];

        float avgWT = 0, avgTAT = 0;

        // Taking Input
        System.out.println("Enter AT and BT for processes");

        for (int i=0; i!=n; i++) {
            System.out.println("\tProcess: " + (i+1));
            System.out.print(("AT: "));
            at[i] = scanner.nextInt();
            System.out.print(("BT: "));
            bt[i] = scanner.nextInt();
            pid[i] = i+1;
        }        

        // Sorting
        for (int i=0; i!=n; i++) {
            for (int j=0; j!=n-(i+1); j++) {
                if (at[j] > at[j+1]) {
                    swap(at, j, j+1);
                    swap(bt, j, j+1);
                    swap(pid, j, j+1);
                }
            }
        }

        // Completion Time
        for (int i=0; i!=n; i++) {
            if (i==0) {
                ct[i] = at[i] + bt[i];
            } else {
                if (at[i] > ct[i-1]) {
                    ct[i] = at[i] + bt[i];
                } else {
                    ct[i] = ct[i-1] + bt[i];
                }
            }
            tat[i] = ct[i] - at[i];
            wt[i] = tat[i] - bt[i];
            avgWT += wt[i];
            avgTAT += tat[i];
        }

        System.out.println("\nPid\tAT\tBT\tCT\tTAT\tWT");
        for (int  i = 0 ; i< n;  i++) {
            System.out.println(pid[i] + "  \t " + at[i] + "\t" + bt[i] + "\t" + ct[i] + "\t" + tat[i] + "\t"  + wt[i] ) ;
        }
       
        System.out.println("\naverage waiting time: "+ (avgWT/n));     
        System.out.println("average turnaround time:"+(avgTAT/n));    
        scanner.close();
    }

    public static void swap(int[] arr, int i, int j) {
        int temp = arr[j];
        arr[j] = arr[i];
        arr[i] = temp;
    }
}
