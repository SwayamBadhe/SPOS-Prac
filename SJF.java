import java.util.Scanner;

public class SJF {
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
        int[] btRemaining = new int[n];
        boolean completed[] = new boolean[n];

        float avgWT = 0, avgTAT = 0;
        // Taking Input
        System.out.println("Enter AT and BT for processes");

        for (int i=0; i!=n; i++) {
            System.out.println("\tProcess: " + (i+1));
            System.out.print(("AT: "));
            at[i] = scanner.nextInt();
            System.out.print(("BT: "));
            bt[i] = scanner.nextInt();
            pid[i] = i + 1;
            btRemaining[i] = bt[i];
        } 

        int currentTime = 0;
        int completedProcesses = 0;

        while (completedProcesses < n) {
            int min = Integer.MAX_VALUE;
            int c = -1;

            for (int i=0; i!=n; i++) {
                if (at[i] <= currentTime && btRemaining[i] < min && btRemaining[i] > 0) {
                    min = btRemaining[i];
                    c = i;
                }
            }

            if (c == -1) {
                currentTime++;
            } else {
                currentTime++;
                btRemaining[c]--;
                
                if (btRemaining[c] == 0) {
                    ct[c] = currentTime;
                    completed[c] = true;
                    completedProcesses++;
                }                
            }
        }

        for (int i=0; i!=n; i++) {
            tat[i] = ct[i] - at[i];
            wt[i] = tat[i] - bt[i];
            avgWT += wt[i];
            avgTAT += tat[i];
        }

        System.out.println("\nPid\tAT\tBT\tCT\tTAT\tWT");
        for (int i=0; i!=n; i++) {
            System.out.println(pid[i] + "  \t " + at[i] + "\t" + bt[i] + "\t" + ct[i] + "\t" + tat[i] + "\t"  + wt[i]);
        }

        System.out.println("\naverage waiting time: "+ (avgWT/n));     
        System.out.println("average turnaround time:"+(avgTAT/n));    
        scanner.close();
    }
}
