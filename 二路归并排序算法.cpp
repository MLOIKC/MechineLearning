#include<stdio.h>
#include<malloc.h>
#include<iostream>
using namespace std;

void disp(int a[], int n) {
	for (int i = 0; i < n; i++) {
		cout << a[i] << ' ';
	}
	cout << endl;
}
void Merge(int a[], int low, int mid, int high) {//��a[low,mid]��[mid+1,high]�鲢Ϊһ����������a[low,high]
	int* temp;
	int i = low, j = mid + 1, k = 0;
	temp = (int*)malloc(sizeof(int) * (high - low + 1));//��̬����ռ�
	while (i <= mid && j <= high)//�ڱ�1�ͱ�2�ֱ����ɨ��ѭ��
		if (a[i] <= a[j]) {
			temp[k] = a[i];
			i++;
			k++;
		}
		else {
			temp[k] = a[j];
			j++;
			k++;
		}
	while (i <= mid) {
		temp[k] = a[i];
		i++;
		k++;
	}
	while (j <= high) {
		temp[k] = a[j];
		j++;
		k++;
	}
	for (k = 0, i = low; i <= high; k++, i++) {
		a[i] = temp[k];
	}
	free(temp);
}

void Mergepass(int a[],int length, int n) {
	int i;
	for (i = 0; i + 2 * length - 1 < n; i = i + 2 * length) {
		Merge(a, i, i + length - 1, i + 2 * length - 1);
	}
	if (i + length - 1 < n) {
		Merge(a, i, i + length - 1, n - 1);
	}
}


void Mergesort(int a[], int n) {
	int length;
	for (length = 1; length < n; length = 2 * length) {
		Mergepass(a, length, n);
	}
}
int main() {
	int n = 10;
	int a[] = { 1,73,23,46,72,90,33,27,52,12 };
	printf("����ǰ��");
	disp(a, n);
	Mergesort(a, n);
	printf("�����");
	disp(a, n);
}
