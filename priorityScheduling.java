import java.util.*;

public class priorityScheduling {

	public static void pln(String t) {
        System.out.println(t);
    }

    public static void p(String t) {
        System.out.print(t);
    }

	public static void main (String args[]) {
		Scanner scanner = new Scanner(System.in);
		
		p("Enter no. of processes: ");
        int n = scanner.nextInt();

        int at[] = new int[n];
        int bt[] = new int[n];
        int wt[] = new int[n];
        int tat[] = new int[n];
        int priority[] = new int[n];
        boolean completed[] = new boolean[n];

        int currentTime = 0, totalP = n;
        float avgWT = 0, avgTAT = 0;
	
        pln("Enter AT and BT for processes");

        for (int i = 0; i < n; i++) {
            pln("\tProcess: " + (i + 1));
            p("AT: ");
            at[i] = scanner.nextInt();
            p("BT: ");
            bt[i] = scanner.nextInt();
            p("Priority: ");
            priority[i] = scanner.nextInt();
            completed[i] = false;
        }
        
        while (totalP > 0) {
			int highPProcess = -1;
			int highP = Integer.MAX_VALUE;
				
			// lower number == greater priority
			for (int i=0; i<n; i++) {
				if (!completed[i] && at[i] <= currentTime && priority[i] < highP) {
					highP = priority[i];
					highPProcess = i;				
				}
			}
			
			if (highPProcess == -1) {
				currentTime++;
			} else {
				int i = highPProcess;
				//wt[i] = currentTime - at[i];
				//tat[i] = wt[i] + bt[i];
				currentTime += bt[i];
				tat[i] = currentTime - at[i];
				wt[i] = tat[i] - bt[i];
				completed[i] = true;
				totalP--;				
			}
        }
        
        for (int i = 0; i < n; i++) {
            avgTAT += tat[i];
            avgWT += wt[i];
        }

        System.out.println("\nPid\tPriority\tAT\tBT\tTAT\tWT");
        for (int  i = 0 ; i< n;  i++) {
            pln((i + 1) + "  \t " + priority[i] + "\t\t" + at[i] + "\t" + bt[i] + "\t" + tat[i] + "\t"  + wt[i] );
        }
       
        System.out.println("\naverage waiting time: "+ (avgWT/n));     
        System.out.println("average turnaround time:"+(avgTAT/n)); 
	}
}
























