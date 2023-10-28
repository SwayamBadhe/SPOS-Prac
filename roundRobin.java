import java.util.*;

public class roundRobin {

    public static void pln(String t) {
        System.out.println(t);
    }

    public static void p(String t) {
        System.out.print(t);
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        p("Enter no. of processes: ");
        int n = scanner.nextInt();
        p("Enter time quanta: ");
        int tq = scanner.nextInt();

        int at[] = new int[n];
        int bt[] = new int[n];
        int wt[] = new int[n];
        int tat[] = new int[n];
        int t_bt[] = new int[n];
        boolean completed[] = new boolean[n];

        int currentTime = 0, maxPIndex = 0;
        float avgWT = 0, avgTAT = 0;

        pln("Enter AT and BT for processes");

        for (int i = 0; i < n; i++) {
            System.out.println("\tProcess: " + (i + 1));
            System.out.print("AT: ");
            at[i] = scanner.nextInt();
            System.out.print("BT: ");
            bt[i] = scanner.nextInt();
            t_bt[i] = bt[i];
            completed[i] = false;
        }

        // Advance to the first arrival time
        while (currentTime < at[0]) {
            currentTime++;
        }

        int pQueue[] = new int[100]; // Create a process queue
        int front = 0; // Front of the queue
        int rear = 0; // Rear of the queue
        
        boolean allComplete = false;
        
        for (int i = 0; i < n; i++) {
        	if (at[i] <= currentTime) {
				pQueue[rear] = i;
				rear++;
			}
        }
	
		while (!allComplete) {
			int currP = pQueue[front];
			for (int i=front; i!=rear; i++) {
				p(pQueue[i] + " ");
			}
			pln(" ");
			front++;
			
			int cbt = Math.min(tq, t_bt[currP]);
            currentTime += cbt;
            t_bt[currP] -= cbt;		
			
			if (t_bt[currP] == 0) {
                tat[currP] = currentTime - at[currP];
                wt[currP] = tat[currP] - bt[currP];
                completed[currP] = true;
            }
            
            // check if all process are complete
            allComplete = true;
			for (int i = 0; i < n; i++) {
				if (!completed[i]) {
					allComplete = false;
					break;
				}
			}
            
            // check if any new process arrived while the current
            // process was executing
            for (int i=0; i!=n; i++) {
            	if (at[i] <= currentTime && at[i] > currentTime-tq && !completed[i]) {
            		if (i != currP) {
	            		pQueue[rear] = i;
	            		rear++;
            		}
            	}         
            }
            
            // add the current process after new process
            if (completed[currP] == false) {
				pQueue[rear] = currP;
            	rear++;            
            }
		}
        

        for (int i = 0; i < n; i++) {
            avgTAT += tat[i];
            avgWT += wt[i];
        }

        avgTAT /= n;
        avgWT /= n;

        System.out.println("Process\tArrival Time\tBurst Time\tWait Time\tTurnaround Time");
        for (int i = 0; i < n; i++) {
            System.out.println((i + 1) + "\t\t" + at[i] + "\t\t" + bt[i] + "\t\t" + wt[i] + "\t\t" + tat[i]);
        }

        System.out.println("\nAverage wait time: " + avgWT);
        System.out.println("Average Turnaround Time: " + avgTAT);
    }
}

