#include <stdio.h>

int main(void)
{
    int length = 0; /* 矩形的长（每行星号数量） */
    int width = 0;  /* 矩形的宽（矩形的行数） */
    int i = 0;      /* 外层循环控制变量（行） */
    int j = 0;      /* 内层循环控制变量（列） */

    printf("********** 矩形文本图形绘制 **********\n");
    printf("请输入矩形的长（每行星号数）和宽（行数）：");
    if (scanf("%d %d", &length, &width) != 2) {
        printf("输入有误，请输入两个整数！\n");
        return 1;
    }

    if (length <= 0 || width <= 0) {
        printf("输入的参数无效，矩形的长和宽均必须大于 0！\n");
        return 1;
    }

    printf("\n绘制 %d 行 %d 列的星号矩形如下：\n", width, length);
    for (i = 1; i <= width; i++) {
        /* 外层循环控制行数：共输出 width 行 */
        for (j = 1; j <= length; j++) {
            /* 内层循环控制列数：每行连续输出 length 个星号 */
            printf("*");
        }
        printf("\n");   /* 每行绘制结束后换行 */
    }

    return 0;
}
