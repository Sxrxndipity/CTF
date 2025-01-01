#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>

void pwncollege(void);

int main(int argc, char* argv[]) {
    int pid;
    int pstat;

    switch (pid = fork()) {
        case -1:
            printf("error\n");
            break;
        case 0:
            pwncollege();
            break;
    }
    waitpid(pid, &pstat, 0);
    return 0;
}
void pwncollege() {
    const char* path = "/challenge/run";
    const char* prg = "run";
    execl(path, prg, NULL);
}
