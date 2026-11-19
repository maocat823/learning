#include <stdio.h>

int main(void)
{
    float a = 0.0f, b = 0.0f, c = 0.0f;
    float max = 0.0f;

    printf("请输入三个实数：");
    scanf("%f%f%f", &a, &b, &c);

    if (a >= b) {          /* 外层判断：a与b中较大的一个 */
        if (a >= c) {
            max = a;
        } else {
            max = c;
        }
    } else {
        if (b >= c) {
            max = b;
        } else {
            max = c;
        }
    }

    printf("三个数%.2f、%.2f、%.2f中的最大值是：%.2f\n", a, b, c, max);

    return 0;
}
