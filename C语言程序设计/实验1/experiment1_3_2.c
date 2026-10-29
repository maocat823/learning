#include <stdio.h>
int main() {
   int a, b; // 声明两个整数变量
   // 格式化输入2个整数
   printf("请输入两个整数：\n");
   scanf("%d %d",&a,&b);
   printf("和：%d\n",a+b);
   printf("差：%d\n",a-b);
   printf("积：%d\n",a*b);
   printf("商：%d\n",a/b );
   return 0;
}
