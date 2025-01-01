#include <stdio.h>

void win(int param1, int param2) {
    if(param1 == 0xdeadbeef && param2 == 0xc0debabe) {
        printf("you won\n");
    } else {
        printf("loser\n");
    }
}
void populate_buf() {
    char buf[16];
    scanf("%s",buf);
}
int main () {
    populate_buf();
    return 0;
}
