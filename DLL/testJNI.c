#include <jni.h>
#include <stdio.h>
#include "testJNI.h"

JNIEXPORT jint JNICALL Java_testJNI_add(JNIEnv *env, jobject thisobj, jint num1, jint num2){
	jint result;
	result = num1 + num2;
	return result;
}
