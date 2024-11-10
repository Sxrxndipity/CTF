.intel_syntax noprefix

.global _start

.section .rodata
    msg:            .asciz "HTTP/1.0 200 OK \r\n\r\n"

.section .data
    .equ AF_INET, 2
    .equ PORT, 0x5000
    .equ IP_ADDR, 0x00000000
    buffer:         .space 1024
    seperator:      .ascii "\r\n\r\n"
    request_get:    .ascii "GET "
    request_post:   .ascii "POST "
    socket_fd:      .quad 0
    accept_fd:      .quad 0
    open_fd:        .quad 0

.section .text

_start:
//socket(AF_INET,SOCK_STREAM,IPPROTO_IP)
mov rdi,2
mov rsi,1
mov rdx,0
mov rax,41
syscall
mov sock_fd,rax

//bind(sock_fd,struct sock_addr, sock_addr length=16bytes)
//sock_addr{int16 AF_INET=2, int16 port=80, int32 addr=0.0.0.0}
mov rdi,sock_fd
mov dword ptr[rsp - 4],IP_ADDR
mov word ptr[rsp - 6],PORT
mov word ptr[rsp - 8],AF_INET
sub rsp,0x8
mov rsi,rsp
mov rdx,16
mov rax,49
syscall

//listen(sock_fd, int backlog)
mov rdi,sock_fd
mov rsi,0
mov rax,50
syscall

parent_process1:
//accept(sock_fd,NULL,NULL)
mov rdi,sock_fd
mov rsi,0
mov rdx,0
mov rax,43
syscall
mov accept_fd,rax

//fork()
mov rax,57
syscall
test rax,rax
jnz parent_process2
jz child_process

parent_process2:
//close(accept_FD)
mov rdi,accept_fd
mov rax,3
syscall
jmp parent_process1

child_process:
//close(socket_fd)
mov rdi,socket_fd
mov rax,3
syscall

//read(accept_fd,buffer,buffer_len) = length of data read
mov rdi,accept_fd
lea rsi,buffer
mov rdx,1024
mov rax,0
syscall
push rax

//Parse method (GET or POST)
mov eax,buffer
mov ebx,request_get
cmp eax,ebx
je handle_get
mov ebx,request_post
cmp eax,ebx
je handle_post
jmp exit

handle_get:
//open(filepath,flag=O_RDONLY=0)
lea rdi,[rsi + 4]
movb [rdi + 16],0
mov rsi,0
mov rax,2
syscall
mov open_fd,rax

//read(open_fd,buffer,buffer_len) = length of data in file
mov rdi,open_fd
lea rsi,buffer
mov rdx,1024
mov rax,0
syscall
push rax

//close(open_fd)
mov rdi,open_fd
mov rax,3
syscall

//write(accept_fd,msg,msg_len)
mov rdi,accept_fd
mov rsi,msg
mov rdx,19
mov rax,1
syscall

//write(accept_fd,buffer(contains data returned by read), buffer_len)
mov rdi,accept_fd
lea rsi,buffer
pop rax
mov rdx,rax
mov rax,1
syscall
jmp exit

handle_post:
//open(filepath, O_WDONLY | O_CREAT = 0x41, 0777)
lea rdi,[rsi + 5]
movb [rdi + 16],0
mov rsi,0x41
mov rdx,0777
mov rax,2
syscall
mov open_fd,rax

//write(open_fd, POST body, length)
//locate POST body
xor rcx,rcx
mov ebx,seperator
locate_body:
mov eax, [buffer+rcx]
add rcx,1
cmp eax,ebx
jne locate_body
add rcx,3
mov rdi,open_fd
lea rsi,[buffer+rcx]
pop rax
mov rdx,rax
sub rdx,rcx
mov rax,1
syscall

//close(open_fd)
mov rdi,open_fd
mov rax,3
syscall

//write(accept_fd,msg,msg_len)
mov rdi,accept_fd
lea rsi,msg
mov rdx,19
mov rax,1
syscall


exit:
mov rdi,0
mov rax,60
syscall







