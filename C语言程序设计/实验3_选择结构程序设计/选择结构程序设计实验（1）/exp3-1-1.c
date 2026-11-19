#include <stdio.h>

int main(void)
{
    float amount = 0.0f;   /* 充值金额（元） */
    int point = 0;         /* 本次奖励积分 */

    printf("请输入一卡通充值金额（元）：");
    scanf("%f", &amount);

    if (amount >= 1000.0f) {
        point = (int)(amount / 100.0f);   /* 每满100元得1积分，(int)取整 */
        printf("本次充值可奖励%d积分\n", point);
    } else {
        printf("充值金额不足1000元，本次充值不奖励积分\n");
    }

    return 0;
}
