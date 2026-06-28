import socket
import ssl

# Connection settings for the Cisco FMC
#TLS Port 8302
FMC_IP = "Insert Your Desired IP" #eg 192.168.1.15
ESTREAMER_PORT = 8302

# Paths to the authentication certificates extracted from your .pkcs12 file
CLIENT_CERT = "fmc_estreamer_client.crt"
CLIENT_KEY = "fmc_estreamer_client.key"

def start_log_stream():
    # 1. Setup secure TLS context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.load_cert_chain(certfile=CLIENT_CERT, keyfile=CLIENT_KEY)
    
    # 2. Disable verification for testing if using FMC self-signed certs
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    print(f"Connecting to Cisco FMC eStreamer service at {FMC_IP}:{ESTREAMER_PORT}...")

    try:
        # 3. Open raw TCP network socket
        with socket.create_connection((FMC_IP, ESTREAMER_PORT), timeout=30) as raw_socket:
            # 4. Wrap the network connection with TLS encryption
            with context.wrap_socket(raw_socket, server_hostname=FMC_IP) as tls_socket:
                print("✅ Secure connection established. Stream active.")
                
                # 5. Continuous loop to read binary stream blocks
                while True:
                    # Read message header (first 8 bytes contain type and length metadata)
                    header = tls_socket.recv(8)
                    if not header:
                        print("Stream closed by the FMC server.")
                        break
                        
                    # Extract packet attributes (Normally parsed via structured schemas)
                    print(f"Received Log Data Packet. Header Buffer: {header.hex()}")
                    
                    # Read remainder of data block payload
                    # (In production, use length fields to parse exact block sizes)
                    payload = tls_socket.recv(4096) 
                    
                    # Output raw packet or forward to your security processing tool
                    print(f"Payload Stream Segment: {payload[:50]}...") 

    except Exception as e:
        print(f"❌ Failed to stream security logs: {e}")

ame__ == "__main__":
    start_log_stream()






""" 

Example Structure of Streamed Data

json{
  "EventPriority": "High",
  "SrcIP": "192.168.1.100",
  "DstIP": "10.0.0.50",
  "Protocol": "tcp",
  "SrcPort": 12345,
  "DstPort": 80,
  "IntrusionPolicy": "Security-Over-Connectivity",
  "Classification": "web-application-attack",
  "Message": "SQL injection attempt detected"
}

"""






