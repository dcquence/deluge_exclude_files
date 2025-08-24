from deluge_client import DelugeRPCClient

client = DelugeRPCClient('127.0.0.1', 58846, 'user', 'password')

try:
    client.connect()
except Exception as e:
    print(f"Failed to connect to Deluge: {e}")
    exit(1)

# Specify the unwanted file extensions
unwanted_extensions = [
    '.zipx', '.mkv.lnk', '.arj', '.mkv.exe',
    '.001', '.gz', '.tz', '.lzh', '.scr', '.exe', '.iso'
]

def check_and_remove_torrents():
    torrents = client.call('core.get_torrents_status', {}, [b'name', b'files'])
    
    for torrent_id, torrent_data in torrents.items():
        torrent_name = torrent_data.get(b'name', b'Unknown Name').decode('utf-8', errors='ignore')
        files = torrent_data.get(b'files', [])

        if not files:
            print(f"No files found for torrent '{torrent_name}' (ID: {torrent_id}), skipping.")
            continue

        for file_info in files:
            file_name = file_info.get(b'path', b'').decode('utf-8', errors='ignore')
            if any(file_name.endswith(ext) for ext in unwanted_extensions):
                print(f"Removing torrent '{torrent_name}' due to unwanted file '{file_name}'")
                client.call('core.remove_torrent', torrent_id, True)
                break

check_and_remove_torrents()
