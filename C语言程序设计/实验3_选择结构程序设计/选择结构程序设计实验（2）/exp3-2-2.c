#include <stdio.h>

int main(void)
{
    int menu = 0;
    float balance = 1000.0f;  /* 一卡通初始余额 */
    float cost = 0.0f;        /* 消费金额 */
    float amount = 0.0f;      /* 充值金额 */
    int bonus = 0;            /* 本次充值奖励积分 */

    printf("菜单1代表查询余额、菜单2代表消费、菜单3代表充值\n");
    printf("请输入菜单选项（1/2/3）：");
    scanf("%d", &menu);

    switch (menu) {
    case 1:
        printf("欢迎进入一卡通查询余额功能\n");
        printf("您的余额为：%.2f元\n", balance);
        break;

    case 2:
        printf("欢迎进入一卡通消费功能\n");
        printf("请输入消费金额：");
        scanf("%f", &cost);

        if (cost <= balance) {
            balance -= cost;
            printf("消费成功，您的当前余额为：%.2f元\n", balance);
        } else {
            printf("余额不足，消费失败，您的当前余额为：%.2f元\n", balance);
        }
        break;

    case 3:
        printf("欢迎进入一卡通充值功能\n");
        printf("请输入充值金额：");
        scanf("%f", &amount);

        /* “余额累计”按充值到账后的余额判断 */
        balance += amount;

        if (amount >= 1000.0f && balance >= 2000.0f) {
            bonus = 100;
        } else if ((amount >= 500.0f && balance >= 1000.0f) ||
                   amount >= 800.0f) {
            bonus = 50;
        } else if (amount >= 200.0f) {
            bonus = 20;
        } else {
            bonus = 0;
        }

        printf("充值成功，您的当前余额为：%.2f元\n", balance);
        if (bonus > 0) {
            printf("本次充值奖励%d积分\n", bonus);
        } else {
            printf("本次充值未达到积分奖励条件\n");
        }
        break;

    default:
        printf("输入的菜单选项有误，请输入1、2或3！\n");
        break;
    }

    return 0;
}
