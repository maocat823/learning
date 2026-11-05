#include <stdio.h>

int main(void)
{
    int menu = 0;

    printf("菜单1代表查询余额、菜单2代表消费、菜单3代表充值\n");
    printf("请输入菜单选项（1/2/3）：");
    scanf("%d", &menu);

    switch (menu) {
    case 1:
        printf("欢迎进入一卡通查询余额功能\n");
        break;
    case 2:
        printf("欢迎进入一卡通消费功能\n");
        break;
    case 3:
        printf("欢迎进入一卡通充值功能\n");
        break;
    default:
        printf("输入的菜单选项有误，请输入1、2或3！\n");
        break;
    }

    return 0;
}
