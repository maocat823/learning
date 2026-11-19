#include <stdio.h>

int main(void)
{
    float balance = 0.0f;  /* 一卡通余额 */
    float cost = 0.0f;     /* 消费金额 */

    printf("请输入一卡通余额（元）：");
    scanf("%f", &balance);
    printf("请输入本次消费金额（元）：");
    scanf("%f", &cost);

    if (cost <= balance) {
        balance = balance - cost;
        printf("刷卡成功，消费%.2f元，当前余额%.2f元\n", cost, balance);
    } else {
        printf("余额不足，请充值\n");
    }

    return 0;
}
