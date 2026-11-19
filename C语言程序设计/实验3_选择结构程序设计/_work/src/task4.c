#include <stdio.h>

int main(void)
{
    float weight = 0.0f;   /* 水果重量（kg） */
    float price = 0.0f;    /* 单价（元/kg） */
    float total = 0.0f;    /* 消费金额（元） */

    printf("请输入水果重量（kg）与单价（元）：");
    scanf("%f%f", &weight, &price);

    if (weight < 2.0f) {
        total = weight * price;              /* 不打折 */
    } else if (weight < 5.0f) {
        total = weight * price * 0.9f;       /* 九折 */
    } else {
        total = weight * price * 0.8f;       /* 八折 */
    }

    printf("水果重量%.2fkg，单价%.2f元/kg，应付金额：%.2f元\n",
           weight, price, total);

    return 0;
}
