start
break *main+709
continue
commands
    silent
    set $r_value = *(unsigned long long*)($rbp-0x18)
    printf "%llx\n", $r_value
    continue
end
break *main+818
commands
    silent
    set $rax=0x1337
    set $rdx=0x1337
end


