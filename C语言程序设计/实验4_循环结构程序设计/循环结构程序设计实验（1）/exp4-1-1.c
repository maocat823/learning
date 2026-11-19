#include <stdio.h>

int main(void)
{
    int menu = 0;   /* 菜单选项 */
    int sum = 0;    /* 库存总量，初始为 0 */
    int count = 0;  /* 每个批次的入库或出库数量 */
    int i = 0;      /* 批次计数 */
    int over = 0;   /* 退出标志，为 1 时结束系统 */

    while (!over) {
        /* 1. 主菜单：由 while 循环反复显示，直到用户选择退出 */
        printf("\n********** 仓库库存管理系统 **********\n");
        printf("  1.入库   2.出库   3.查询库存   4.退出\n");
        printf("请输入操作选项（1-4）：");

        if (scanf("%d", &menu) != 1) {
            printf("输入有误，请输入数字选项！\n");
            while (getchar() != '\n') {
                ;   /* 清空缓冲区中的非法字符 */
            }
            continue;   /* 本次输入作废，重新显示菜单 */
        }

        switch (menu) {
        case 1:
            /* 2. 入库：for 循环连续处理 5 个批次 */
            printf("\n---------- 入 库 ----------\n");
            for (i = 1; i <= 5; i++) {
                printf("请输入第%d批次入库数量（输入<=0结束）：", i);
                scanf("%d", &count);
                if (count <= 0) {
                    printf("入库数量必须大于 0，本次入库结束。\n");
                    break;          /* 结束入库的 for 循环 */
                }
                sum += count;
                printf("入库成功，当前库存为：%d\n", sum);
            }
            break;

        case 2:
            /* 3. 出库：for 循环连续处理 5 个批次 */
            printf("\n---------- 出 库 ----------\n");
            for (i = 1; i <= 5; i++) {
                printf("请输入第%d批次出库数量：", i);
                scanf("%d", &count);
                if (count > sum) {
                    printf("出库数量超过当前库存 %d，本次出库无效！\n", sum);
                    continue;       /* 跳过本次出库，直接进入下一批次 */
                }
                if (count <= 0) {
                    printf("出库数量必须大于 0，本次出库无效！\n");
                    continue;
                }
                sum -= count;
                printf("出库成功，当前库存为：%d\n", sum);
            }
            break;

        case 3:
            /* 4. 查询：直接输出当前库存 */
            printf("\n---------- 查询库存 ----------\n");
            printf("当前库存数量为：%d\n", sum);
            break;

        case 4:
            /* 5. 退出：置退出标志，循环结束后程序结束 */
            printf("\n已退出仓库库存管理系统，再见！\n");
            over = 1;
            break;

        default:
            printf("输入的菜单选项有误，请输入 1-4 之间的数字！\n");
            break;
        }

        if (over) {
            break;      /* 跳出 while 主循环，结束系统 */
        }
    }

    return 0;
}
