import time
from numpy import size
from pySerialTransfer import pySerialTransfer as txfer


if __name__ == '__main__':
    try:
        link = txfer.SerialTransfer('COM3')

        link.open()
        time.sleep(2)  # allow some time for the Arduino to completely reset

        # while True:
        send_size = 0

        ###################################################################
        # Send a list
        ###################################################################

        list_ = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        list_size = link.tx_obj(list_)
        send_size += list_size
        print(send_size)

        ###################################################################
        # Transmit all the data to send in a single packet
        ###################################################################
        link.send(send_size)

        ###################################################################
        # Wait for a response and report any errors while receiving packets
        ###################################################################
        while not link.available():
            if link.status < 0:
                if link.status == txfer.CRC_ERROR:
                    print('ERROR: CRC_ERROR')
                elif link.status == txfer.PAYLOAD_ERROR:
                    print('ERROR: PAYLOAD_ERROR')
                elif link.status == txfer.STOP_BYTE_ERROR:
                    print('ERROR: STOP_BYTE_ERROR')
                else:
                    print('ERROR: {}'.format(link.status))

            ###################################################################
            # Parse response list
            ###################################################################
            # rec_list_ = link.rx_obj(obj_type=type(list_),
            #                         obj_byte_size=list_size,
            #                         list_format='i')

            ###################################################################
            # Display the received data
            ###################################################################
            print('SENT: {}'.format(list_))
            # print('RCVD: {}'.format(rec_list_))
            print(' ')

    except KeyboardInterrupt:
        try:
            link.close()
        except:
            pass

    except:
        import traceback
        traceback.print_exc()

        try:
            link.close()
        except:
            pass
