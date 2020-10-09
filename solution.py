from socket import *

def transmit(socket, msg):
  socket.send(msg.encode())

def receive_reply(socket):
  return socket.recv(1024).decode()

def mail_from_cmd(fr):
  return 'MAIL FROM:<{0}>\r\n'.format(fr)

def rcpt_to_cmd(to):
  return 'RCPT TO:<{0}>\r\n'.format(to)

def data_cmd():
  return 'DATA\r\n'

def quit_cmd():
  return 'QUIT\r\n'

def join_header_tuple(header):
  return ': '.join(header)

def dot_stuff(line):
  if line[:1] == '.':
    return '.' + line
  return line

def build_message(headers, body):
  message_lines = list(map(join_header_tuple, headers))
  message_lines.append('')

  escaped_body = map(dot_stuff, body.splitlines())
  message_lines.extend(escaped_body)
  return '\r\n'.join(message_lines)

def is_250(reply):
  return reply[:3] == '250'

def is_354(reply):
  return reply[:3] == '354'

def send_mail(socket, fr, recipients, headers, body):
  endmsg = "\r\n.\r\n"

  transmit(socket, mail_from_cmd(fr))
  reply = receive_reply(socket)
  #print(reply)
  if not is_250(reply):
  #  print('250 reply not received from server.')
    return

  for recipient in recipients:
    transmit(socket, rcpt_to_cmd(recipient))
    reply = receive_reply(socket)
  #  print(reply)
    if not is_250(reply):
    #  print('250 reply not received from server.')
      return

  transmit(socket, data_cmd())
  reply = receive_reply(socket)
  #print(reply)
  if not is_354(reply):
  #  print('354 reply not received from server.')
    return

  transmit(socket, build_message(headers, body))

  transmit(socket, endmsg)
  reply = receive_reply(socket)
  if not is_250(reply):
  #  print('250 reply not received from server.')
    return

def smtp_client(port=1025, mailserver='127.0.0.1'):
    msg = "\r\n My message"

    # Choose a mail server (e.g. Google mail server) if you want to verify the script beyond GradeScope

    # Create socket called clientSocket and establish a TCP connection with mailserver and port

    # Fill in start
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailserver, port))
    # Fill in end

    recv = clientSocket.recv(1024).decode()
    #print(recv)
    #if recv[:3] != '220':
    #    print('220 reply not received from server.')

    # Send HELO command and print server response.
    heloCommand = 'HELO Alice\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    #print(recv1)
    #if recv1[:3] != '250':
    #    print('250 reply not received from server.')

    send_mail(clientSocket,
      'ky572@nyu.edu',
      ['ky572@nyu.edu'],
      [
        ('From', 'ky572@nyu.edu'),
        ('To', 'ky572@nyu.edu'),
        ('Subject', 'Test Email From CSGY6843 SMTP Client')
      ],
      msg)

    # Send QUIT command and get server response.
    # Fill in start
    transmit(clientSocket, quit_cmd())
    recv1 = receive_reply(clientSocket)
    #print(recv1)
    # Fill in end


if __name__ == '__main__':
    smtp_client(1025, '127.0.0.1')
