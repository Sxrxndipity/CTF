#include <stdio.h>

int secret_function() {
    asm("jmp %esp");
}

void receive_feedback()
{
    char buffer[64];

    puts("Please leave your comments for the server admin but DON'T try to steal our flag.txt:\n");
    gets(buffer);
}

int main()
{
    setuid(0);
    setgid(0);

    receive_feedback();

    return 0;
}
/*
 * 76 bytes offset 0x4c to overwrite eip
 * 0x0804919f : jmp esp ropgadget
 *
*/
