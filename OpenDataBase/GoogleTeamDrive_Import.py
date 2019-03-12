#This is a function that when called will have the user


#Here are examples of performing a file download with our Drive API client libraries. From: https://developers.google.com/drive/api/v3/manage-downloads?authuser=1

file_id = '0BwwA4oUTeiV1UVNwOHItT0xfa2M'
request = drive_service.files().get_media(fileId=file_id)
fh = io.BytesIO()
downloader = MediaIoBaseDownload(fh, request)
done = False
while done is False:
    status, done = downloader.next_chunk()
    print "Download %d%%." % int(status.progress() * 100)