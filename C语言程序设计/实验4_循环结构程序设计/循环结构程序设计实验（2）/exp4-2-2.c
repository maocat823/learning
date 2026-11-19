#include <stdio.h>

int main(void)
{
    int height = 0; /* 等腰三角形的高度（行数） */
    int i = 0;      /* 外层循环控制变量（当前行号） */
    int j = 0;      /* 内层循环控制变量（空格或星号计数） */

    printf("********** 等腰三角形文本图形绘制 **********\n");
    printf("请输入等腰三角形的高度（行数）：");
    if (scanf("%d", &height) != 1) {
        printf("输入有误，请输入一个整数！\n");
        return 1;
    }

    if (height <= 0) {
        printf("输入的参数无效，等腰三角形的高度必须大于 0！\n");
        return 1;
    }

    printf("\n绘制高度为 %d 的等腰三角形如下：\n", height);
    for (i = 1; i <= height; i++) {
        /* 1. 内层循环一：打印第 i 行星号前的 (height - i) 个空格 */
        for (j = 1; j <= height - i; j++) {
            printf(" ");
        }
        /* 2. 内层循环二：打印第 i 行的 (2 * i - 1) 个星号 */
        for (j = 1; j <= 2 * i - 1; j++) {
            printf("*");
        }
        printf("\n");   /* 当前行绘制结束后换行 */
    }

    return 0;
}
