# Debugging REST API with Command Line
## Overview `nc` command
Netcat is a utility that [reads](https://www.computerhope.com/jargon/r/read.htm) and [writes](https://www.computerhope.com/jargon/w/write.htm) [data](https://www.computerhope.com/jargon/d/data.htm) across [network](https://www.computerhope.com/jargon/n/network.htm) connections, using the [TCP](https://www.computerhope.com/jargon/t/tcpip.htm) or [UDP](https://www.computerhope.com/jargon/u/udp.htm) [protocols](https://www.computerhope.com/jargon/p/protocol.htm). It is designed to be a reliable "back-end" tool, used directly or driven by other programs and [scripts](https://www.computerhope.com/jargon/s/script.htm). At the same time, it is a feature-rich network [debugging](https://www.computerhope.com/jargon/d/debug.htm) and exploration tool since it can create almost any kind of connection you would need and has several interesting built-in capabilities.
Common uses include:

* Simple TCP [proxies](https://www.computerhope.com/jargon/p/proxyser.htm)
* [Shell](https://www.computerhope.com/jargon/s/shell.htm)-script based HTTP [clients](https://www.computerhope.com/jargon/c/client.htm) and [servers](https://www.computerhope.com/jargon/s/server.htm)
* Network [daemon](https://www.computerhope.com/jargon/d/daemon.htm) testing
* A [SOCKS](https://www.computerhope.com/jargon/s/socks.htm) or HTTP ProxyCommand for [ssh](https://www.computerhope.com/jargon/s/ssh.htm)

Run `man nc` to have an overview.


## Create Chat Server

Interestingly the nc command can be used to create chat server where multiple users can connect and send messages. The methodology used to create chat server is the same with file transfer. In this case simple text is transferred between local and remote systems.
* First we will create a listening port which will be 4444 in this case.
```bash
    nc -l 4444
```
* On the another terminal (on the same computer or another computer) we will connect to the chat server by providing its IP address and port number which is 4444.
```bash
    nc <ip address> 4444
```
where `<ip address> ` is replaced by  your local ip `127.0.0.1` if running the command on the same machine as the server, or replaced by the server ip. You will get something similar to the picture below:
![](/tutorials/sys/sys6-chat.png)


## Make HTTP Request

The `nc` command can be used to make HTTP Requests to the remote web server. Even there are more useful tools nc provides basic usage about making HTTP Requests. The HTTP Request text is redirected into the nc command where the nc command uses the specified remote web server IP address/Hostname and port number.
```bash
    printf "GET / HTTP/1.1" | nc google.com 80
```
Notice the pipe `|` commands shifts the output of the comands on left hand side to the input of the right hand side.

Alternatively the multiple lines for the HTTP Request can be expressed by using the “\\r\\n” end of line.
```bash
    printf "GET / HTTP/1.1\r\nHost:google.com\r\n\r\n" | nc google.com 80
```


