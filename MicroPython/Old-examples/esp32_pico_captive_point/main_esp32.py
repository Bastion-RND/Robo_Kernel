# Complete project details at https://RandomNerdTutorials.com
from machine import UART
from time import sleep

usart_flag=0
myUsart = UART(1, baudrate=115200, bits=8, parity=0, rx=14, tx=27, stop=2)

def web_page():  
  html = """<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8">
<title>ESP Web Server</title>
<link rel="icon" href="data:,">
<style type="text/css">
#action {
background:yellow;
border:0px solid #555;
color:#555;
width:0px;
height:0px;
padding:0px;
}

html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}
</style>
<script>
function AddText(text)
{
document.myform.action.value=text;
}
</script>
</head>
<body>
<h1>ESP Web Server</h1>
<form name="myform" method="get">
<textarea id="action" name="action">start</textarea>
<input id="button1" type="submit" value="Stop"  OnClick='javascript:AddText ("stop")'  />
<input id="button2" type="submit" value="↑" OnClick='javascript:AddText ("start")' />
<input id="button3" type="submit" value="↓"  OnClick='javascript:AddText ("back")'  />
<input id="button4" type="submit" value="←"  OnClick='javascript:AddText ("left")'  />
<input id="button5" type="submit" value="→" OnClick='javascript:AddText ("right")' />
</form>
</body>
</html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  mv_start = request.find('/?action=start')
  mv_back = request.find('/?action=back')
  mv_right = request.find('/?action=right')
  mv_left = request.find('/?action=left')
  mv_stop = request.find('/?action=stop')
  if mv_start == 6:
    print('start')
    myUsart.write(str("\r\nstart\n"))
  if mv_back == 6:
    print('back')
    myUsart.write(str("\r\nback\n"))
#     led.value(0)
  if mv_right == 6:
    print('right')
    myUsart.write(str("\r\nright\n"))
  if mv_left == 6:
    print('left')
    myUsart.write(str("\r\nleft\n"))
  if mv_stop == 6:
    print('stop')
    myUsart.write(str("\r\nstop\n"))
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  conn.sendall(response)
  conn.close()
