//gcc seededRandom.c -std=c99 -shared -fpic -O3 -o _seededRandom.so
#include <stdio.h>

unsigned long long init(char *seed, int len){
	unsigned long long a=6364136223846793005;
	unsigned long long c=1442695040888963;
	unsigned long long x=0;
	for(int i=0;i<len;i++){
		x=x*129+seed[i];
	}
	return x;
}

void step(unsigned long long *x){
	unsigned long long a=6364136223846793005;
	unsigned long long c=1442695040888963;
	unsigned long long v=(*x)%7+1;
	for(int i=0;i<v;i++){
		*x=((*x)*a+c);
	}
}

double random(unsigned long long *x){
	//step(x);
	double f=  (double)(*x)/(((unsigned long long) 1)<<63);
	return f/2;
	//return 0.0;
}

int randint(unsigned long long *x, int n){
	float f2= ( (float)(*x)/(((unsigned long long) 1)<<63) )/2;
	int out= ((int) (f2*n))%n;
	//printf("%f %d %d\n",f2,out,n);
	return out;
}









