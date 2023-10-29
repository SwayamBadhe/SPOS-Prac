public class testJNI{
	static{
		System.loadLibrary("native");
	}
	
	public static void main(String[] args){
		System.out.println("Addition is: " + new testJNI().add(10,20));
	}	
	
	private native int add(int num1, int num2);
}


